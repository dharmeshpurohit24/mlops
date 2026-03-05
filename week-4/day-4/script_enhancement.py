import paramiko
import logging

publicIp = "52.66.253.53"
logFile = "disk_alert.log"

logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def isDiskOverUsage(value, threshold=80):
    if int(value) > threshold:
        return True
    else:
        return False

def checkUsageScript():    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=publicIp,
            username="ec2-user",
            key_filename="learning.pem"
        )

        stdin, stdout, stderr = ssh.exec_command("df / | awk 'NR==2 {gsub(\"%\",\"\"); print $5}'")

        diskUsageValue = stdout.read().decode().strip()

        if isDiskOverUsage(diskUsageValue):
            logging.warning(f"Disk usage is overboard *{diskUsageValue}* !!")

        else: 
            logging.info(f"Disk usage is normal = {diskUsageValue}")
        
        ssh.close()

    except Exception as e: 
        logging.exception("Failed to read disk usage from server.\nCheck the disk_alert.log file for details.")

if __name__ == "__main__":
    checkUsageScript()