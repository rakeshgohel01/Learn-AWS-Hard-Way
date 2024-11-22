# AWS Identity and Access Management

### 1. Introduction to IAM

#### What is AWS IAM?

* Cloud-native identity management service
* Centralized control of AWS account access
* Fine-grained access management for AWS resources
* Enables creating users, groups, roles, and defining permissions

#### Core Principles

* Least Privilege: Grant minimum necessary permissions
* Centralized Access Control
* Multi-Factor Authentication (MFA) Support
* Compliance and Auditing Capabilities

### 2. IAM Core Components

#### 2.1 Users

* Represents individuals or services requiring AWS access
* Unique identifier and credentials
* Can be assigned to multiple groups
* Types:
  - Root User (initial account creator)
  - IAM Users (recommended for day-to-day operations)

#### 2.2 Groups

* Collection of IAM users
* Simplify permission management
* Enable bulk permission assignment
* Best practice for organizing user permissions

#### 2.3 Roles

* Set of permissions defining AWS resource access
* Can be assumed by users, services, or resources
* Support cross-account access
* Enable temporary access credentials

#### 2.4 Policies

* JSON documents defining permissions
* Determine actions allowed/denied
* Types:
  - AWS Managed Policies
  - Customer Managed Policies
  - Inline Policies

### 3. Permission Structure

#### Policy Document Components (Identity-Based Policy)

- Allows user to perform actions

- Controls what a user can do across multiple resources

```json
Identity X (user, group, role) can do Action Y on Resource Z

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow/Deny",
            "Action": ["service:Operation"],
            "Resource": ["arn:aws:service:region:account-id:resource"],
            "Condition": {optional matching rules}
        }
    ]
}
```

- #### Permission Evaluation Logic
1. Default: All requests are denied
2. Explicit Allow overrides Deny
3. Explicit Deny always wins
4. Multiple policies are combined

#### 

### 4. Authentication Mechanisms

#### 4.1 Authentication Methods

* Username/Password
* Multi-Factor Authentication (MFA)
* Access Keys
* Temporary Security Credentials
* Single Sign-On (SSO)
* Identity Federation

#### 4.2 Credential Types

* Console Password
* Access Key ID and Secret Access Key
* X.509 Certificates
* SSH Keys

### 5. Advanced IAM Concepts

#### 5.1 Trust Relationships

* Define who can assume a role
* Enable cross-account access
* Support service-to-service interactions

#### 5.2 Resource-Based Policies

* Allows resources to be accessed from different account

* Controls who can access a specific resource

* Attached directly to resources

* Examples: S3 bucket policies, SQS queue policies

* ```json
  Resource X allows Identity Y to do Action Z
  
  {
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::account-id:user/{username}"},
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-bucket/*"]
    }]
  }
  ```

* Complement identity-based policies
  
  * Both must permit the action for cross-account access to work
  
  * Together - create precise access patterns
  
  * Example scenario
    
    * ```textile
      Scenario: Company A wants to share S3 bucket data with Company B
      
      Company A (Account owner):
      - Creates resource-based policy on S3 bucket allowing Company B's account
      
      Company B:
      - Creates identity-based policy allowing their users to access the bucket
      
      Result: Only authorized users from Company B can access the specific bucket
      ```

#### 5.3 Service Roles

* Permissions allowing AWS services to act on your behalf
* Examples: Lambda execution role, EC2 instance role
* Enable secure service interactions

### 6. Best Practices

#### Security Best Practices

* Disable root account access
* Use strong password policies
* Enable MFA
* Rotate credentials regularly
* Implement least privilege principle

#### Operational Best Practices

* Use groups for permission management
* Leverage AWS managed policies
* Implement regular access reviews
  * More in Monitoring Tools sections
* Use AWS Organizations for centralized management

### 7. Common IAM Scenarios

#### Scenario 1: Developer Access

