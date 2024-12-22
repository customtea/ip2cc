import ipaddress
import typing
import csv
import json

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


def bit_seq_lsb(n: int, len=None):
    if len is None:
        len = n.bit_length()
    for i in range(len):
        bit = (n >> i) & 1
        yield bit

def bit_seq_msb(n: int, len=None):
    if len is None:
        len = n.bit_length()
    for i in range(n.bit_length()-1,-1,-1):
        bit = (n >> i) & 1
        yield bit

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_range = False
        self.country_code = ""

class IPRangeTrie:
    def __init__(self):
        self.root = {"node": {}}
    
    def load(self, filename):
        with open(filename) as f:
            self.root = json.load(f)

    def insert_rir(self, network: ipaddress.IPv4Network, cidr, cc):
        node = self.root
        bits = list(bit_seq_msb(int(network.network_address), len=network.max_prefixlen))
        for idx in range(cidr):
            bit = bits[idx]
            if bit not in node["node"]:
                node["node"][bit] = {"node":{}}
            node = node["node"][bit]
        node["cc"] = cc
        node["cidr"] = cidr
        node["ip"] = network.exploded

    def search_cc(self, ip):
        node = self.root
        for bit in bit_seq_msb(int(ip)):
            sbit = str(bit)
            if "cc" in node:
                return node["cc"]
            if sbit not in node["node"]:
                return False
            node = node["node"][sbit]
        return node["cc"]

def create_table():
    ip_trie = IPRangeTrie()
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
        ip_trie.insert_rir(ip, cidr, cc)
    incsv.close()

    with open("ipcc.json", "w") as f:
        json.dump(ip_trie.root, f)

def main():
    ip_trie = IPRangeTrie()
    ip_trie.load("./ipcc.json")

    search_ip = ipaddress.ip_address('165.242.93.20')
    # apnic,JP,ipv4,165.242.0.0,65536,19931004,allocated

    print(ip_trie.search_cc(search_ip))


if __name__ == '__main__':
    create_table()
    main()
