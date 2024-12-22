import requests
import time

rir_table = {
"arin":"https://ftp.apnic.net/stats/arin/delegated-arin-extended-latest",
"ripe-ncc":"https://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest",
"apnic":"https://ftp.apnic.net/stats/apnic/delegated-apnic-latest",
"lacnic":"https://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest",
"afrinic":"https://ftp.apnic.net/stats/afrinic/delegated-afrinic-latest",
}

for rir, url in rir_table.items():
    r = requests.get(url)
    with open(f"{rir}.csv", "w") as f:
        f.write(r.content.decode("utf8"))
    time.sleep(1)

