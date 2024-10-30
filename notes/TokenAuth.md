## Learning Objectives

- The students should be able to apply the concepts of authentication and authorization in API development, using techniques such as JWT.
- The students should be able to understand  secure APIs, preventing common vulnerabilities like SQL injection attacks, forging JWT.
- The students should be able to analyze and implement best practices for securing APIs, including encryption, access control.

### **JWT User Authentication**

JSON Web Tokens (JWT) is a popular method for user authentication in APIs. A JWT is a compact, URL-safe token that contains claims, which are pieces of information about the user (e.g., their username or role). JWTs are signed with a secret key, which means that they can be verified as authentically generated form our server.

### How JWT works?

1. **Send a POST request to the authentication server**: The client sends a POST request with user credentials (email/username and passowrd).
2. **Verify Credentials**: The server checks if credentials are valid.
3. **Create JWT**: If valid, the server creates a JWT with user details.
4. **Send JWT to Client**: The server sends the JWT back to the client.
5. **Send JWT to Resources Server**: The client sends the JWT to access resources.
6. **Verify JWT**: The resource server verifies the JWT's authenticity.
7. **Access Granted**: If valid, the resource server grants access.
8. **Access Denied**: If invalid, access is denied.

#### Implementing JWT

```
pip install pyjwt
```

Add a `utils` folder and a util.py file, here we'll set up functions to create (encode_token()) and validate tokens

##### Create a login route:
- login service to query db for customer with matching username and password, if customer, encode_token() and return it to the controller
- login controller recieves username and password via POST request and sends them to login service. I token return token, else return error
- login route is a POST route expecting a payload:
```
{
    "username": <some username>,
    "password": <some password>
}
```

### Implementing Access Control
Now that we've implemented tokens, we can require that our users have one in order to use/access particular resources.

To do this we are going to create a `@token_required` wrapper that we can place over our functions to enforce access control

Back in util.py we'll create our wrapper to:
- check an see if the requests include `Authorization` in the hearders
- Decode the token
- Check the Expiration Signature of the token
- Validate the token

If all of those checks pass the wrapper will run the wrapped function, if not we will return a response code of 401 Unauthorized

#### Implementing Role-Based Access Control

In order to have role-based access control we have to have roles! So we're going to add a role field to our Member model, where we will be able to set members as `admin` or `general` members.

We can now embed this information into the tokens we make just like we did with `member_id` and set up a wrapper `@admin_required` That not only checks the validates the token, but confirms that the role embedded in the token is the `admin` role.
