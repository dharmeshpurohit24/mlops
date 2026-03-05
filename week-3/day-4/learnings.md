## S3 buckets

- S3 (Simple storage service) used to store, retrive and manage any amount of data from anywhere.

**Basic Info**
- bucket: container for storing
- object: Actual files
- key: unique name to identify an object inside a bucket
- prefix: logical path used to organize objects like paths
- Bucket key: it is a feature that reduce AWS KMS cost by creating a bucket level key.
- Versioning: Keeps multiple versions of an object in the same bucket.
- Replication: Automatically copies objects between buckets.

**Encryption in S3**
- SSE-S3: Server-side encryption using S3-managed keys
- SSE-KMS: Server-side encryption using AWS KMS keys
- DSSE-KMS: Dual-layer encryption using two KMS keys for higher security

**Steps followed**
- First create KMS keys in both aws account (for s3 bucket replication).
- Create two buckets in aws accounts with versioning enabled and key selected.
- Now in source account create a role for bucket to read (srouce bucket) and decrypt (source kms key) objects in soruce bucket and encrypt (destination kms key) and write to destination bucket (bucket name).
- Now for source account kms key policy allow to decrypt the data from bucket.
- In destination bucket account allow the kms key to encrypt the data in destination.
- Now in both buckets in source account and destination account edit the bucket policy to enforce encryption in objects.
- Now in source account bucket enable the replication rule for destination account bucket (use Destination account id and bucket name).
- Choose the iam role create for source bucket.
- Enable the kms encryption checkbox and put the destination account kms key arn.
- Create this replication rule.