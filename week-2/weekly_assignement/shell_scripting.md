## Weekly shell scripting assignment:-

** Creating user and assign to group **
1. `sudo adduser new-user` : This will create a new user with home directory.
2. `su new-user` : This will switch to user
3. `cd ~` : Will take to home directory of user.
4. `su piyush` : Will switch to piyush user (root user here) and now we can add new-user to use sudo.
5. `sudo usermod -aG sudo new-user` : Will add a new group sudo for new-user (will append Group sudo in new-user groups)
6. `exit` : To exit current session for refresh.
7. `su new-user`: Switch to new-user and now we can use sudo.
8. `sudo groupadd new-grp` : Will create a new group named new-grp.
9. `sudo usermod -aG new-grp new-user` : We have sudo permission now so we this new group to user.
10. `groups new-user` : Can verify by using this command which groups are added for current user.

** Finding log older then 7 days **
- `find /var/log -name "*.log" -type f -mtime +7` : Will list all the files modified more than 7 days ago.

** Changing permissions **

we change the permissions using numbers as we know:-
execute : 1
write : 2
read : 4 
and we write in format owner;group;others (eg. 100)

So command for read and write permission to owner only.
- `chmod 600 /opt/devops/scripts`