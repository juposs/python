#!/usr/bin/python
#from myutil import file
import json
import os

#file1 = file("../to-be_converted/sample-outputs/ceph-s.json")
#data = file1.read()

data = os.popen("ceph -s -f json-pretty").read()
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

print "P Ceph_Space TB_used={0:.2f}|Percent_used={1:.2f};{2};{3} Currently {1:.2f}%% used ({0:.2f} TiB of {4:.2f} TiB)".format(tb_used,perc_used,space_warn,space_crit,tb_total)

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

print "0 Ceph_Recovery recovering_mb_sec={0:.2f}|recovering_objects_per_sec={1}|recovering_keys_per_sec={2}|misplaced_objects={3}|misplaced_ratio={4}|degraded_objects={5}|degraded_ratio={6} Recovery IO: {0:.2f} MiB/s | Objects/s: {1} | Keys/s: {2} | Misplaced objects: {3}; ratio: {4:.2f}% | Degraded objects: {5}; ratio: {6:.2f}%".format(recovering_mb_sec, recovering_objects_per_sec, recovering_keys_per_sec, misplaced_objects, misplaced_ratio, degraded_objects, degraded_ratio)

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
for each in jsonfile["pgmap"]["pgs_by_state"]:
    if each["state_name"] == "active+clean+scrubbing+deep":
        deep_scrubbing_pg = each["count"]
    else:
        deep_scrubbing_pg = 0

for each in jsonfile["pgmap"]["pgs_by_state"]:
    if each["state_name"] == "active+clean+scrubbing":
        scrubbing_pg = each["count"]
    else:
        scrubbing_pg = 0

print "0 Ceph_Scrubbing deep_scrubbing_pg={0}|scrubbing_pg={1} Number of deep scrubbing PGs: {0} | Number of scubbing PGs: {1}".format(deep_scrubbing_pg, scrubbing_pg)

# OSDs
num_osds = jsonfile["osdmap"]["osdmap"]["num_osds"]
num_up_osds = jsonfile["osdmap"]["osdmap"]["num_up_osds"]
num_in_osds = jsonfile["osdmap"]["osdmap"]["num_in_osds"]
full_osds = jsonfile["osdmap"]["osdmap"]["full"] # true/false?
nearfull_osds = jsonfile["osdmap"]["osdmap"]["nearfull"] # true/false?


#Ceph_Health
pgstates = "PGs by state: "
for dic in jsonfile["pgmap"]["pgs_by_state"]:
    pgstates = pgstates + "{0}: {1} | ".format(dic["state_name"], dic["count"])

try:
    health_status = jsonfile["health"]["status"]
except KeyError:
    health_status = jsonfile["health"]["overall_status"]

try:
    health_summary = jsonfile["helath"]["summary"]
except KeyError:
    health_summary = []

health_summary_parsed = ""
if len(health_summary) < 1:
    health_summary_parsed = "OK "
else:
    for each in health_summary:
        health_summary_parsed = health_summary_parsed + "{0}: {1} | ".format(each["severity"], each["summary"])

if health_status != "HEALTH_OK" or int(num_osds) != int(num_up_osds) or int(num_osds) != int(num_in_osds):
        status = 2
else:
        status = 0

print "{0} Ceph_Health num_osds={1}|num_up_osds={2}|num_in_osds={3} Health-summary: {4}| {5}".format(status, num_osds, num_up_osds, num_in_osds, health_summary_parsed, pgstates)
