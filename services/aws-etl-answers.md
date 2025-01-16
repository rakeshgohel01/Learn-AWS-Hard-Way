# Answers to ETL

## Quiz: AWS Glue

1. What are the core components of AWS Glue?
   
   - **Data Catalog**: A centralized repository to store metadata about your data assets.
   - **Crawlers**: Tools that scan data sources, infer schemas, and populate the Data Catalog.
   - **ETL Jobs**: Jobs that extract, transform, and load data using either PySpark or Python scripts.
   - **Triggers**: Mechanisms to schedule and orchestrate ETL jobs.
   - **Security**: Built-in IAM integration for access control and encryption.

2. Explain how Glue Crawlers work.
   
   - Glue Crawlers automatically scan data sources to determine their structure and schema.
   - They create or update metadata in the AWS Glue Data Catalog, enabling it to be used in ETL jobs or analytics.
   - Steps involved:
     1. Define a crawler with the data source location (e.g., S3 bucket or database).
     2. Specify the output target (a Data Catalog database or table).
     3. Run the crawler to infer the schema and update the Data Catalog.

3. How can you secure an ETL job in AWS Glue?
   
   - **Access Control**:
     - Use IAM roles and policies to grant least privilege access to Glue jobs.
   - **Encryption**:
     - Enable encryption for data at rest (e.g., using S3 bucket encryption).
     - Use SSL/TLS for data in transit.
   - **Network Security**:
     - Run Glue jobs in a VPC to isolate them from public access.
     - Restrict access to data sources using security groups and NACLs.
   - **Audit and Monitoring**:
     - Enable AWS CloudTrail to log Glue job activities.
     - Monitor job execution and resource usage with CloudWatch.

# 

## Quiz: Apache Airflow

1. What are Directed Acyclic Graphs (DAGs) in Airflow?
   
   - Represents workflows as a collection of tasks arranged in a sequence with dependencies.
   
   - Defines order and dependency in a graph

2. How does Airflow integrate with AWS services?
   
   - Provides  operators and hooks to interact with AWS services
     - S3Hook, S3FileTransferOperator - reading/writing data in s3
     - GlueJobOperator 
     - RedshiftOperator, PostgressHook - load/query data in Redshift
     - LambdaInvokeFunctionOperator
     - KinesisFirehoseOperator - send data to Kinesis Firehsoe
   - Managed MWAA bs selfhosting (EC2/K8s)

3. When should you choose Airflow over AWS-native tools like Glue?
   
   - Use Airflow when
     - complex orchestration, conditional logic, external integration not natively supported by Glue
       - multi or hybrid cloud, a central tool
       - extensive monitoring/debugging at task level
       - open source and custom plugins for pipeline
   - Use Glue when
     - fully managed ETL, minimal infra
       - AWS ecosystem support
       - Cost optimization is priority with serverless approach

## Quiz: Real-Time Processing

1. What are the differences between Kinesis Streams and Firehose?
   
   - Kinesis Streams
     - Real time streaming capabilities
       - Developers have full control over data ingestion, processing and delivery pipelines
       - Requires custom apps (lambda/custom app) to process/deliver data
       - Data retention upto 7 days
   - Kinesis Firehose
     - Fully managed, data destination to S3, Redshift, ElasticSearch
       - Automates process/delivery without custom code
       - No retention of data

2. How can you use Kinesis for real-time machine learning?
   
   - Data ingestion: stream real time data
   - Processing pipeline (use lambda to process data)
   - Machine leraning integratiom (pass data to AWS SageMaker endpoint for realtime inference)
   - Use prediction for downstream apps

3. What are the key benefits of integrating Lambda with Kinesis?
   
   - Serverless,
   - Event-driven architecture
   - Pay as you go compute
   - Integrate with other services

## Quiz: Batch Processing

1. What are the advantages of using AWS Batch?
   - Fully managed scalable
   - Flexible resources spot/ec2 instances
   - Docker support
   - Integrates with AWS service

2. How can you optimize costs in AWS Batch pipelines?
   - Use spot instances
   - Optimize job query (high/low priority to allocate resouces)
   - Right sizing instance types
   - Batch scheduling
   - Minimize idle resources

3. Explain how S3 integrates with AWS Batch workflows.
   - Input/output storage
   - Data staging location 
   - Event-driven s3 to trigger Batch
   - Encryption at rest/transit

## Quiz: Security and Cost

1. How can IAM roles improve ETL pipeline security?

2. What are the best practices for cost-efficient Glue jobs?

3. How can encryption improve the security of ETL workflows?

## Quiz: Comparisons

1. What are the key differences between Glue and Airflow?

2. How does Kinesis compare to Kafka for real-time pipelines?

3. When should you choose AWS-native services over open-source frameworks?

## 

1. What are the differences between Kinesis Streams and Firehose?

2. How can you use Kinesis for real-time machine learning?

3. What are the key benefits of integrating Lambda with Kinesis?
