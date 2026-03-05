## Steps for IAM user and role

**Step-0: account creation**
- create a aws account and login into that.

**Step-1: Policy creation**
- from the sidebar click policies.
- click create policy button and specify policy editor (json/visual).I have selected json.
- in policy editor on left side select action and specify (like "s3:ListAllMyBuckets") s3 and then listallmybuckets.
- then add resource (for s3 select all resource and click add a resource) or add directly in json.
- click on next and enter name for this policy and click create policy.

**Step-2: Create Role**
- click on create role and then select identity.
- for iam user (choose aws account) and click next.
- in permission policy selector filter by *customer managed* and click the policy we generated.
- click next and enter name for this role and click create role.

**Step-3: create a IAM user**
- from the sidebar choose users and click create user button.
- assign a username and select *provide user access to aws management console* checkbox.
- click next and select *attach policies directly* select the policy created.
- click next and review all the details there and click create user.