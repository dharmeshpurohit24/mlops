import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

publicIp = "65.1.110.118"

ssh.connect(
    hostname=publicIp,
    username="ec2-user",
    key_filename="learning.pem"
)

stdin, stdout, stderr = ssh.exec_command("df / | awk 'NR==2 {gsub(\"%\",\"\"); print $5}'")

value = stdout.read().decode().strip()

if(int(value) > 80):
    print("disk usage overboard !!")
    with open("disk_alert.log", "a") as fp:
        fp.write(f"{publicIp} - Disk usage is over 80%\n")
else: 
    print(f"Disk usage is {value}")

ssh.close()