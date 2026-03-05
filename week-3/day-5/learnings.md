## Application load balancing for Ec-2 instances

**Load balancer**
Load balancer is used to balance the load on ec-2 instances by diverting the traffic to group of ec-2 instances instead of just one instance.
This helps in reducing single point of failure.

**Types of AWS load balancer**
1. Classic Load Balancer (ELB):
    -> Old generation load balancer used in legacy applications
    -> uses basic round-robin
    -> works on layer 4 and 7 (works on both network and application layer)

2. Network Load Balancer (NLB):
    -> fastest and low latency
    -> works on layer 4 (network layer)
    -> uses basic routing without inspecting HTTP traffic

3. Application Load Balancer (ALB):
    -> fast and low latency
    -> works on layer 7 (application layer)
    -> uses smart routing 

**Steps followed**
- Create two Ec-2 instances (default options).
- Create a new target group.
- Now select newly created target group and register target (two ec-2 instance we created).
- Now Create a load balancer and choose ALB (Application Load Balancer).
- Fill the basic info and add listeners for target group port 80 http protocal (select forward to target group).
- In routing action forward to target group and select the target group we created. Then create Load balancer.
- The setup is completed now.

**Note**
- we can add health checks for monitoring the status of instance.
- can use cloudwatch for monitoring the logs.
