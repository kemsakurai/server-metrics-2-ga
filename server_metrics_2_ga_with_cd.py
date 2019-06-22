import argparse
import os
import random
import socket    
import uuid
import subprocess
import datetime
import psutil
import datetime 
import json
import subprocess
from google_measurement_protocol import event, report


def send_network(dt_str, default_dash_dt, args, cid):
    result = subprocess.getoutput('sadf -T -s ' + dt_str + ' -j -- -n DEV')
    if "sadf: command not found" not in result:
        json_o = json.loads(result)
        statistics = json_o.get('sysstat').get('hosts')[-1].get('statistics')
        if statistics:
            net_devs = statistics[-1].get("network").get("net-dev")
            for net_dev in net_devs:
                # -----------------
                # cd1:net_dev.get('rxkB')
                # cd2=net_dev.get('txkB')
                data = event('network-' + net_dev.get('iface'), default_dash_dt, None, 0, cd1=net_dev.get('rxkB'),cd2=net_dev.get('txkB'))
                report(args.property, cid, data)

def send_filesystem(default_dash_dt, args, cid):
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        # -------------------------
        # cd1:total
        # cd2:used
        usage = psutil.disk_usage(partition.mountpoint)
        total = usage.total / 1024 / 1024
        used = usage.used / 1024 / 1024
        data = event('filesystem-' + partition.device, default_dash_dt, None, 0,  cd1=total,cd2=used)
        report(args.property, cid, data)

def send_io(dt_str, default_dash_dt, args, cid):
    result = subprocess.getoutput('sadf -T -s ' + dt_str + ' -j -- -b')
    if "sadf: command not found" not in result:
        json_o = json.loads(result)
        statistics = json_o.get('sysstat').get('hosts')[-1].get('statistics')
        if statistics:
            # -------------------------
            # cd1:rtps
            # cd2:wtps
            io = statistics[-1].get("io")
            rtps = io.get("io-reads").get("rtps")
            wtps = io.get("io-writes").get("wtps")
            data = event('io', default_dash_dt, None, 0,  cd1=rtps, cd2=wtps)
            report(args.property, cid, data)

def send_memory(default_dash_dt, args, cid):
    # ----------------------------------------------------
    # send memory
    # cd1:total_mb
    # cd2:used_mb
    # cd3:available_mb
    mem = psutil.virtual_memory()
    total_mb = mem.total / 1024 / 1024
    used_mb = mem.used / 1024 / 1024
    available_mb = mem.available / 1024 / 1024
    data = event('memory',default_dash_dt, None, 0, cd1=total_mb, cd2=used_mb, cd3=available_mb)
    report(args.property, cid, data)

    # ----------------------------------------------------
    # swap memory
    # cd1:total_mb
    # cd2:used_mb
    # cd3:free_mb
    swap = psutil.swap_memory()
    total_mb = swap.total / 1024 / 1024
    used_mb = swap.used / 1024 / 1024
    free_mb = swap.free / 1024 / 1024
    data = event('swap',default_dash_dt, None, 0, cd1=total_mb, cd2=used_mb, cd3=free_mb)
    report(args.property, cid, data)

def send_cpu(dt_str, default_dash_dt, args, cid):
    result = subprocess.getoutput('sadf -T -s ' + dt_str + ' -j -- -u')
    if "sadf: command not found" not in result:
        json_o = json.loads(result)
        statistics = json_o.get('sysstat').get('hosts')[-1].get('statistics')
        if statistics:
            cpu_loads = statistics[-1].get("cpu-load")
            for cpu_load in cpu_loads:
                # -----------------------
                # cd1:user
                # cd2:system
                # cd3:iowait
                user = cpu_load.get("user") * 100 
                system = cpu_load.get("system") * 100 
                iowait = cpu_load.get("iowait") * 100
                data = event('cpu-' + cpu_load.get("cpu") , default_dash_dt, None, 0,  cd1=user,cd2=system, cd3=iowait)
                report(args.property, cid, data)

def send_loadavg(default_dash_dt, args, cid):
    # --------------------------
    # loadavg
    loadavg1, loadavg5, loadavg15 = os.getloadavg()    
    # --------------------------
    # cd1:loadavg1
    # cd2:loadavg5
    # cd3:loadavg15
    data = event('loadavg', default_dash_dt, None, 0, cd1=loadavg1, cd2=loadavg5, cd3=loadavg15)
    report(args.property, cid, data)

def main():
    parser = argparse.ArgumentParser(description="Main Script's argments")
    parser.add_argument("-p", "--property", type=str, required=True, help='Specify properties of Google Analytics.')
    args = parser.parse_args()
    cid = uuid.uuid4()

    dt_now = datetime.datetime.now()
    default_dash_dt = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    dt_now = dt_now - datetime.timedelta(minutes=2) 
    dt_str = dt_now.strftime('%H:%M:%S')

    # --------------------------
    # loadavg
    send_loadavg(default_dash_dt, args, cid)

    # --------------------------
    # cpu
    send_cpu(dt_str, default_dash_dt, args, cid)

    # ------------------------------------------------
    # memory
    send_memory(default_dash_dt, args, cid)

    # ------------------------------------------------
    # io
    send_io(dt_str, default_dash_dt, args, cid)

    # ------------------------------------------------
    # filesystem
    send_filesystem(default_dash_dt, args, cid)

    # ------------------------------------------------
    # network    
    send_network(dt_str, default_dash_dt, args, cid)

if __name__ == "__main__":
    # execute only if run as a script
    main()
