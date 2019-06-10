#!/usr/bin/python
from myutil import file
import json

file1 = file("../to-be_converted/sample-outputs/ceph-s.json")
data = file1.read()

jsonfile = json.loads(data)

#Ceph_Space
data_bytes = jsonfile["pgmap"]["data_bytes"]
bytes_total = jsonfile["pgmap"]["bytes_total"]
bytes_avail = jsonfile["pgmap"]["bytes_avail"]
bytes_used  = jsonfile["pgmap"]["bytes_used"]

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

#Ceph_ClientIO
read_bytes_per_sec = jsonfile["pgmap"]["read_bytes_per_sec"]
write_bytes_per_sec  = jsonfile["pgmap"]["write_bytes_per_sec"]
read_op_per_sec  = jsonfile["pgmap"]["read_op_per_sec"]
write_op_per_sec  = jsonfile["pgmap"]["write_op_per_sec"]


print bytes_total
print str(int(bytes_total)/(2**40)), "TB"
