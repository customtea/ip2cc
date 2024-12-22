import csv


filenames = [ "./afrinic.csv", "./apnic.csv", "./arin.csv", "./lacnic.csv", "./ripe-ncc.csv" ]

outfile = open("./ipcc.csv", "w", newline="")
cw = csv.writer(outfile)

for file in filenames:
    with open(file) as f:
        cr = csv.reader(f, delimiter="|")
        
        for l in cr:
            # print(l)
            if "#" in l[0]:
                continue
            if "*" in l[1]:
                continue
            if l[2] == "ipv4":
                cw.writerow(l)
