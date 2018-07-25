# Single Cellular Automata as a PRNG
These aren't high-quality PRNGs, never mind secure (despite what Stephen
Wolfram claims back in the '80s), but they are interesting in and of
themselves, and are worth study in their own right.

There are 256 rules, and their boolean forms are as follows, with "p" as the
left cell, "q" as the middle cell, and "r" as the right cell, following
standard conventions.

| Rule     | Boolean             | Alegbraic (mod 2)          | Rule     | Boolean                | Alegbraic (mod 2)         		|
|----------|---------------------|----------------------------|----------|------------------------|---------------------------		|
| 0        | 0                   | 0                          | 128      |                        | p\*q\*r                   		|
| 1        | ~(p\|q\|r)          | (1+p)\*(1+q)\*(1+r)        | 129      |                        | 1+p+q+p\*q+r+p\*r+q\*r    		|
| 2        | ~p&~q&r             | (1+p)\*(1+q)\*r            | 130      |                        | (1+p+q)\*r                		|
| 3        | ~(p\|q)             | (1+p)\*(1+q)               | 131      |                        | 1+p+q+p\*q+p\*q\*r        		|
| 4        | (~(p\|r))&q         | (1+p)\*q\*(1+r)            | 132      |                        | q\*(1+p+r)                		|
| 5        | ~(p\|r)             | (1+p)\*(1+r)               | 133      |                        | 1+p+r+p\*r+p\*q\*r        		|
| 6        | ~p&(q\|r)           | (1+p)\*(q+r)               | 134      |                        | q+p\*q+r+p\*r+p\*q\*r     		|
| 7        | ~(p\|(q&r))         | (1+p)\*(1+q\*r)            | 135      |                        | 1+p+q\*r                  		|
| 8        | ~p&q&r              | (1+p)\*q\*r                | 136      |                        | q\*r                      		|
| 9        | ~(p\|(q^r))         | (1+p)(1+q+r)               | 137      |                        | 1+p+q+p\*q+r+p\*r+p\*q\*r 		|
| 10       | ~p&r                | (1+p)\*r                   | 138      |                        | (1+p+p\*q)\*r             		|
| 11       | p^(p\|~q\|r)        | (1+p)\*(1+q+q\*r)          | 139      |                        | 1+p+q+p\*q+q\*r           		|
| 12       | (p&q)^q             | (1+p)\*q                   | 140      |                        | q\*(1+p+p\*r)             		|
| 13       | p^(p\|q\|~r)        | (1+p)\*(1+r+q\*r)          | 141      |                        | 1+p+r+p\*r+q\*r           		|
| 14       | p^(p\|q\|r)         | (1+p)\*(q+r+q\*r)          | 142      |                        | q+p\*q+r+p\*r+q\*r        		|
| 15       | ~p                  | (1+p)                      | 143      |                        | 1+p+p\*q\*r               		|
| 16       | p&~q&~r             | p\*(1+q)\*(1+r)            | 144      |                        | p\*(1+q+r)                		|
| 17       | ~(q\|r)             | (1+q)\*(1+r)               | 145      |                        | 1+q+r+q\*r+p\*q\*r        		|
| 18       | (p^q^r)&~q          | (1+q)\*(p+r)               | 146      |                        | p+p\*qr+q\*r+p\*q\*r      		|
| 19       | ~((p&r)\|q)         | (1+q)\*(1+p\*r)            | 147      |                        | 1+q+p\*r                  		|
| 20       | (p^q)&~r            | (p+q)\*(1+r)               | 148      |                        | p+q+p\*r+q\*r+p\*q\*r     		|
| 21       | ~((p&q)\|r)         | (1+p\*q)\*(1+r)            | 149      |                        | 1+p\*q+r                  		|
| 22       | p^(p&q&r)^q^r       | p+q+r+p\*q\*r              | 150      |                        | p+q+r                     		|
| 23       | p^((p^~q)\|(q^r))   | 1+p\*q+p\*r+q\*r           | 151      |                        | 1+p\*q+p\*r+q\*r+p\*q\*r  		|
| 24       | (p^q)&(p^r)         | p+p\*q+p\*r+q\*r           | 152      |                        | p+p\*q+p\*r+q\*r+p\*q\*r  		|
| 25       | (p&q&r)^q^~r        | 1+q+r+p\*q\*r              | 153      |                        | 1+q+r                     		|
| 26       | p^((p&q)\|r)        | p+p\*q+r+p\*q\*r           | 154      |                        | p+p\*q+r                  		|
| 27       | p^((p^~q)\|r)       | 1+q+p\*r+q\*r              | 155      |                        | 1+q+p\*r+q\*r+p\*q\*r     		|
| 28       | p^((p&r)\|q)        | p+q+p\*r+p\*q\*r           | 156      |                        | p+q+p\*r                  		|
| 29       | p^((p^~r)\|q)       | 1+p\*q+r+q\*r              | 157      |                        | 1+p\*q+r+q\*r+p\*q\*r     		|
| 30       | p^(q\|r)            | p+q+r+q\*r                 | 158      |                        | p+q+r+q\*r+p\*q\*r        		|
| 31       | ~(p&(q\|r))         | 1+p\*q+p\*r+p\*q\*r        | 159      |                        | 1+p\*q+p\*r               		|
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**     		|
| 32       | p&~q&r              | p\*(1+q)\*r                | 160      |                        | p\*r                      		|
| 33       | !((p^q^r)\|q)       | (1+q)\*(1+p+r)             | 161      |                        | 1+p+q+p\*q+r+q\*r+p\*q\*r 		|
| 34       | ~q&r                | (1+q)\*r                   | 162      |                        | (1+q+p\*q)\*r             		|
| 35       | (~p\|q\|r)^q        | (1+q)\*(1+p+p\*r)          | 163      |                        | 1+p+q+p\*q+p\*r           		|
| 36       | (p^q)&(q^r)         | q+p\*q+p\*r+q\*r           | 164      |                        | q+p\*q+p\*+q\*r+p\*q\*r   		|
| 37       | p^(p\|q\|r)^~r      | 1+q+r+p\*q\*r              | 165      |                        | 1+p+r                     		|
| 38       | ((p&q)\|r)^q        | q+p\*q+r+p\*q\*r           | 166      |                        | q+p\*+r                   		|
| 39       | ((p^~q)\|r)^q       | 1+p+p\*r+q\*r              | 167      |                        | 1+p+p\*r+q\*r+p\*q\*r     		|
| 40       | (p^q)&r             | (p+q)\*r                   | 168      |                        | (p+q+p\*q)\*r             		|
| 41       | ~((p&q)\|(p^q^r))   | 1+p+q+p\*q+r+p\*q\*r       | 169      |                        | 1+p+q+p\*q+r              		|
| 42       | (p&q&r)^r           | (1+p\*q)\*r                | 170      |                        | r                         		|
| 43       | p^((p^r)\|(p^~q))   | 1+p+q+p\*q+p\*r+q\*r       | 171      |                        | 1+p+q+p\*q+p\*r+q\*r+p\*q\*r	|
| 44       | (p&(q\|r))^q        | q+p\*q+p\*r+p\*q\*r        | 172      |                        | q+p\*q+p\*r               		|
| 45       | p^(q\|~r)           | 1+p+r+q\*r                 | 173      |                        | 1+p+r+q\*+p\*q\*r         		|
| 46       | (p&q)^(q\|r)        | q+p\*q+r+q\*r              | 174      |                        | q+p\*q+r+q\*r+p\*q\*r     		|
| 47       | ~p\|(~q&r)          | 1+p+p\*r+p\*q\*r           | 175      |                        | 1+p+p\*r                  		|
| 48       | p&~q                | p\*(1+q)                   | 176      |                        | p\*(1+q+q\*r)             		|
| 49       | (p\|q\|~r)^q        | (1+q)\*(1+r+p\*r)          | 177      |                        | 1+q+r+p\*r+q\*r           		|
| 50       | (p\|q\|r)^q         | (1+q)\*(p+r+p\*r)          | 178      |                        | p+p\*q+r+p\*r+q\*r        		|
| 51       | ~q                  | 1+q                        | 179      |                        | 1+q+p\*q\*r               		|
| 52       | (p\|(q&r))^q        | p+q+q\*r+p\*q\*r           | 180      |                        | p+q+q\*r                  		|
| 53       | (p\|(q^~r))^q       | 1+p\*q+r+p\*r              | 181      |                        | 1+p\*q+r+p\*r+p\*q\*r     		|
| 54       | (p\|r)^q            | p+q+r+p\*r                 | 182      |                        | p+q+r+p\*r+p\*q\*r        		|
| 55       | ~((p\|r)&q)         | 1+p\*q+q\*r+p\*q\*r        | 183      |                        | 1+p\*q+q\*r               		|
| 56       | p^((p\|r)&q)        | p+p\*q+q\*r+p\*q\*r        | 184      |                        | p+p\*q+q\*r                		|
| 57       | (p\|~r)^q           | 1+q+r+p\*r                 | 185      |                        | 1+q+r+p\*r+p\*q\*r        		|
| 58       | (p\|(q^r))^q        | p+p\*q+r+p\*r              | 186      |                        | p+p\*q+r+p\*r+p\*q\*r     		|
| 59       | (~p&r)\|~q          | 1+q+q\*r+p\*q\*r           | 187      |                        | 1+q+q\*r                  		|
| 60       | p^q                 | p+q                        | 188      |                        | p+q+p\*q\*r               		|
| 61       | p^(p\|q\|r)^~q      | 1+p\*q+r+p\*r+q\*r+p\*q\*r | 189      |                        | 1+p\*q+r+p\*r+q\*r        		|
| 62       | (p&q)^(p\|q\|r)     | p+q+r+p\*r+q\*r+p\*q\*r    | 190      |                        | p+q+r+p\*r+q\*r           		|
| 63       | ~(p&q)              | 1+p\*q                     | 191      |                        | 1+p\*q+p\*q\*r            		|
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**     		|
| 64       | p&q&~r              | p\*q\*(1+r)                | 192      | p&q                    | p\*q                      		|
| 65       | ~((p^)\|r)          | (1+p+q)\*(1+r)             | 193      |                        | 1+p+q+r+p\*r+q\*r+p\*q\*r 		|
| 66       | (p^r)&(q^r)         | p\*q+r+p\*r+q\*r           | 194      |                        | p\*q+r+p\*r+q\*r+p\*q\*r  		|
| 67       | p^(p&q&r)^~q        | 1+p+q+p\*q\*r              | 195      |                        | 1+p+q                     		|
| 68       | q&~r                | q\*(1+r)                   | 196      |                        | q\*(1+r+p\*r)             		|
| 69       | (~p\|q\|r)^r        | (1+p+p\*q)\*(1+r)          | 197      |                        | 1+p+p\*q+r+p\*r           		|
| 70       | ((p&r)\|q)^r        | q+r+p\*r+p\*q\*r           | 198      |                        | q+r+p\*r                  		|
| 71       | ((p^~r)\|q)^r       | 1+p+p\*q+q\*r              | 199      |                        | 1+p+p\*q+q\*r+p\*q\*r     		|
| 72       | (p&q)^(q&r)         | q\*(p+r)                   | 200      |                        | q\*(p+r+p\*r)             		|
| 73       | ~((p&r)\|(p^q^r))   | 1+p+q+r+p\*r+p\*q\*r       | 201      |                        | 1+p+q+r+p\*r              		|
| 74       | (p&(q\|r))^r        | p\*q+r+p\*r+p\*q\*r        | 202      |                        | p\*q+r+p\*r               		|
| 75       | (p^(~q\|r)          | 1+p+q+q\*r                 | 203      |                        | 1+p+q+q\*r+p\*q\*r        		|
| 76       | (p&q&r)^q           | q\*(1+p\*r)                | 204      |                        | q                         		|
| 77       | p^((p^q)\|(p^~r))   | 1+p+p\*q+r+p\*r+q\*r       | 205      |                        | 1+p+p\*q+r+p\*r+q\*r+p\*q\*r        |
| 78       | p^((p^)\|r)         | q+r+p\*r+q\*r              | 206      |                        | q+r+p\*r+q\*r+p\*q\*r     		|
| 79       | ~p\|(q&~r)          | 1+p+p\*q+p\*q\*r           | 207      |                        | 1+p+p\*q                  		|
| 80       | p&~r                | p\*(1+r)                   | 208      |                        | p\*(1+r+q\*r)             		|
| 81       | (p\|~q\|r)^r        | (1+q+p\*q)\*(1+r)          | 209      |                        | 1+q+p\*q+r+q\*r           		|
| 82       | (p\|(q&r))^r        | p+r+q\*r+p\*q\*r           | 210      |                        | p+r+q\*r                  		|
| 83       | (p\|(q^~r))^r       | 1+q+p\*q+p\*r              | 211      |                        | 1+q+p\*q+p\*r+p\*q\*r     		|
| 84       | (p\|q\|r)^r         | (p+q+p\*q)\*(1+r)          | 212      |                        | p+q+p\*q+p\*r+q\*r        		|
| 85       | ~r                  | 1+r                        | 213      |                        | 1+r+p\*q\*r               		|
| 86       | (p\|q)^r            | p+q+p\*q+r                 | 214      |                        | p+q+p\*q+r+p\*q\*r        		|
| 87       | ~((p\|q)&r)         | 1+p\*r+q\*r+p\*q\*r        | 215      |                        | 1+p\*r+q\*r               		|
| 88       | p^((p\|q)&r)        | p+p\*r+q\*r+p\*q\*r        | 216      |                        | p+p\*r+q\*r               		|
| 89       | (p\|~q)^r           | 1+q+p\*q+r                 | 217      |                        | 1+q+p\*q+r+p\*q\*r        		|
| 90       | p^r                 | p+r                        | 218      |                        | p+r+p\*q\*r               		|
| 91       | p^(~(p\|q\|r))^r    | 1+q+p\*q+p\*r+q\*r+p\*q\*r | 219      |                        | 1+q+p\*q+p\*r+q\*r        		|
| 92       | (p\|(q^r))^r        | p+q+p\*q+p\*r              | 220      |                        | p+q+p\*q+p\*r+p\*q\*r     		|
| 93       | ~((p\|~q)&r)        | 1+r+q\*r+p\*q\*r           | 221      |                        | 1+r+q\*r                  		|
| 94       | (p&r)^(p\|q\|r)     | p+q+p\*q+r+q\*r+p\*q\*r    | 222      |                        | p+q+p\*q+r+q\*r           		|
| 95       | ~(p&r)              | 1+p\*r                     | 223      |                        | 1+q\*r+p\*q\*r            		|
| **Rule** | **Boolean**         | **Alegbraic (mod 2)**      | **Rule** | **Boolean**            | **Alegbraic (mod 2)**     		|
| 96       | p&(q^r)             | p\*(q+r)                   | 224      |                        | p\*(q+r+q\*r)             		|
| 97       | ~((p^q^r)\|(q&r))   | 1+p+q+r+q\*r+p\*q          | 225      |                        | 1+p+q+r+q\*r              		|
| 98       | ((p\|r)&q)^r        | p\*q+r+q\*r+p\*q\*r        | 226      |                        | p\*q+r+q\*r               		|
| 99       | (~p\|r)^q           | 1+p+q+p\*r                 | 227      |                        | 1+p+q+p\*r+p\*q\*r        		|
| 100      | ((p&q)\|r)^q        | q+p\*r+q\*r+p\*q\*r        | 228      |                        | q+p\*r+q\*r               		|
| 101      | p^(p&q)^~r          | 1+p+p\*q+r                 | 229      |                        | 1+p+p\*q+r+p\*q\*r        		|
| 102      | q^r                 | q+r                        | 230      |                        | q+r+p\*q\*r               		|
| 103      | ~(p\|q\|r)^q^r      | 1+p+p\*q+p\*r+q\*r+p\*q\*r | 231      |                        | 1+p+p\*q+p\*r+q\*r        		|
| 104      | p^(p\|q\|r)^q^r     | p\*q+p\*r+q\*r+p\*q\*r     | 232      |                        | p\*q+p\*r+q\*r             		|
| 105      | p^q^~r              | 1+p+q+r                    | 233      |                        | 1+p+q+r+p\*q\*r           		|
| 106      | (p&q)^r             | p\*q+r                     | 234      |                        | p\*q+r+p\*q\*r            		|
| 107      | p^(p\|q\|~r)^q^r    | 1+p+q+p\*r+q\*r+p\*q\*r    | 235      |                        | 1+p+q+p\*r+q\*r           		|
| 108      | (p&r)^q             | q+p\*r                     | 236      |                        | q+p\*r+p\*q\*r            		|
| 109      | p^(p\|~q\|r)^q^r    | 1+p+p\*q+r+q\*r+p\*q\*r    | 237      |                        |                           		|
| 110      | (~p&q&r)^q^r        | q+r+q\*r+p\*q\*r           | 238      |                        |                           		|
| 111      | ~p\|(q^r)           | 1+p+p\*q+p\*r              | 239      |                        |                           		|
| 112      | p^(p&q&r)           | p\*(1+q\*r)                | 240      |                        |                           		|
| 113      | p^(~((p^q)\|(p^r))) | 1+q+p\*q+r+p\*r+q\*r       | 241      |                        |                           		|
| 114      | ((p^q)\|r)^q        | p+r+p\*r+q\*r              | 242      |                        |                           		|
| 115      | (p&~r)\|~q          | 1+q+p\*q+p\*q\*r           | 243      |                        |                           		|
| 116      | (p\|q)^(q&r)        | p+q+p\*q+q\*r              | 244      |                        |                           		|
| 117      | (p&~q)\|~r          | 1+r+p\*r+p\*q\*r           | 245      |                        |                           		|
| 118      | (p\|q\|r)^(q&r)     | p+q+p\*q+r+p\*r+p\*q\*r    | 246      |                        |                           		|
| 119      | ~(q&r)              | 1+q\*r                     | 247      |                        |                           		|
| 120      | p^(q&r)             | p+q\*r                     | 248      |                        |                           		|
| 121      | p^(~p\|q\|r)^q^r    | 1+q+p\*q+r+p\*r+p\*q\*r    | 249      |                        |                           		|
| 122      | p^(p&~q&r)^r        | p+r+p\*r+p\*q\*r           | 250      |                        |                           		|
| 123      | ~((p^q^r)&q)        | 1+q+p\*q+q\*r              | 251      |                        |                           		|
| 124      | p^(p&q&~r)^q        | p+q+p\*q+p\*q\*r           | 252      |                        |                           		|
| 125      | (p^q)\|~r           | 1+r+p\*r+q\*r              | 253      |                        |                           		|
| 126      | (p^q)\|(p^r)        | p+q+p\*q+r+p\*r+q\*r       | 254      |                        |                           		|
| 127      | ~(p&q&r)            | 1+p\*q\*r                  | 255      | 1                      | 1                         		|
