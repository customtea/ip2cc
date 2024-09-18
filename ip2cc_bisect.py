import csv
import ipaddress
import bisect

netmasks = {
    16777216 : 8, 8388608 : 9,
    4194304 : 10, 2097152 : 11,
    1048576 : 12, 524288 : 13,
    262144 : 14, 131072 : 15,
    65536 : 16, 32768 : 17,
    16384 : 18, 8192 : 19,
    4096 : 20, 2048 : 21,
    1024 : 22, 512 : 23,
    256 : 24, 128 : 25,
    64 : 26, 32 : 27,
    16 : 28, 8 : 29,
    4 : 30, 2 : 31,
    1 : 32
}

iplist = []

incsv = open("./ipcc.csv")
cr = csv.reader(incsv)


for line in cr:
    # print(line)
    cc = line[1]
    str_ip = line[3]
    str_mask = line[4]
    cidr = netmasks.get(int(str_mask))
    if cidr is None:
        continue
    # 
    # ip = ipaddress.ip_address(str_ip)
    try:
        ip = ipaddress.ip_network(f"{str_ip}/{cidr}")
    except ValueError:
        continue
    mask = int(str_mask) -1
    iplist.append(int(ip.network_address))
    iplist.append(int(ip.broadcast_address))

ips = sorted(iplist)
left = bisect.bisect_left(ips, int(ipaddress.ip_address("165.242.93.20")))
right = bisect.bisect_right(ips, int(ipaddress.ip_address("165.242.93.20")))

print(ipaddress.ip_address(iplist[left]), ipaddress.ip_address(iplist[right]))

# target_ip = "165.242.93.20"
# csv.reader()

