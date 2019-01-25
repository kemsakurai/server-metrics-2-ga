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
                data = event('network-' + net_dev.get('iface'), 'rxkB', net_dev.get('rxkB'), 0, cd1=default_dash_dt)
                report(args.property, cid, data)
                data = event('network-' + net_dev.get('iface'), 'txkB', net_dev.get('txkB'), 0, cd1=default_dash_dt)
                report(args.property, cid, data)

def send_filesystem(default_dash_dt, args, cid):
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        data = event('filesystem-' + partition.device, 'total', usage.total / 1024 / 1024, 0,  cd1=default_dash_dt)
        report(args.property, cid, data)
        data = event('filesystem-' + partition.device, 'used', usage.used / 1024 / 1024, 0,  cd1=default_dash_dt)
        report(args.property, cid, data)

def send_io(dt_str, default_dash_dt, args, cid):
    result = subprocess.getoutput('sadf -T -s ' + dt_str + ' -j -- -b')
    if "sadf: command not found" not in result:
        json_o = json.loads(result)
        statistics = json_o.get('sysstat').get('hosts')[-1].get('statistics')
        if statistics:
            io = statistics[-1].get("io")
            rtps = io.get("io-reads").get("rtps")
            data = event('io', 'rtps', rtps, 0,  cd1=default_dash_dt)
            report(args.property, cid, data)
            wtps = io.get("io-writes").get("wtps")
            data = event('io', 'wtps', wtps, 0,  cd1=default_dash_dt)
            report(args.property, cid, data)

def send_memory(default_dash_dt, args, cid):
    mem = psutil.virtual_memory()

    total_mb = mem.total / 1024 / 1024
    data = event('memory','total',total_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

    used_mb = mem.used / 1024 / 1024
    data = event('memory','used',used_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

    available_mb = mem.available / 1024 / 1024
    data = event('memory','available',available_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

    swap = psutil.swap_memory()
    total_mb = swap.total / 1024 / 1024
    data = event('swap','total',total_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

    used_mb = swap.used / 1024 / 1024
    data = event('swap','used',used_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

    free_mb = swap.free / 1024 / 1024
    data = event('swap','free',free_mb, 0,  cd1=default_dash_dt)
    report(args.property, cid, data)

def send_cpu(dt_str, default_dash_dt, args, cid):
    result = subprocess.getoutput('sadf -T -s ' + dt_str + ' -j -- -u')
    if "sadf: command not found" not in result:
        json_o = json.loads(result)
        statistics = json_o.get('sysstat').get('hosts')[-1].get('statistics')
        if statistics:
            cpu_loads = statistics[-1].get("cpu-load")
            for cpu_load in cpu_loads:
                user = cpu_load.get("user") * 100 
                data = event('cpu-' + cpu_load.get("cpu"), 'user', user, 0, cd1=default_dash_dt)
                report(args.property, cid, data)
                system = cpu_load.get("system") * 100 
                data = event('cpu-' + cpu_load.get("cpu"), 'system', system, 0, cd1=default_dash_dt)
                report(args.property, cid, data)
                iowait = cpu_load.get("iowait") * 100
                data = event('cpu-' + cpu_load.get("cpu") , 'iowait', iowait, 0,  cd1=default_dash_dt)
                report(args.property, cid, data)

def send_loadavg(default_dash_dt, args, cid):
    # --------------------------
    # loadavg
    loadavg1, loadavg5, loadavg15 = os.getloadavg()
    data = event('loadavg', 'loadavg1', loadavg1, 0, cd1=default_dash_dt)
    report(args.property, cid, data)
    data = event('loadavg','loadavg5',loadavg5, 0, cd1=default_dash_dt)
    report(args.property, cid, data)
    data = event('loadavg','loadavg15',loadavg15, 0, cd1=default_dash_dt)
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
