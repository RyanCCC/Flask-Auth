# Flask-HTTPAuth

使用Flask-HTTPAuth+PostGrepsql实现接口的token验证和权限管控

### Flask-HttPAuth

[Welcome to Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)

1. Basic authentication examples


The function decorated with the verify_password decorator receives the username and password sent by the client. If the credentials belong to a user, then the function should return the user object. If the credentials are invalid the function can return None or False. The user object can then be queried from the current_user() method of the authentication instance.

```python

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()

```

2. Digest authentication example
 
```python

from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.username())

if __name__ == '__main__':
    app.run()

```
By default, Flask-HTTPAuth stores the challenge data in the Flask session. To make the authentication flow secure when using session storage, it is required that server-side sessions are used instead of the default Flask cookie based sessions, as this ensures that the challenge data is not at risk of being captured as it moves in a cookie between server and client. The Flask-Session and Flask-KVSession extensions are both very good options to implement server-side sessions.

As an alternative to using server-side sessions, an application can implement its own generation and storage of challenge data. To do this, there are four callback functions that the application needs to implement:

```python

@auth.generate_nonce
def generate_nonce():
    """Return the nonce value to use for this client."""
    pass

@auth.generate_opaque
def generate_opaque():
    """Return the opaque value to use for this client."""
    pass

@auth.verify_nonce
def verify_nonce(nonce):
    """Verify that the nonce value sent by the client is correct."""
    pass

@auth.verify_opaque
def verify_opaque(opaque):
    """Verify that the opaque value sent by the client is correct."""
    pass

```

3. Token Authentication Example 

```python

from flask import Flask, g
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()

```

4. API Document

class flask_httpauth.**HTTPBasicAuth**

> This class handles HTTP Basic authentication for Flask routes.

**\_\_init\_\_(scheme=None, realm=None)**
    
> Create a basic authentication object.  
>     
> If the optional scheme argument is provided, it will be used instead of the standard “Basic” scheme in the WWW-Authenticate response. A fairly common practice is to use a custom scheme to prevent browsers from prompting the user to login.
> 
>The realm argument can be used to provide an application defined realm with the WWW-Authenticate header.

**verify_password**(verify_password_callback)

> If defined, this callback function will be called by the framework to verify that the username and password combination provided by the client are valid. The callback function takes two arguments, the username and the password. It must return the user object if credentials are valid, or True if a user object is not available. In case of failed authentication, it should return None or False. Example usage:
          
```python
@auth.verify_password
  def verify_password(username, password):
    user = User.query.filter_by(username).first()
    if user and passlib.hash.sha256_crypt.verify(password, user.password_hash):
        return user
```

**get_user_roles(roles_callback)**

>If defined, this callback function will be called by the framework to obtain the roles assigned to a given user. The callback function takes a single argument, the user for which roles are requested. The user object passed to this function will be the one returned by the verify_callback function. The function should return the role or list of roles that belong to the user. Example:

```python
@auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()
```

**get_password(password_callback)**

> Deprecated This callback function will be called by the framework to obtain the password for a given user. Example:

```python
@auth.get_password
def get_password(username):
    return db.get_user_password(username)
```

**hash_password(hash_password_callback)**

>Deprecated If defined, this callback function will be called by the framework to apply a custom hashing algorithm to the password provided by the client. If this callback isn’t provided the password will be checked unchanged. The callback can take one or two arguments. The one argument version receives the password to hash, while the two argument version receives the username and the password in that order. Example single argument callback:

```python
@auth.hash_password
def hash_password(password):
    return md5(password).hexdigest()
    
@auth.hash_password
def hash_pw(username, password):
    salt = get_salt(username)
    return hash(password, salt)


```

**error_handler(error_callback)**

> If defined, this callback function will be called by the framework when it is necessary to send an authentication error back to the client. The function can take one argument, the status code of the error, which can be 401 (incorrect credentials) or 403 (correct, but insufficient credentials). To preserve compatiiblity with older releases of this package, the function can also be defined without arguments. The return value from this function must by any accepted response type in Flask routes. If this callback isn’t provided a default error response is generated. Example:

```python

@auth.error_handler
def auth_error(status):
    return "Access Denied", status

```

**login_required(view_function_callback)**

> This callback function will be called when authentication is successful. This will typically be a Flask view function. Example:

```python
@app.route('/private')
@auth.login_required
def private_page():
    return "Only for authorized people!"

@app.route('/private')
@auth.login_required(role='admin')
def private_page():
    return "Only for admins!"


```

**current_user()**

```python

@app.route('/')
@auth.login_required
def index():
    user = auth.current_user()
    return "Hello, {}!".format(user.name)

```

**username()**

```python
@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.username())
```


**class flask_httpauth.HTTPDigestAuth**

> This class handles HTTP Digest authentication for Flask routes. The SECRET_KEY configuration must be set in the Flask application to enable the session to work. Flask by default stores user sessions in the client as secure cookies, so the client must be able to handle cookies. To make this authentication method secure, a session interface that writes sessions in the server must be used.

