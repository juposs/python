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
try:
    degraded_objects = jsonfile["pgmap"]["degraded_objects"]
except KeyError:
    degraded_objects = 0

try:
    degraded_total = jsonfile["pgmap"]["degraded_total"]
except KeyError:
    degraded_total = 0

try:
    degraded_ratio = jsonfile["pgmap"]["degraded_ratio"]
except KeyError:
    degraded_ratio = 0

#print "{0} {1} {2}".format(degraded_objects, degraded_total, degraded_ratio)

#Ceph_Misplaced
try:
    misplaced_objects = jsonfile["pgmap"]["misplaced_objects"]
except KeyError:
    misplaced_objects = 0

try:
    misplaced_total = jsonfile["pgmap"]["misplaced_total"]
except KeyError:
    misplaced_total = 0

try:
    misplaced_ratio = jsonfile["pgmap"]["misplaced_ratio"]
except KeyError:
    misplaced_ratio = 0

#Ceph_Recovery
try:
    recovering_objects_per_sec = jsonfile["pgmap"]["recovering_objects_per_sec"]
except KeyError:
    recovering_objects_per_sec = 0

try:
    recovering_bytes_per_sec = jsonfile["pgmap"]["recovering_bytes_per_sec"]
except KeyError:
    recovering_bytes_per_sec = 0

try:
    recovering_keys_per_sec = jsonfile["pgmap"]["recovering_keys_per_sec"]
except KeyError:
    recovering_keys_per_sec = 0

recovering_mb_sec = float(recovering_bytes_per_sec)/(2**20)

print "0 Ceph_Recovery recovering_mb_sec={0:.2f}|recovering_objects_per_sec={1}|recovering_keys_per_sec={2} Recovery IO: {0:.2f} MiB/s | Objects/s: {1} | Keys/s: {2}".format(recovering_mb_sec, recovering_objects_per_sec, recovering_keys_per_sec)

#Ceph_Stats
try:
    read_bytes_sec = jsonfile["pgmap"]["read_bytes_sec"]
except KeyError:
    read_bytes_sec = 0

try:
    write_bytes_sec  = jsonfile["pgmap"]["write_bytes_sec"]
except KeyError:
    write_bytes_sec = 0

try:
    read_op_per_sec  = jsonfile["pgmap"]["read_op_per_sec"]
except KeyError:
    read_op_per_sec = 0

try:
    write_op_per_sec  = jsonfile["pgmap"]["write_op_per_sec"]
except KeyError:
    write_op_per_sec = 0

read_mb_sec = float(read_bytes_sec)/(2**20)
write_mb_sec = float(write_bytes_sec)/(2**20)

print "0 Ceph_Stats read_mb_sec={0:.2f}|write_mb_sec={1:.2f}|read_op_per_sec={2}|write_op_per_sec={3} Client IO/read: {0:.2f} MiB/s | Client IO/write: {1:.2f} MiB/s | OP/s Read: {2} | OP/s Write: {3}".format(read_mb_sec, write_mb_sec, read_op_per_sec, write_op_per_sec)

#Ceph_Scrubbing

#Ceph_Health

# Create new checks Ceph_Misplaced and Ceph_Degraded, or just include them into Ceph_Health?
# Old outputs
#echo "$healthstatus Ceph_Health - $STATE"
#echo "0 Ceph_Scrubbing deep_scrub=$deep_scrub|scrubbing=$scrub $scrubbing_info"
