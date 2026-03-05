## Weekly Assignment for networking

** Write the IP address 135.1.1.25 mask 255.255. 248.0 in CIDR notation **

255.255.248.0 convert to binary notation...

255     .  255   . 248    . 0
11111111.11111111.11111000.00000000
count no of 1's = 8 + 8 + 5 => 21

so in CIDR notation: 135.1.1.25/21



** For this 192.168.0.0/16 Subnetting need to be implemented for assigning network to 5 different projects **

192.168.0.0/16

16 => only 1 network (no subnetting currently)

we need 5 subnet for different projects...

2^2 = 4 (not enough) 2^3 = 8 (sufficient) 
we need to take 3 bits from host id now we will have

16 + 3 => 19 (network id's)
32 - 19 => 13 (host id's)

we will now have 2^13 => 8190 host address

so the subnets now we have will be like this :-
19 => 255.255.224.0 (in dotted decimal)
subnet block size = 256 - 224 => * 32 *-<<<

Project A = 192.168.0.0 - 192.168.31.255
Project B = 192.168.32.0 - 192.168.63.255
Project C = 192.168.64.0 - 192.168.95.255
Project D = 192.168.96.0 - 192.168.127.255
Project E = 192.168.128.0 - 192.168.159.255