**__init__(self, scheme=None, realm=None, use_ha1_pw=False)**

> Create a digest authentication object.
> 
> If the optional scheme argument is provided, it will be used instead of the “Digest” scheme in the WWW-Authenticate response. A fairly common practice is to use a custom scheme to prevent browsers from prompting the user to login.
> 
> The realm argument can be used to provide an application defined realm with the WWW-Authenticate header.
> 
> If use_ha1_pw is False, then the get_password callback needs to return the plain text password for the given user. If use_ha1_pw is True, the get_password callback needs to return the HA1 value for the given user. The advantage of setting use_ha1_pw to True is that it allows the application to store the HA1 hash of the password in the user database.

**generate_ha1(username, password)**

> Generate the HA1 hash that can be stored in the user database when use_ha1_pw is set to True in the constructor.

**generate_nonce(nonce_making_callback)**

> If defined, this callback function will be called by the framework to generate a nonce. If this is defined, verify_nonce should also be defined.
> 
> This can be used to use a state storage mechanism other than the session.

**verify_nonce(nonce_verify_callback)**

> If defined, this callback function will be called by the framework to verify that a nonce is valid. It will be called with a single argument: the nonce to be verified.
> 
> This can be used to use a state storage mechanism other than the session.

**generate_opaque(opaque_making_callback)**

>If defined, this callback function will be called by the framework to generate an opaque value. If this is defined, verify_opaque should also be defined.
>
>This can be used to use a state storage mechanism other than the session.

**verify_opaque(opaque_verify_callback)**

> If defined, this callback function will be called by the framework to verify that an opaque value is valid. It will be called with a single argument: the opaque value to be verified.
> 
> This can be used to use a state storage mechanism other than the session.

**get_password(password_callback)**

> See basic authentication for documentation and examples.

**get_user_roles(roles_callback)**

> See basic authentication for documentation and examples.

**error_handler(error_callback)**

> See basic authentication for documentation and examples.

**login_required(view_function_callback)**

> See basic authentication for documentation and examples.

**current_user()**

> See basic authentication for documentation and examples.

**username()**

> See basic authentication for documentation and examples.

**class flask_httpauth.HTTPTokenAuth**

> This class handles HTTP authentication with custom schemes for Flask routes.

**__init__(scheme='Bearer', realm=None, header=None)**

> Create a token authentication object.
> 
> The scheme argument can be use to specify the scheme to be used in the WWW-Authenticate response. The Authorization header sent by the client must include this scheme followed by the token. Example:
> 
> Authorization: Bearer this-is-my-token 
> The realm argument can be used to provide an application defined realm with the WWW-Authenticate header.
> 
> The header argument can be used to specify a custom header instead of Authorization from where to obtain the token. If a custom header is used, the scheme should not be included. Example:
> 
> X-API-Key: this-is-my-token

**verify_token(verify_token_callback)**

> This callback function will be called by the framework to verify that the credentials sent by the client with the Authorization header are valid. The callback function takes one argument, the token provided by the client. The function must return the user object if the token is valid, or True if a user object is not available. In case of a failed authentication, the function should return None or False. Example usage:

```python
@auth.verify_token
def verify_token(token):
    return User.query.filter_by(token=token).first()
```

> Note that a verify_token callback is required when using this class.

**get_user_roles(roles_callback)**

> See basic authentication for documentation and examples.

**error_handler(error_callback)**

>See basic authentication for documentation and examples.

**login_required(view_function_callback)**

> See basic authentication for documentation and examples.

**current_user()**

> See basic authentication for documentation and examples.

**class flask_httpauth.HTTPMultiAuth**

> This class handles HTTP authentication with custom schemes for Flask routes.

**__init__(auth_object, ...)**

> Create a multiple authentication object.
> 
> The arguments are one or more instances of HTTPBasicAuth, HTTPDigestAuth or HTTPTokenAuth. A route protected with this authentication method will try all the given authentication objects until one succeeds.

**login_required(view_function_callback)**

> See basic authentication for documentation and examples.

**current_user()**

> See basic authentication for documentation and examples.

### Flask-SQLAlchemy

### OAuth2


### 参考

1. [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)
2. [Flask-HTTPAuth-Document](https://flask-httpauth.readthedocs.io/en/latest/)
3. [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
4. [Flask应用](https://www.dreamer.im/tags/Flask/)
5. [How to Build an OAuth Service using Python, Flask, Postgres and JWT](https://www.grizzlypeaksoftware.com/articles?id=5SCpQMgookgKNtupzNHg9K)
6. [Flask与Vue的token认证](https://www.shangmayuan.com/a/82f95b1aaf6b4fd5a661d5f7.html)
7. [Flask-user](https://github.com/caitinggui/flask-user)
8. [Flask-oauthlib](https://github.com/lepture/flask-oauthlib)
