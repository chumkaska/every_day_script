import random

g = ("R" + "".join(random.sample("01234567890"*2, 3)) + "".join(random.sample("ABCDEFGHJKLMNOPQRSTUVWXYZ"*2, 4)) + " " for i in range(10))
#print("\n".join(g))
sn = open("seriiniki.txt", "a")
sn.write("\n".join(g))
