# Answers to API Gateway

## 1.    What is the difference between REST and HTTP APIs in API Gateway?

Difference Between REST APIs and HTTP APIs in Amazon API Gateway

| **Feature**             | **REST APIs**                                                                                        | **HTTP APIs**                                                                 |
| ----------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Use Case**            | Suitable for traditional, feature-rich APIs with high customization needs.                           | Designed for simple, low-latency, and cost-efficient APIs.                    |
| **Protocol**            | Follows REST architecture and supports request/response structure.                                   | Supports both REST-like and other HTTP-based protocols.                       |
| **Performance**         | Higher latency due to feature-rich capabilities.                                                     | Lower latency, optimized for performance.                                     |
| **Pricing**             | More expensive; supports advanced features like caching and throttling.                              | Lower cost (up to 70% cheaper than REST APIs).                                |
| **Features**            | Includes API Gateway features such as request validation, transformations, caching, and usage plans. | Limited features; lacks caching and request/response transformations.         |
| **Authentication**      | Supports IAM, Lambda authorizers, and Amazon Cognito User Pools.                                     | Supports IAM, Lambda authorizers, and Amazon Cognito User Pools (simplified). |
| **WebSocket Support**   | Not supported.                                                                                       | Not supported (use WebSocket APIs for real-time communication).               |
| **Integration Options** | Lambda, HTTP backends, AWS services, and more.                                                       | Primarily focuses on Lambda and HTTP backends.                                |
| **Custom Domain Names** | Supports custom domains and edge-optimized endpoints.                                                | Supports custom domains with regional endpoints only.                         |
| **Target Workload**     | Ideal for complex, enterprise-grade APIs.                                                            | Ideal for lightweight, modern workloads requiring cost efficiency.            |

*Summary*

- **REST APIs**: Best suited for applications requiring advanced features and extensive API management.
- **HTTP APIs**: Best suited for cost-sensitive, lightweight, or high-performance use cases.

## 2.    How does API Gateway integrate with Cognito User Pools?

API Gateway Integration with Amazon Cognito User Pools

Amazon API Gateway integrates seamlessly with Amazon Cognito User Pools to provide user authentication and authorization for your APIs. Below is an overview of how the integration works and the steps to implement it.

*How It Works*

1. **User Authentication**:
   
   - API Gateway uses Amazon Cognito User Pools to authenticate users.
   - Users log in through the Cognito-hosted UI or your custom authentication mechanism and receive a JSON Web Token (JWT) as a credential.

2. **Authorization**:
   
   - API Gateway validates the JWT in incoming API requests.
   - It ensures that the token is issued by the associated Cognito User Pool and verifies the token's claims (e.g., user identity and permissions).

3. **Policy Enforcement**:
   
   - Based on the claims in the JWT, API Gateway can allow or deny access to specific resources or methods.

Steps to Integrate API Gateway with Cognito User Pools

1. **Set Up a Cognito User Pool**
   
   - Create a new Cognito User Pool.
   - Configure the user pool settings, such as users, attributes, and app clients.

2. **Configure the API Gateway**
   
   - In your API Gateway console:
     - Select your API and navigate to **Authorization**.
     - Create a new Cognito User Pool authorizer.
     - Associate the authorizer with your Cognito User Pool.
   - Specify which API methods require authentication via this authorizer.

3. **Secure API Endpoints**
   
   - Attach the Cognito User Pool authorizer to individual routes or methods in your API Gateway.
   - Define which scopes (e.g., `read`, `write`) are required for accessing each endpoint.

4. **Test the Integration**
   
   - Obtain a JWT by logging in as a user in your Cognito User Pool.
   - Include the JWT in the `Authorization` header of your API requests.
   - Test the API to ensure requests with valid tokens succeed and invalid requests are denied.

Benefits of Using Cognito with API Gateway

1. **Simplified User Management**:
   
   - Cognito handles user sign-up, sign-in, and account recovery.

2. **Token-Based Authentication**:
   
   - Secure APIs with standards-based authentication using JWTs.

3. **Access Control**:
   
   - Control access to specific resources or methods using claims in the JWT.

4. **Scalability**:
   
   - Handle millions of users and scale seamlessly with API Gateway and Cognito.

Example: Setting Up a Cognito Authorizer in API Gateway

*Create the Authorizer*

```bash
aws apigateway create-authorizer \
  --rest-api-id <api-id> \
  --name MyCognitoAuthorizer \
  --type COGNITO_USER_POOLS \
  --provider-arns arn:aws:cognito-idp:<region>:<account-id>:userpool/<user-pool-id>
```

## 3.    What factors impact the cost of using API Gateway?

Factors Impacting the Cost of Using Amazon API Gateway

The cost of using Amazon API Gateway depends on several factors, including the type of API, usage patterns, and additional features. Below is a breakdown of the primary factors that impact the cost:

1. **API Type**
   
   - **REST APIs**: Priced based on the number of API calls and data transfer out. REST APIs generally have a higher cost due to the comprehensive feature set.
   - **HTTP APIs**: Lower cost compared to REST APIs, making them ideal for simple use cases with fewer features.
   - **WebSocket APIs**: Priced based on the number of messages sent and received, connection duration, and API requests.

2. **Number of API Calls**
   
   - API Gateway charges based on the number of requests handled by the API.
   - The cost increases as the volume of API calls grows.

3. **Data Transfer**
   
   - Outbound data transfer from API Gateway incurs additional charges.
   - Large payloads or high-frequency requests can increase data transfer costs.

4. **Caching**
   
   - If caching is enabled using API Gateway's cache, costs are incurred based on:
     - Cache size (ranging from 0.5 GB to 237 GB).
     - Cache capacity and associated hourly charges.
   - Caching helps reduce backend processing costs but adds to API Gateway expenses.

5. **Latency and Regional Factors**
   
   - Costs vary by region; some AWS regions have different pricing structures.
   - Proximity of clients to the deployed API Gateway endpoints can impact performance and data transfer costs.

6. **Custom Domain Names**
   
   - Using custom domain names with API Gateway incurs an additional monthly charge.

7. **Security Features**
   
   - Enabling advanced security features like AWS WAF for protection against common web exploits can add to the cost.
   - Using authorization mechanisms like Cognito User Pools or Lambda authorizers also increases costs.

8. **Integration Type**
   
   - The type of backend integration (e.g., AWS Lambda, HTTP, VPC links) affects cost:
     - **Lambda Integrations**: Add the cost of Lambda invocations.
     - **VPC Links**: Charge based on the number of hours the VPC link is active.

9. **Throttling and Rate Limits**
   
   - If you exceed the free tier or configured limits, throttling and rate-limited requests may incur additional charges.

10. **Free Tier**
    
    - API Gateway offers a free tier, which includes:
      - 1 million API calls per month for REST or HTTP APIs.
      - 1 million messages for WebSocket APIs.
    - Exceeding the free tier will result in charges.

11. **Monitoring and Logging**
    
    - Enabling detailed CloudWatch metrics and logging increases CloudWatch costs.
    - Additional charges are incurred for data ingestion, storage, and retrieval.

Tips for Cost Optimization

- Use HTTP APIs instead of REST APIs for simple use cases.
- Optimize data transfer by reducing payload size.
- Enable caching only when necessary and choose an appropriate cache size.
- Monitor API usage and set throttling limits to avoid unnecessary costs.
- Leverage the free tier for testing and small-scale deployments.
