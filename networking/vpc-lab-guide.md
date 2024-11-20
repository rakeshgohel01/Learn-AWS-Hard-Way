# Lab Guide: VPC Setup and Configuration

### Objective

Create a VPC with public and private subnets, configure necessary gateways, and deploy a test EC2 instance.

### Duration: 45 minutes

### Prerequisites

- AWS Console access
- Understanding of CIDR notation
- Basic EC2 knowledge

### Steps

#### 1. Create VPC

```bash
# VPC Details
Name:-VPC1
CIDR: 10.0.0.0/16
Region: us-east-1
```

1. Navigate to VPC Dashboard
2. Click "Create VPC"
3. Enter VPC details
4. Enable DNS hostnames

#### 2. Create Subnets

```bash
# Public Subnet
Name: Public-Subnet-1
CIDR: 10.0.1.0/24
AZ: us-east-1a

# Private Subnet
Name: Private-Subnet-1
CIDR: 10.0.2.0/24
AZ: us-east-1a
```

#### 3. Configure Internet Gateway

1. Create Internet Gateway
2. Attach to VPC
3. Configure route table

#### 4. Configure NAT Gateway

1. Create NAT Gateway in public subnet
2. Allocate Elastic IP
3. Update private subnet route table

#### 5. Security Configuration

```bash
# Security Group Rules
Inbound:
- SSH (22): Your IP
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0

Outbound:
- All traffic: 0.0.0.0/0
```

#### 6. Deploy Test EC2 Instance

1. Launch EC2 in public subnet
2. Configure security group
3. Test connectivity

### Validation Steps

1. SSH into public EC2 instance
   1. Use key pair
   2. Use Session manager
2. Ping internet from public instance
3. Check routing tables
4. Verify security group rules

### Common Issues and Solutions

1. Cannot connect to EC2:
   
   - Check security group
   - Verify route table
   - Confirm IGW attachment

2. No internet access:
   
   - Check NAT Gateway status
   - Verify route tables
   - Confirm IGW configuration

### Next Steps

- Add more subnets
- Configure VPC endpoints
- Set up VPC peering
- Implement transit gateway