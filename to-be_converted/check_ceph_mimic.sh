# Sample Output:
# 2 Ceph_Health - HEALTH_WARN noout flag(s) set
# P Ceph_Space TB_used=138|Percent_used=32.0;85;90 32.0% used (138 TiB of 437 TiB)
# 0 Ceph_Stats io_read_mibs=0|io_write_mibs=0|ops_rd_sec=|ops_wr_sec=0 IO/read: 0 MiB/s - IO/write: 0 MiB/s - OP/s Read:  - OP/s Write: 0
# 0 Ceph_Recovery rec_io_mibs=0|obj_sec=0 Currently no recovery running
# 0 Ceph_Scrubbing deep_scrub=2|scrubbing=0 Number of PGs deep scrubbing: 2 | Number of PGs scrubbing: 0
 
#!/bin/bash
#set -vx
 
#####Health########
 
STATEOSD=`ceph health |grep osdmap`
OSDS=`echo $STATEOSD |cut -d " " -f 3`
OSDSUP=`echo $STATEOSD |cut -d " " -f 5`
OSDSIN=`echo $STATEOSD |cut -d " " -f 7`
BLOCKED_Requests=`ceph health | grep "requests are blocked"`
 
STATE=`ceph health`
if [ "$STATE" != "HEALTH_OK" ] || [ "$OSDS" != "$OSDSUP" ] || [ "$OSDS" != "$OSDSIN" ] || [ "$BLOCKED_Requests" != "" ]; then
        ####### repair osd by TCo ######
#        STATEDETAIL=`ceph health detail`
#        INCONSISTENPGS=`ceph health detail | grep -i +incons | cut -d " " -f 2`
#        INCONSISTENOSDS=`echo $STATEDETAIL | grep -i +incons | cut -d " " -f 6 | sed 's/\[//' | sed 's/\]//' | sed 's/\,/ /g'`
#        IOSD1=`echo $INCONSISTENTOSDS | cut -d " " -f 1`
#        IOSD2=`echo $INCONSISTENTOSDS | cut -d " " -f 2`
#        IOSD3=`echo $INCONSISTENTOSDS | cut -d " " -f 3`
#        NUMBERS=`ceph osd tree | grep flash -A 1 | grep osd | cut -c 1-2`
#        case "${numbers[@]}" in *"$IOSD1"* ) `ceph pg repair $INCONSISTENPGS` ;; esac
        ################################
        healthstatus=2
else
        healthstatus=0
 
fi
 
#####Space#######
swarn=85
scrit=90
 
size=`ceph status |grep used`
total=`echo $size |awk '{print $8}'`
free=`echo $size |awk '{print $5}'`
used=`echo $size |awk '{print $2}'`
used_unit=`echo $size | awk '{print $3}'`
free_unit=`echo $size | awk '{print $6}'`
total_unit=`echo $size | awk '{print $9}'`
 
if [ $used_unit == "GiB" ]; then
        usedtb=`echo "scale=1; $used/1024" |bc -l`
        percentused=`echo "scale=1; $usedtb/($total/100)" |bc -l`
elif [ $used_unit == "TiB" ]; then
        usedtb=$used
        percentused=`echo "scale=1; $usedtb/($total/100)" |bc -l`
fi
 
#####Stats#######
# io:
#       client:   19 KiB/s rd, 1.9 MiB/s wr, 18 op/s rd, 34 op/s wr
#       recovery: 294 MiB/s, 73 objects/s
 
stats=$(ceph -s |grep "client:")
if [ -z "$stats" ]
        then
        io_read=0
        io_write=0
        ops_rradd=0
        ops_write=0
        else
        iord=$(echo $stats | awk '{print $2}')
        iord_unit=$(echo $stats | awk '{print $3}')
        if [ $(echo $stats | awk '{print $7}') == "rd," ]; then
                iowr=0
                iowr_unit=$iord_unit
                ops_rd=$(echo $stats | awk '{print $5}')
                ops_rd_unit=$(echo $stats | awk '{print $6}')
                ops_wr=0
                ops_wr_unit=$ops_rd_unit
        elif [ $(echo $stats | awk '{print $7}') == "wr," ]; then
                iowr=$(echo $stats | awk '{print $5}')
                iowr_unit=$(echo $stats | awk '{print $6}')
                ops_rd=$(echo $stats | awk '{print $8}')
                ops_rd_unit=$(echo $stats | awk '{print $9}')
                ops_wr=$(echo $stats | awk '{print $11}')
                ops_wr_unit=$(echo $stats | awk '{print $12}')
        fi
