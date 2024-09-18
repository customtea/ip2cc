import ipaddress
import typing
import csv

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


def bit_seq_lsb(n: int):
    for i in range(n.bit_length()):
        bit = (n >> i) & 1
        yield bit

def bit_seq_msb(n: int):
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
        self.root = TrieNode()

    def insert(self, network: typing.Union[ipaddress.IPv4Network, ipaddress.IPv6Network]):
        node = self.root
        for bit in bit_seq_msb(int(network.network_address)):
            # print(bit, end="")
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        # node.is_end_of_range = True

    def insert_rir(self, network, cidr, cc):
        node = self.root
        bits = list(bit_seq_msb(int(network.network_address)))
        for idx in range(cidr):
            bit = bits[idx]
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.is_end_of_range = True
        node.country_code = cc

    def search(self, ip):
        node = self.root
        for bit in bit_seq_msb(int(ip)):
            if bit not in node.children:
                return False
            node = node.children[bit]
        # return node.is_end_of_range
        return node.country_code


def main():
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

    # 検索対象のIPアドレス
    search_ip = ipaddress.ip_address('165.242.93.20')
    # apnic,JP,ipv4,165.242.0.0,65536,19931004,allocated

    print(ip_trie.search(search_ip))


if __name__ == '__main__':
    main()
