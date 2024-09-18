import json

cctable = {}
with open("./country.tsv") as f:
    for line in f:
        sline = line.split("\t")
        # print(sline)
        jname = sline[0]
        ename = sline[1]
        code = sline[5]
        # print(jname, code)
        if code == "alpha-2":
            continue
        cctable[code] = {"jname":jname, "ename":ename}
        
        with open("./cc.json", "w") as wf:
            json.dump(cctable, wf, indent=4, ensure_ascii=False)