fi
 
#JPo Fixed MB/s and GB/s => Calculate current MB/s cluster io
#       io_read=`echo "$iord/1024" | bc -l`
 
if [ "$iord_unit" == "B/s" ]
        then
        io_read=`echo "scale=2; $iord/1024/1024" | bc -l`
elif [ "$iord_unit" == "KiB/s" ]
        then
        io_read=`echo "scale=2; $iord/1024" | bc -l`
elif [ "$iord_unit" == "MiB/s" ]
        then
        io_read=$iord
elif [ "$iord_unit" == "GiB/s" ]
        then
        io_read=`echo "scale=2; $iord*1024" | bc -l`
fi
 
if [ "$ops_rd_unit" == "kop/s" ]
        then
        ops_read=`echo "scale=2; $ops_rd*1000" | bc -l`
elif [ "$ops_rd_unit" == "op/s" ]
        then
        ops_read=$ops_rd
fi
 
if [ "$iowr_unit" == "B/s" ]
        then
        io_write=`echo "scale=2; $iowr/1024/1024" | bc -l`
elif [ "$iowr_unit" == "KiB/s" ]
        then
        io_write=`echo "scale=2; $iowr/1024" | bc -l`
elif [ "$iowr_unit" == "MiB/s" ]
        then
        io_write=$iowr
elif [ "$iord_unit" == "GiB/s" ]
        then
        io_write=`echo "scale=2; $iowr*1024" | bc -l`
fi
 
typeset -i ops_write
if [ "$ops_wr_unit" == "kop/s" ]
        then
        ops_write=`echo "scale=2; $ops_wr*1000" | bc -l`
elif [ "$ops_wr_unit" == "op/s" ]
        then
        ops_write=$ops_wr
fi
 
#####Recovery#######
recovery=$(ceph -s | grep "recovery:")
 
if [ -z "$recovery" ]
        then
        recovery_io=0
        recovery_obj=0
        recovery_info="Currently no recovery running"
        else
        recovery_io=$(echo $recovery | awk '{print $2}')
        recovery_io_unit=$(echo $recovery | awk '{print $3}')
        recovery_obj=$(echo $recovery | awk  '{print $4}')
        recovery_obj_unit=$(echo $recovery | awk  '{print $5}')
 
        typeset -i rec_io
        if [ "$recovery_io_unit" == "B/s" ]
                then
                rec_io=`echo "scale=2; $recovery_io/1024/1024" | bc -l`
        elif [ "$recovery_io_unit" == "KiB/s" ]
                then
                rec_io=`echo "scale=2; $recovery_io/1024" | bc -l`
        elif [ "$recovery_io_unit" == "MiB/s" ]
                then
                rec_io=$recovery_io
        elif [ "$recovery_io_unit" == "GiB/s" ]
                then
                rec_io=`echo "scale=2; $recovery_io*1024" | bc -l`
        fi
        recovery_info="IO: $recovery_io MiB/s - Ojects/s: $recovery_obj"
fi
 
#####Scrubbing#####
scrubbing=$(ceph -s | egrep scrubbing$ |awk '{print $1}')
deep_scrubbing=$(ceph -s | grep scrubbing+deep |awk '{print $1}')
if [ "$scrubbing" == "" ]; then
        scrub=0
elif [ "$scrubbing" != "" ]; then
        scrub=$scrubbing
fi
 
if [ "$deep_scrubbing" == "" ]; then
        deep_scrub=0
elif [ "$deep_scrubbing" != "" ]; then
        deep_scrub=$deep_scrubbing
fi
 
scrubbing_info="Number of PGs deep scrubbing: $deep_scrub | Number of PGs scrubbing: $scrub"
 
##########output###########
 
echo "$healthstatus Ceph_Health - $STATE"
echo "P Ceph_Space TB_used=$usedtb|Percent_used=$percentused;$swarn;$scrit $percentused% used ($usedtb TiB of $total $total_unit)"
echo "0 Ceph_Stats io_read_mibs=$io_read|io_write_mibs=$io_write|ops_rd_sec=$ops_read|ops_wr_sec=$ops_write IO/read: $io_read MiB/s - IO/write: $io_write MiB/s - OP/s Read: $ops_read - OP/s Write: $ops_write"
echo "0 Ceph_Recovery rec_io_mibs=$recovery_io|obj_sec=$recovery_obj $recovery_info"
echo "0 Ceph_Scrubbing deep_scrub=$deep_scrub|scrubbing=$scrub $scrubbing_info"