from datetime import datetime

f = open("log.log", "r")
lines = f.readlines()
f.close()
d = list()

sdatex = '02/Mar/2018'
datex = datetime.strptime(sdatex, '%d/%b/%Y')

for line in lines:
    part =  line.split('"')
    bytesx = part[2].split()[1]
    ip = part[0].split()[0]
    date = line.split("[")[1].split(":")[0]
    time = line.split("[")[1]
    time1 = time.split()[0]
    time2 = time1.split(":")[1:4]
    time2 = ":".join(time2)
    d.append((int(bytesx), ip, date, time2))



res = []
for tup in sorted(d, key=lambda tup: tup[0], reverse=True)[:10]:

     res.append(str(tup[0]) + "\t" + tup[1] + "\t" + tup[2] + "\t" + tup[3])
res = "\n".join(res)
print(res)

f = open("log12.log", "w")
f.write(res)
f.close()