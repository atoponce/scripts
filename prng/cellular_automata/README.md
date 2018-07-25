# Single Cellular Automata as a PRNG
These aren't high-quality PRNGs, never mind secure (despite what Stephen
Wolfram claims back in the '80s), but they are interesting in and of
themselves, and are worth study in their own right.

There are 256 rules, and their boolean forms are as follows, with "p" as the
left cell, "q" as the middle cell, and "r" as the right cell, following
standard conventions.

Both the [boolean logic](http://atlas.wolfram.com/01/01/views/172/TableView.html)
and [algeraic logic](http://atlas.wolfram.com/01/01/views/173/TableView.html)
sourced and converted from Wolfram Atlas. The rendered Markdown should be able
to be cleanly copied and pasted.

| Rule     | Boolean             | Alegbraic (mod 2)          | Rule     | Boolean                | Alegbraic (mod 2)            |
|----------|---------------------|----------------------------|----------|------------------------|------------------------------|
| 0        | 0                   | 0                          | 128      | p&q&r                  | p\*q\*r                      |
| 1        | ~(p\|q\|r)          | (1+p)\*(1+q)\*(1+r)        | 129      | ~((p^q)\|(p^r))        | 1+p+q+p\*q+r+p\*r+q\*r       |
| 2        | ~p&~q&r             | (1+p)\*(1+q)\*r            | 130      | (p^q^r)&r              | (1+p+q)\*r                   |
| 3        | ~(p\|q)             | (1+p)\*(1+q)               | 131      | p^(p&q&~r)^~q          | 1+p+q+p\*q+p\*q\*r           |
| 4        | (~(p\|r))&q         | (1+p)\*q\*(1+r)            | 132      | (p^q^r)&q              | q\*(1+p+r)                   |
| 5        | ~(p\|r)             | (1+p)\*(1+r)               | 133      | p^(p&~q&r)^~r          | 1+p+r+p\*r+p\*q\*r           |
| 6        | ~p&(q^r)            | (1+p)\*(q+r)               | 134      | (p&(q\|r))^q^r         | q+p\*q+r+p\*r+p\*q\*r        |
| 7        | ~(p\|(q&r))         | (1+p)\*(1+q\*r)            | 135      | ~p^(q&r)               | 1+p+q\*r                     |
| 8        | ~p&q&r              | (1+p)\*q\*r                | 136      | q&r                    | q\*r                         |
| 9        | ~(p\|(q^r))         | (1+p)\*(1+q+r)             | 137      | (~p\|q\|r)^q^r         | 1+p+q+p\*q+r+p\*r+p\*q\*r    |
| 10       | ~p&r                | (1+p)\*r                   | 138      | (p&~q&r)^r             | (1+p+p\*q)\*r                |
| 11       | p^(p\|~q\|r)        | (1+p)\*(1+q+q\*r)          | 139      | ~((p\|q)^(q&r)         | 1+p+q+p\*q+q\*r              |
| 12       | (p&q)^q             | (1+p)\*q                   | 140      | (~p\|r)&q              | q\*(1+p+p\*r)                |
| 13       | p^(p\|q\|~r)        | (1+p)\*(1+r+q\*r)          | 141      | p^((p^q)\|~r)          | 1+p+r+p\*r+q\*r              |
| 14       | p^(p\|q\|r)         | (1+p)\*(q+r+q\*r)          | 142      | p^((p^q)\|(p^r))       | q+p\*q+r+p\*r+q\*r           |
| 15       | ~p                  | (1+p)                      | 143      | ~p\|(q&r)              | 1+p+p\*q\*r                  |
| 16       | p&~q&~r             | p\*(1+q)\*(1+r)            | 144      | p&(p^q^r)              | p\*(1+q+r)                   |
| 17       | ~(q\|r)             | (1+q)\*(1+r)               | 145      | (~p&q&r)^q^~r          | 1+q+r+q\*r+p\*q\*r           |
| 18       | (p^q^r)&~q          | (1+q)\*(p+r)               | 146      | p^((p\|r)&q)^r         | p+p\*qr+q\*r+p\*q\*r         |
| 19       | ~((p&r)\|q)         | (1+q)\*(1+p\*r)            | 147      | (p&r)^~q               | 1+q+p\*r                     |
| 20       | (p^q)&~r            | (p+q)\*(1+r)               | 148      | p^((p\|q)&r)^q         | p+q+p\*r+q\*r+p\*q\*r        |
| 21       | ~((p&q)\|r)         | (1+p\*q)\*(1+r)            | 149      | (p&q)^~r               | 1+p\*q+r                     |
| 22       | p^(p&q&r)^q^r       | p+q+r+p\*q\*r              | 150      | p^q^r                  | p+q+r                        |
| 23       | p^((p^~q)\|(q^r))   | 1+p\*q+p\*r+q\*r           | 151      | p^(~(p\|q\|r)^q^r      | 1+p\*q+p\*r+q\*r+p\*q\*r     |
| 24       | (p^q)&(p^r)         | p+p\*q+p\*r+q\*r           | 152      | (p\|q\|r)^q^r          | p+p\*q+p\*r+q\*r+p\*q\*r     |
| 25       | (p&q&r)^q^~r        | 1+q+r+p\*q\*r              | 153      | q^~r                   | 1+q+r                        |
| 26       | p^((p&q)\|r)        | p+p\*q+r+p\*q\*r           | 154      | p^(p&q)^r              | p+p\*q+r                     |
| 27       | p^((p^~q)\|r)       | 1+q+p\*r+q\*r              | 155      | (p\|q\|~r)^q^r         | 1+q+p\*r+q\*r+p\*q\*r        |
| 28       | p^((p&r)\|q)        | p+q+p\*r+p\*q\*r           | 156      | p^(p&r)^q              | p+q+p\*r                     |
| 29       | p^((p^~r)\|q)       | 1+p\*q+r+q\*r              | 157      | (p\|~q\|r)^q^r         | 1+p\*q+r+q\*r+p\*q\*r        |
| 30       | p^(q\|r)            | p+q+r+q\*r                 | 158      | (p^q^r)\|(q&r)         | p+q+r+q\*r+p\*q\*r           |
| 31       | ~(p&(q\|r))         | 1+p\*q+p\*r+p\*q\*r        | 159      | ~(p&(q^r))             | 1+p\*q+p\*r                  |
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**        |
| 32       | p&~q&r              | p\*(1+q)\*r                | 160      | p&r                    | p\*r                         |
| 33       | !((p^q^r)\|q)       | (1+q)\*(1+p+r)             | 161      | p^(p\|~q\|r)^r         | 1+p+q+p\*q+r+q\*r+p\*q\*r    |
| 34       | ~q&r                | (1+q)\*r                   | 162      | (p\|~q)&r              | (1+q+p\*q)\*r                |
| 35       | (~p\|q\|r)^q        | (1+q)\*(1+p+p\*r)          | 163      | (~p\|(q^r))^q          | 1+p+q+p\*q+p\*r              |
| 36       | (p^q)&(q^r)         | q+p\*q+p\*r+q\*r           | 164      | p^(p\|q\|r)^r          | q+p\*q+p\*+q\*r+p\*q\*r      |
| 37       | p^(p\|q\|r)^~r      | 1+p+r+p\*q\*r              | 165      | p^~r                   | 1+p+r                        |
| 38       | ((p&q)\|r)^q        | q+p\*q+r+p\*q\*r           | 166      | (p&q)^q^r              | q+p\*+r                      |
| 39       | ((p^~q)\|r)^q       | 1+p+p\*r+q\*r              | 167      | p^(p\|q\|~r)^r         | 1+p+p\*r+q\*r+p\*q\*r        |
| 40       | (p^q)&r             | (p+q)\*r                   | 168      | (p\|q)&r               | (p+q+p\*q)\*r                |
| 41       | ~((p&q)\|(p^q^r))   | 1+p+q+p\*q+r+p\*q\*r       | 169      | (~(p\|q))^r            | 1+p+q+p\*q+r                 |
| 42       | (p&q&r)^r           | (1+p\*q)\*r                | 170      | r                      | r                            |
| 43       | p^((p^r)\|(p^~q))   | 1+p+q+p\*q+p\*r+q\*r       | 171      | (~(p\|q))\|r           | 1+p+q+p\*q+p\*r+q\*r+p\*q\*r |
| 44       | (p&(q\|r))^q        | q+p\*q+p\*r+p\*q\*r        | 172      | (p&(q^r))^q            | q+p\*q+p\*r                  |
| 45       | p^(q\|~r)           | 1+p+r+q\*r                 | 173      | (p^~r)\|(q&r)          | 1+p+r+q\*r+p\*q\*r           |
| 46       | (p&q)^(q\|r)        | q+p\*q+r+q\*r              | 174      | ((p&q)^q)\|r           | q+p\*q+r+q\*r+p\*q\*r        |
| 47       | ~p\|(~q&r)          | 1+p+p\*r+p\*q\*r           | 175      | ~p\|r                  | 1+p+p\*r                     |
| 48       | p&~q                | p\*(1+q)                   | 176      | p&(~q\|r)              | p\*(1+q+q\*r)                |
| 49       | (p\|q\|~r)^q        | (1+q)\*(1+r+p\*r)          | 177      | p^(~((p^q)\|r))        | 1+q+r+p\*r+q\*r              |
| 50       | (p\|q\|r)^q         | (1+q)\*(p+r+p\*r)          | 178      | ((p^q)\|(p^r))^q       | p+p\*q+r+p\*r+q\*r           |
| 51       | ~q                  | 1+q                        | 179      | (p&r)\|~q              | 1+q+p\*q\*r                  |
| 52       | (p\|(q&r))^q        | p+q+q\*r+p\*q\*r           | 180      | p^q^(q&r)              | p+q+q\*r                     |
| 53       | (p\|(q^~r))^q       | 1+p\*q+r+p\*r              | 181      | p^(~p\|q\|r)^r         | 1+p\*q+r+p\*r+p\*q\*r        |
| 54       | (p\|r)^q            | p+q+r+p\*r                 | 182      | (p&r)\|(p^q^r)         | p+q+r+p\*r+p\*q\*r           |
| 55       | ~((p\|r)&q)         | 1+p\*q+q\*r+p\*q\*r        | 183      | (p^q^r)\|~q            | 1+p\*q+q\*r                  |
| 56       | p^((p\|r)&q)        | p+p\*q+q\*r+p\*q\*r        | 184      | p^(p&q)^(q&r)          | p+p\*q+q\*r                  |
| 57       | (p\|~r)^q           | 1+q+r+p\*r                 | 185      | (p&r)\|(q^~r)          | 1+q+r+p\*r+p\*q\*r           |
| 58       | (p\|(q^r))^q        | p+p\*q+r+p\*r              | 186      | (p&~q)\|r              | p+p\*q+r+p\*r+p\*q\*r        |
| 59       | (~p&r)\|~q          | 1+q+q\*r+p\*q\*r           | 187      | ~q\|r                  | 1+q+q\*r                     |
| 60       | p^q                 | p+q                        | 188      | p^(p&q&r)^q            | p+q+p\*q\*r                  |
| 61       | p^(p\|q\|r)^~q      | 1+p\*q+r+p\*r+q\*r+p\*q\*r | 189      | (p^q)\|(p^~r)          | 1+p\*q+r+p\*r+q\*r           |
| 62       | (p&q)^(p\|q\|r)     | p+q+r+p\*r+q\*r+p\*q\*r    | 190      | (p^q)\|r               | p+q+r+p\*r+q\*r              |
| 63       | ~(p&q)              | 1+p\*q                     | 191      | ~p\|~q\|r              | 1+p\*q+p\*q\*r               |
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**        |
| 64       | p&q&~r              | p\*q\*(1+r)                | 192      | p&q                    | p\*q                         |
| 65       | ~((p^q)\|r)         | (1+p+q)\*(1+r)             | 193      | p^(p\|q\|~r)^q         | 1+p+q+r+p\*r+q\*r+p\*q\*r    |
| 66       | (p^r)&(q^r)         | p\*q+r+p\*r+q\*r           | 194      | p^(p\|q\|r)^q          | p\*q+r+p\*r+q\*r+p\*q\*r     |
| 67       | p^(p&q&r)^~q        | 1+p+q+p\*q\*r              | 195      | p^~q                   | 1+p+q                        |
| 68       | q&~r                | q\*(1+r)                   | 196      | (p\|~r)&q              | q\*(1+r+p\*r)                |
| 69       | (~p\|q\|r)^r        | (1+p+p\*q)\*(1+r)          | 197      | (~(p\|(q^r)))^q        | 1+p+p\*q+r+p\*r              |
| 70       | ((p&r)\|q)^r        | q+r+p\*r+p\*q\*r           | 198      | (p&r)^q^r              | q+r+p\*r                     |
| 71       | ((p^~r)\|q)^r       | 1+p+p\*q+q\*r              | 199      | p^(p\|~q\|r)^q         | 1+p+p\*q+q\*r+p\*q\*r        |
| 72       | (p&q)^(q&r)         | q\*(p+r)                   | 200      | (p\|r)&q               | q\*(p+r+p\*r)                |
| 73       | ~((p&r)\|(p^q^r))   | 1+p+q+r+p\*r+p\*q\*r       | 201      | (~(q\|r))^q            | 1+p+q+r+p\*r                 |
| 74       | (p&(q\|r))^r        | p\*q+r+p\*r+p\*q\*r        | 202      | (p&(q^r))^r            | p\*q+r+p\*r                  |
| 75       | (p^(~q\|r)          | 1+p+q+q\*r                 | 203      | (p^~q)\|(q&r)          | 1+p+q+q\*r+p\*q\*r           |
| 76       | (p&q&r)^q           | q\*(1+p\*r)                | 204      | q                      | q                            |
| 77       | p^((p^q)\|(p^~r))   | 1+p+p\*q+r+p\*r+q\*r       | 205      | (~(p\|r))\|q           | 1+p+p\*q+r+p\*r+q\*r+p\*q\*r |
| 78       | p^((p^q)\|r)        | q+r+p\*r+q\*r              | 206      | (~p&r)\|q              | q+r+p\*r+q\*r+p\*q\*r        |
| 79       | ~p\|(q&~r)          | 1+p+p\*q+p\*q\*r           | 207      | ~(p&~q)                | 1+p+p\*q                     |
| 80       | p&~r                | p\*(1+r)                   | 208      | p&(q\|~r)              | p\*(1+r+q\*r)                |
| 81       | (p\|~q\|r)^r        | (1+q+p\*q)\*(1+r)          | 209      | ~((p&q)^(q\|r))        | 1+q+p\*q+r+q\*r              |
| 82       | (p\|(q&r))^r        | p+r+q\*r+p\*q\*r           | 210      | p^(q&r)^r              | p+r+q\*r                     |
| 83       | (p\|(q^~r))^r       | 1+q+p\*q+p\*r              | 211      | p^(~p\|q\|r)^q         | 1+q+p\*q+p\*r+p\*q\*r        |
| 84       | (p\|q\|r)^r         | (p+q+p\*q)\*(1+r)          | 212      | ((p^q)\|(p^r))^r       | p+q+p\*q+p\*r+q\*r           |
| 85       | ~r                  | 1+r                        | 213      | (p&q)\|~r              | 1+r+p\*q\*r                  |
| 86       | (p\|q)^r            | p+q+p\*q+r                 | 214      | (p&q)\|(p^q^r)         | p+q+p\*q+r+p\*q\*r           |
| 87       | ~((p\|q)&r)         | 1+p\*r+q\*r+p\*q\*r        | 215      | ~((p^q)&r)             | 1+p\*r+q\*r                  |
| 88       | p^((p\|q)&r)        | p+p\*r+q\*r+p\*q\*r        | 216      | p^((p^q)&r)            | p+p\*r+q\*r                  |
| 89       | (p\|~q)^r           | 1+q+p\*q+r                 | 217      | (p&q)\|(q^~r)          | 1+q+p\*q+r+p\*q\*r           |
| 90       | p^r                 | p+r                        | 218      | p^(p&q&r)^r            | p+r+p\*q\*r                  |
| 91       | p^(~(p\|q\|r))^r    | 1+q+p\*q+p\*r+q\*r+p\*q\*r | 219      | (p^r)\|(p^~q)          | 1+q+p\*q+p\*r+q\*r           |
| 92       | (p\|(q^r))^r        | p+q+p\*q+p\*r              | 220      | (p&~r)\|q              | p+q+p\*q+p\*r+p\*q\*r        |
| 93       | ~((p\|~q)&r)        | 1+r+q\*r+p\*q\*r           | 221      | q\|~r                  | 1+r+q\*r                     |
| 94       | (p&r)^(p\|q\|r)     | p+q+p\*q+r+q\*r+p\*q\*r    | 222      | (p^q^r)\|q             | p+q+p\*q+r+q\*r              |
| 95       | ~(p&r)              | 1+p\*r                     | 223      | ~(p&~q&r)              | 1+p\*r+p\*q\*r               |
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**        |
| 96       | p&(q^r)             | p\*(q+r)                   | 224      | p&(q\|r)               | p\*(q+r+q\*r)                |
| 97       | ~((p^q^r)\|(q&r))   | 1+p+q+r+q\*r+p\*q\*r       | 225      | p^(~(q\|r))            | 1+p+q+r+q\*r                 |
| 98       | ((p\|r)&q)^r        | p\*q+r+q\*r+p\*q\*r        | 226      | (p&q)^(q&r)^r          | p\*q+r+q\*r                  |
| 99       | (~p\|r)^q           | 1+p+q+p\*r                 | 227      | (p&r)\|(p^~q)          | 1+p+q+p\*r+p\*q\*r           |
| 100      | ((p|\q)&r)^q        | q+p\*r+q\*r+p\*q\*r        | 228      | ((p^q)&r)^q            | q+p\*r+q\*r                  |
| 101      | p^(p&q)^~r          | 1+p+p\*q+r                 | 229      | (p&q)\|(p^~r)          | 1+p+p\*q+r+p\*q\*r           |
| 102      | q^r                 | q+r                        | 230      | (p&q&r)^q^r            | q+r+p\*q\*r                  |
| 103      | ~(p\|q\|r)^q^r      | 1+p+p\*q+p\*r+q\*r+p\*q\*r | 231      | (p^~q)\|(q^r)          | 1+p+p\*q+p\*r+q\*r           |
| 104      | p^(p\|q\|r)^q^r     | p\*q+p\*r+q\*r+p\*q\*r     | 232      | (p&q)\|((p\|q)&r)      | p\*q+p\*r+q\*r               |
| 105      | p^q^~r              | 1+p+q+r                    | 233      | p^(p&q&r)^q^~r         | 1+p+q+r+p\*q\*r              |
| 106      | (p&q)^r             | p\*q+r                     | 234      | (p&q)\|r               | p\*q+r+p\*q\*r               |
| 107      | p^(p\|q\|~r)^q^r    | 1+p+q+p\*r+q\*r+p\*q\*r    | 235      | (p^~q)\|r              | 1+p+q+p\*r+q\*r              |
| 108      | (p&r)^q             | q+p\*r                     | 236      | (p&r)\|q               | q+p\*r+p\*q\*r               |
| 109      | p^(p\|~q\|r)^q^r    | 1+p+p\*q+r+q\*r+p\*q\*r    | 237      | (p^~r)\|q              | 1+p+p\*q+r+q\*r              |
| 110      | (~p&q&r)^q^r        | q+r+q\*r+p\*q\*r           | 238      | q\|r                   | q+r-q\*r                     |
| 111      | ~p\|(q^r)           | 1+p+p\*q+p\*r              | 239      | ~p\|q\|r               | 1+p+p\*q+p\*r+p\*q\*r        |
| 112      | p^(p&q&r)           | p\*(1+q\*r)                | 240      | p                      | p                            |
| 113      | p^(~((p^q)\|(p^r))) | 1+q+p\*q+r+p\*r+q\*r       | 241      | p\|(~(q\|r))           | 1+q+p\*q+r+p\*r+q\*r+p\*q\*r |
| 114      | ((p^q)\|r)^q        | p+r+p\*r+q\*r              | 242      | p\|(~q&r)              | p+r+p\*r+q\*r+p\*q\*r        |
| 115      | (p&~r)\|~q          | 1+q+p\*q+p\*q\*r           | 243      | p\|~q                  | 1+q+p\*q                     |
| 116      | (p\|q)^(q&r)        | p+q+p\*q+q\*r              | 244      | p\|(q&~r)              | p+q+p\*q+q\*r+p\*\*r         |
| 117      | (p&~q)\|~r          | 1+r+p\*r+p\*q\*r           | 245      | p\|~r                  | 1+r+p\*r                     |
| 118      | (p\|q\|r)^(q&r)     | p+q+p\*q+r+p\*r+p\*q\*r    | 246      | p\|(q^r)               | p+q+p\*q+r+p\*r              |
| 119      | ~(q&r)              | 1+q\*r                     | 247      | p\|~q\|~r              | 1+q\*r+p\*q\*r               |
| 120      | p^(q&r)             | p+q\*r                     | 248      | p\|(q&r)               | p+q\*r+p\*q\*r               |
| 121      | p^(~p\|q\|r)^q^r    | 1+q+p\*q+r+p\*r+p\*q\*r    | 249      | p\|(q^~r)              | 1+q+p\*q+r+p\*r              |
| 122      | p^(p&~q&r)^r        | p+r+p\*r+p\*q\*r           | 250      | p|\r                   | p+r-p\*r                     |
| 123      | ~((p^q^r)&q)        | 1+q+p\*q+q\*r              | 251      | p\|~q\|r               | 1+q+p\*q+q\*r+p\*q\*r        |
| 124      | p^(p&q&~r)^q        | p+q+p\*q+p\*q\*r           | 252      | p\|q                   | p+q-p\*q                     |
| 125      | (p^q)\|~r           | 1+r+p\*r+q\*r              | 253      | p\|q\|~r               | 1+r+p\*r+q\*r+p\*q\*r        |
| 126      | (p^q)\|(p^r)        | p+q+p\*q+r+p\*r+q\*r       | 254      | p\|q\|r                | q+p\*(-1+q)\*(-1+r)+r-q\*r   |
| 127      | ~(p&q&r)            | 1+p\*q\*r                  | 255      | 1                      | 1                            |
