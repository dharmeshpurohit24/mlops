## public and private subnets in VPC

**Basic Info**
- Subnet: When we break a large network in smaller networks it is called subnet of that network.Each subnet have its own range of ip's.
- Private subnet: In private subnet devices cannot directly access the internet. Devices are only visible inside network (VPC). They dont have public ip's. We can use NAT for devices in private subnet to access the internet.
- Public subnet: In public subnet devices can directly access the internet. Devices in public subnet have public ip.
- SSH (secure shell): Used to access the instance or server remotely and do the work there.

**Steps followed**
- First create a vpc and write the CIDR block (10.0.0.0/24).
- create subnet and choose the vpc id for it use same az for now.
- For first subnet use 10.0.0.0/25 (gives 128 ip's) public subnet.
- For second subnet use 10.0.0.128/25 (same 128 ip) private subnet. 
- Create a new internet gateway and then attach the gateway to vpc.
- Create the route tables for the subnet private and public.
- For public route table add a new route (0.0.0.0/0) and target internet gateway(we created in setp-3) and click *save*.
- Create a private route table.

## Ec-2 instance in private and public subnet

**Basic Info**
- NAT (Network Address Translation): Private subnet cannot directly access the internet.
A nat gateway helps allow private instance to send traffic and recieve the traffic from internet.

**Steps followed**
- In the vpc we created already.
- Create a NAT gateway using public subnet and allocate a elastic ip.
- Update the private route table and add the route for 0.0.0.0/0 to NAT gateway we created.
- Now create two Ec-2 instances.
- Create public Ec-2 instance using default options and public subnet created.
- While creating private Ec-2 disable the auto assign ip for security group add the public security group.
- Now create these ec-2 instance.

## Auto Scaling Group

- we use launch template to specify the instance configuration and then create a auto scaling group for automatic managing the ec2 instances.
- performs health checks also.

**Types of scaling**

- Target Tracking Scaling: Automatically adjusts the number of instances to maintain a target metric(like cpu utilization). 
- Step Scaling: add or remove instance in steps based on theresholds. can define what to do on particular threshold.
- Simple Scaling: Add or remove a fixed number of instances when a single threshold is breached. less flexible 

**Steps followed**
- Create a new launch template.
- Choose default AMI (amazon linux free tier) and t2.micro as inatance type. Keep security group ssh (port 22) with my ip option. Then Create launch template.
- Now create a new auto scaling group.
- Select the launch template we created.
- On group size choose desired capacity as 1 and minimum 1 and maximum as 2.
- Create a target scaling policy and choose average cpu utilization with target value of 50.
- Create this auto scaling group.

## Bugets Alarms

**Bugets**
- Allows monitoring of your AWS costs and usage.
- Can set thresholds for cost, usage, or reservations

**Budget Alarms**
- Sends notifications when spending exceeds a set threshold.
- used for cost management and control.

**Steps followed**
- Create a new budget.
- Choose the zero budget alarm.
- Click create the alarm.