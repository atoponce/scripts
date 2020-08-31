#!/usr/bin/python3

import secrets

dice = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","W","X","Y","Z"]
i = 25
tmp = ""
pw = ""

while i > 1:
    i -= 1
    j = secrets.randbelow(i)
    dice[j], dice[i] = dice[i], dice[j]

for i in range(25):
    tmp = dice[i]
    tmp += str(secrets.randbelow(6) + 1)
    tmp += secrets.choice("NESW")
    tmp += " "
    pw += tmp

print(pw)
