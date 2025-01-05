### Quiz: OAuth 2.0 Flows

1. Which OAuth 2.0 flow is most secure for web apps?
   
   - **Authorization Code Flow** is the most secure for web apps because the authorization code is exchanged server-side, keeping sensitive tokens away from the front end.

2. Why is the Implicit Flow less secure than the Authorization Code Flow?
   
   - **Implicit Flow** is less secure because the access token is returned directly to the browser, increasing the risk of token leakage through URL exposure or interception.

3. In which scenario would you use the Client Credentials Flow?
   
   - **Client Credentials Flow** is used for machine-to-machine communication where no user is involved, such as backend services accessing APIs directly.

### Quiz: **OAuth 2.0 Flows**

1. How does OIDC differ from OAuth 2.0?
   
   OIDC extends OAuth 2.0 by adding an identity layer, enabling authentication in addition to OAuth 2.0's authorization capabilities. While OAuth 2.0 grants applications access to resources, OIDC allows the verification of a user's identity and provides ID tokens with user details.

2. What kind of information is included in an ID Token?
   
   An ID Token contains user profile information such as the user's name, email, and unique identifier (subject). It also includes metadata like the token's issue time, expiration, and the issuer's details.

3. How can OIDC enable Single Sign-On (SSO)?
   
   OIDC enables Single Sign-On by allowing users to authenticate once with an identity provider and access multiple applications without logging in again. The ID token, which carries identity information, can be reused across different client applications within the same trust domain.

### Quiz: Security Features

1. Why is token expiry important?
   
    Token expiry limits the window of opportunity for malicious use if a token is     compromised. By enforcing short-lived tokens, applications reduce the risk of unauthorized access and ensure users periodically re-authenticate, enhancing overall security.

2. How does PKCE improve OAuth 2.0 security?
   
    PKCE (Proof Key for Code Exchange) prevents authorization code interception attacks by introducing a dynamically generated code challenge. This ensures that even if an authorization code is intercepted, it cannot be exchanged for a token without the original code verifier, adding an extra layer of security for public clients.

3. What are common scopes in OIDC authentication?
   
    Common scopes in OIDC include:
- openid – Required for OIDC, requests ID token.

- profile – Access to basic user information (name, family name, etc.).

- email – Access to user's email address.

- address – Access to user's address.

- phone – Access to user's phone number.
