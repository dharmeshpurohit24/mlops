## Launch on demand EC-2 instances with restricted ssh access (for itt)

**Ec-2 Basic Info**
- Ec-2 (elastic compute cloud) is used renting servers on the internet from amazon. 
- This virtual instance can be adjusted according to needs like ram,os, storage.
- SSH (secure shell): used to connect linux type instance. uses port 22.
- AMI (amazon machine image): template that contains the operating system and required configurations.
- Key-pair: used for secure login.
- Security Groups: Used as a virtual firewall for controlling which ports are open and which ip can access it.
- EBS (elastic block storage): virtual storage which can be attached and detached to ec2.

**Get the ip range first**
- Contacted the itt it-team for getting the range of ip for itt network.

**Steps followed**
- Launch a new Ec-2 instance and give it a name.
- Choose an AMI (amazon machine image) as *amazon linux* (for free tier).
- Select the instance type as t2.micro (for free tier).
- Create (can use default config) or choose a key pair for accessing the ec-2 remotely.
- *In Newtork settings section* for firewall (security group) choose create security group option (default) and select allow ssh traffic (for opening port 22 for ssh).
- Now choose custom (from dropdown) and enter the ip's provided by it team.
- In storage (will be default 8 as root volume) add a new volume and write 7 (as told in assignment) with gp2 (free tier).
- Leave rest as default and click launch instance.

**Remote SSH**
- First make the file readable. `chmod 400 itt-ssh.pem` in location file is downloaded.
- Run the command `ssh -i itt-ssh.pem ec2-user@<public ip of instance>`.

**Notes**
- Security groups are stateful means if we allow incomming traffic on a port outgoing traffic is automatically allowed back.
- The family of instance and its usage:-
    -> t : bustable general purpose for small task
    -> m : general purpose
    -> c : compute optimized
    -> r : memory optimized
- For this assingment we used the security grp to use custom ip ranges provided.