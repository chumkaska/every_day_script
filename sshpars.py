f = open("ssh.log")
lines = f.readlines()
f.close()
d = list()


for line in lines:
    part = line.split()[2]
    date = line.split() [:2]
    date = "".join(date)
    allstring = line.split() [10]
    #allstring = "".join(allstring)
    texts = line.split()[5]
    fail = 'Failed'
    if texts == fail:
        print(fail + " " + part + " " + date + " " + allstring)







#print(part, fail)