* Create IAM group with development permissions
* Attach specific service access policies
* Enable temporary elevated access
* ```bash
  1)
  aws iam create-group --group-name DevelopersGroup
  
  2)
  aws iam attach-group-policy --group-name DevelopersGroup --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
  
  custom-development-policy.json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::development-bucket",
          "arn:aws:s3:::development-bucket/*"
        ]
      }
    ]
  }
  
  aws iam create-policy --policy-name CustomDevelopmentPolicy --policy-document file://custom-development-policy.json
  aws iam attach-group-policy --group-name DevelopersGroup --policy-arn arn:aws:iam::<account-id>:policy/CustomDevelopmentPolicy
  
  
  3)
  trust-policy.json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::<account-id>:group/DevelopersGroup"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  
  
  aws iam create-role --role-name DevelopersElevatedRole --assume-role-policy-document file://trust-policy.json
  
  aws iam attach-role-policy --role-name DevelopersElevatedRole --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
  
  aws sts assume-role --role-arn arn:aws:iam::<account-id>:role/DevelopersElevatedRole --role-session-name TemporaryAccess
  
  export AWS_ACCESS_KEY_ID=TemporaryAccessKey
  export AWS_SECRET_ACCESS_KEY=TemporarySecret
  export AWS_SESSION_TOKEN=TemporaryToken
  
  aws sts get-caller-identity 
  ```

#### Scenario 2: CI/CD Pipeline

* Create service role for deployment
* Use temporary credentials
* Implement strict resource access
* ```json
  1)
  trust-policy.json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  
  
  aws iam create-role --role-name DeploymentServiceRole --assume-role-policy-document file://trust-policy.json
  
  
  aws iam attach-role-policy --role-name DeploymentServiceRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
  aws iam attach-role-policy --role-name DeploymentServiceRole --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess
  aws iam attach-role-policy --role-name DeploymentServiceRole --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerServiceFullAccess
  
  
  2)
  Credential check
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/DeploymentServiceRole
  
  
  3)
  custom_policy.json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::deployment-bucket/*"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
          "lambda:InvokeFunction"
        ],
        "Resource": [
          "arn:aws:lambda:us-east-1:123456789012:function:MyDeploymentFunction"
        ]
      }
    ]
  }
  
  
  aws iam create-policy --policy-name DeploymentStrictAccess --policy-document file://deployment-policy.json
  aws iam attach-role-policy --role-name DeploymentServiceRole --policy-arn arn:aws:iam::<account-id>:policy/DeploymentStrictAccess
  
  
  ```

#### Scenario 3: Compliance Requirement

* Use tag-based access control
* Implement strict boundary policies
* Enable comprehensive logging

### 8. Monitoring and Compliance

#### Monitoring Tools

* AWS CloudTrail
  * Logs all API actionss by users, roles and services
  * Provides a historical record of resource access/actions
  * **Use Case**: Detect unused roles or unusual activity during access reviews
* Amazon CloudWatch
* AWS Trusted Advisor
  * Offers security best prartice checks
  * Identifies inactive IAM users and unused access keys
  * **Use Case**: Quick insights into unused resources
* AWS Config
  * Continuosly tracks chanegs to IAM enttities/policies
  * includes managed rules like
    * iam-user-no-inlline-policy
    * iam-user-unused-credentials-check
    * iam-policy-no-statements-with-admin-acess
    * **Use Case**: Monitor and enforce compliance with security policies
* AWS IAM Access Analyzer
  * Permission analysis for resources i.e s3, IAM roles/policies
  * Detects unintended access, especially for public or cross-account access
  * **Use case**: Identify and act on overly permissive roles/policies

#### Compliance Frameworks

* Support for HIPAA, PCI DSS, SOC
* Detailed access logging
* Automated compliance checks

### 9. Troubleshooting IAM

#### Common Troubleshooting Techniques

* Use IAM Policy Simulator
* Review CloudTrail logs
* Check policy syntax
* Verify trust relationships
* Understand permission boundaries

### 10. Future of AWS IAM

* Increasing granular controls
* More automated security
* Enhanced machine learning integration
* Simplified management interfaces

## Conclusion

IAM is critical for securing AWS environments. Continuous learning and adaptation are key to maintaining robust cloud security.
