#!/usr/bin/python
from myutil import file
import json

file1 = file("../to-be_converted/sample-outputs/ceph-s.json")
data = file1.read()

jsonfile = json.loads(data)

#Ceph_Space
space_warn = 85
space_crit = 90

data_bytes = jsonfile["pgmap"]["data_bytes"]
bytes_total = jsonfile["pgmap"]["bytes_total"]
bytes_avail = jsonfile["pgmap"]["bytes_avail"]
bytes_used  = jsonfile["pgmap"]["bytes_used"]

tb_used = float(bytes_used)/(2**40)
perc_used = (float(bytes_used)/float(bytes_total))*100
tb_total = float(bytes_total)/(2**40)

print "P Ceph_Space TB_used={0:.2f}|Percent_used={1:.2f};{2};{3} Currently {1:f}%% used ({0:.2f} TiB of {4:.2f} TiB)".format(tb_used,perc_used,space_warn,space_crit,tb_total)

#Ceph_Degraded
degraded_objects = jsonfile["pgmap"]["degraded_objects"]
degraded_total = jsonfile["pgmap"]["degraded_total"]
degraded_ratio = jsonfile["pgmap"]["degraded_ratio"]

#Ceph_Misplaced
misplaced_objects = jsonfile["pgmap"]["misplaced_objects"]
misplaced_total = jsonfile["pgmap"]["misplaced_total"]
misplaced_ratio = jsonfile["pgmap"]["misplaced_ratio"]

#Ceph_Recovery
recovering_objects_per_sec = jsonfile["pgmap"]["recovering_objects_per_sec"]
recovering_bytes_per_sec = jsonfile["pgmap"]["recovering_bytes_per_sec"]
recovering_keys_per_sec = jsonfile["pgmap"]["recovering_keys_per_sec"]

#Ceph_Stats
read_bytes_sec = jsonfile["pgmap"]["read_bytes_sec"]
write_bytes_sec  = jsonfile["pgmap"]["write_bytes_sec"]
read_op_per_sec  = jsonfile["pgmap"]["read_op_per_sec"]
write_op_per_sec  = jsonfile["pgmap"]["write_op_per_sec"]

#Ceph_Scrubbing

#Ceph_Health


# Old outputs
#echo "$healthstatus Ceph_Health - $STATE"
#echo "0 Ceph_Stats io_read_mibs=$io_read|io_write_mibs=$io_write|ops_rd_sec=$ops_read|ops_wr_sec=$ops_write IO/read: $io_read MiB/s - IO/write: $io_write MiB/s - OP/s Read: $ops_read - OP/s Write: $ops_write"
#echo "0 Ceph_Recovery rec_io_mibs=$recovery_io|obj_sec=$recovery_obj $recovery_info"
#echo "0 Ceph_Scrubbing deep_scrub=$deep_scrub|scrubbing=$scrub $scrubbing_info"
