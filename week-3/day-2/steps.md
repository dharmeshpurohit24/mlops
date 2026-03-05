## VPC creation with public and private subnet

**Setp-1: VPC Creation**
- open aws searchbar and search for vpc and click on it.
- click create vpc button and fill the form.
- click vpc only (as will setup the subnet and routing table manually).
- Choose ipv4 as default for now.
- now enter ipv4 CIDR input (have writen 10.0.0.0/24) currently we use /24 we dont need many ip's.
- keep rest as default and click create VPC button.

**Step-2: Subneting**
- on sidebar click subnet and click create subnet button.
- select the vpc id (we just created in step-1).
- then create subnet for that network. Use Same AZ for now.
- click AZ for ap-south-1a in both subnet.
- for first subnet use 10.0.0.0/25 (gives 128 ip's) public subnet.
- for second subnet use 10.0.0.128/25 (same 128 ip) private subnet.

**Step-3: Internet gateway**
- from sidebar select internet gateway and click *create internet gateway* button.
- now name the gateway.
- then click on actions dropdown and *attach to VPC* and select the VPC.
- vpc is connected to gateway now.

**Step-4: Route Tables**
- fron sidebar click on route tables button (will create 2 route tables for public and private subnet).
- now click *create route table* and fill the details.
- write a name and select the VPC and click create route table (for public subnet).
- click on table id we just created.
- for public route table add a new route (0.0.0.0/0) and target internet gateway(we created in setp-3) and click *save*.
- now go to subnet associations and click *edit subnet associations* select the public subnet (as this is public route) and click *save*.
- now create a *new route table* (for private subnet not necessary but best practice).
- write name for it and use same vpc and click *create*.
- in this private subnet go to *subnet association* and click *edit subnet associations*.
- now add the private subnet and click *save*.

Now we have created a VPC (10.0.0.0/24).
Created two subnets public (10.0.0.0/25) and private (10.0.0.128/25).