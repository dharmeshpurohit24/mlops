## Networking assignment 

** self-explanatory diagram for creating subnets from a network. **

- Network is a group of devices connected together for communication.
- In a network we are assigned a Ip address (unique no) for identification.
- Subnet is basically dividing a large network into smaller one.
- We use subnet mask to seperate network and host id. Where (1: network and 0: host)
- We use subnetting to divide the network for better management and security also.

Network: 192.168.1.0/24
Subnet Mask: 255.255.255.0

            192.168.1.0/24
-----------------------------------------
| PC1 | PC2 | PC3 | PC4 | PC5 | PC6 | ...
-----------------------------------------
(All devices are in ONE network)


Main Network: 192.168.1.0/24
                    |
          -------------------------
          |                       |
      Subnet A                Subnet B
  192.168.1.0/25          192.168.1.128/25
  Mask: .128              Mask: .128
          |                       |
     -----------             -----------
     | PC1 PC2 |             | PC3 PC4 |
     -----------             -----------


** Subnet the Class C IP Address 205.11.2.0 so that you have 30 subnets ** 

205.11.2.0

currently there is only one network for class C
205.11.2.0/24 This is currently here.

as we know we can create in power of 2 for creating 30 subnet i need :-

2^5 = 32 (more then enough)
so we need to borrow 5 bits from host id
network id: 24 + 5 = 29


205.11.2.0/29

subnet mask = 29 => 11111111.11111111.11111111.11111000 => 255.255.255.248

each subnet can have = 32 - 29 => 3 host bits
SO HOST = 2^3 => 8

Block size = 256 - 248 => 8 bit size

Hence we have :-
205.11.2.0 - 205.11.2.7 => 1 subnet

205.11.2.8 - 205.11.2.15 => 2 subnet

205.11.2.16 - 205.11.2.23 => 3 subnet
....

For subnet 2 :-

205.11.2.8 <= network
205.11.2.9 <- 1
205.11.2.10  <-2
205.11.2.11  <= 3'rd host 
205.11.2.12
205.11.2.13
205.11.2.14
205.11.2.15 <= brodcast


IP of third host on subnet 2 is * 205.11.2.11/29 *