# Flask-HTTPAuth

使用Flask-HTTPAuth+MongoDB实现接口的token验证和权限管控

## HOW TO USE
1. 运行```app.py```，访问http://127.0.0.1:5000/swagger-ui.html 出现以下swagger ui界面：
![image](https://user-images.githubusercontent.com/27406337/138835289-cb3426b2-bc8f-4108-8906-5416edb94fd8.png)

2. 使用“注册新的用户信息”的接口，添加一个新的用户
成功即可返回“success”
![image](https://user-images.githubusercontent.com/27406337/138835820-54f6d52d-6027-4491-b3a2-626f152441c4.png)

3. 获取用户信息

![image](https://user-images.githubusercontent.com/27406337/138836808-1f943314-4b94-497c-adb4-83e14ab02ac0.png)

4. 调用loginin接口获取获取token

![image](https://user-images.githubusercontent.com/27406337/138836941-7f5f43e8-280a-4c3d-bb8d-7729676cf4ec.png)

5. 调用helloworld

![image](https://user-images.githubusercontent.com/27406337/138837108-6aca0bb1-5cea-4cff-8f9a-42fdade4e77a.png)


# 数据库

本项目中主要使用到的数据库有：mongodb、redis以及postgrepsql，详细可以分别参考我的博客：[python Nosql数据库操作](https://blog.csdn.net/u012655441/article/details/120761110)。


# Flask-HttPAuth

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

这个类似于EF，我还是不太喜欢用这个，例如操作pgsql直接用的是psycopg2，这样可以更加方便调试。

**一个简单的应用**

```python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# 创建数据库

from yourapplication import db
db.create_all()

# 创建用户

>>> from yourapplication import User
>>> admin = User('admin', 'admin@example.com')
>>> guest = User('guest', 'guest@example.com')

# 写入用户
>>> db.session.add(admin)
>>> db.session.add(guest)
>>> db.session.commit()

# 简单的关系

from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
```

**配置参数说明：**

| 配置 | 说明 |
|-------|------|
|SQLALCHEMY_DATABASE_URI| 用于连接数据的数据库。例如：sqlite:////tmp/test.db mysql://username:password@server/db|
|SQLALCHEMY_BINDS|	一个映射绑定 (bind) 键到 SQLAlchemy 连接 URIs 的字典。 更多的信息请参阅 绑定多个数据库。|
|SQLALCHEMY_ECHO|	如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。|
|SQLALCHEMY_RECORD_QUERIES	| 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。更多信息请参阅 get_debug_queries()。|
|SQLALCHEMY_NATIVE_UNICODE|	可以用于显式地禁用支持原生的 unicode。这是 某些数据库适配器必须的（像在 Ubuntu 某些版本上的 PostgreSQL），当使用不合适的指定无编码的数据库 默认值时。|
|SQLALCHEMY_POOL_SIZE|	数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。|
|SQLALCHEMY_POOL_TIMEOUT|	指定数据库连接池的超时时间。默认是 10。|
|SQLALCHEMY_POOL_RECYCLE|	自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时。|
|SQLALCHEMY_MAX_OVERFLOW|	控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。|
|SQLALCHEMY_TRACK_MODIFICATIONS|	如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。|

**连接URI格式**

```python
dialect+driver://username:password@host:port/database
```

**声明模型**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
```
| 类型 | 说明 |
|----|----|
|Integer|	一个整数|
|String (size)|	有长度限制的字符串|
|Text|	一些较长的 unicode 文本|
|DateTime	表示为 Python datetime 对象的 时间和日期|
|Float	存储浮点值|
|Boolean|	存储布尔值|
|PickleType	存储为一个持久化的 Python 对象|
|LargeBinary|	存储一个任意大的二进制数据|

**one to many**

```python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
                                lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
```


**many to many**


```python
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('pages', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

**API Document**

http://www.pythondoc.com/flask-sqlalchemy/api.html

# OAuth2

OAuth（开放授权）是一个开放标准，允许用户授权第三方移动应用访问他们存储在另外的服务提供者上的信息，而不需要将服务提供者上的用户的用户密码提供给第三方移动应用或分享他们数据的所有内容。

图来源：[OAuth2详解](https://www.jianshu.com/p/84a4b4a1e833)

![image](https://user-images.githubusercontent.com/27406337/131957491-83e44bd2-cb3b-49d1-9539-0b412aa63bc8.png)

QAuth运作流程：1. 用户（Resource Owner）打开客户端（User Agent），客户端要求用户给与第三方服务提供方（HTTP service）授权并附上client id和URI；2. 第三方服务提供方即授权方接收到请求后，向用户询问是否进行授权。方法是让用户提供用户名和密码。3. 用户同意授权后，授权方重定向到客户端提供和的URL并附上授权码（Authorization code）。4. 客户端拿到授权码后向认证服务端（Authorization server）申请令牌。5. 认证服务端确认客户端的请求无误后向客户端发放令牌。5. 客户端拿到令牌后即可在资源服务器（Resource server）申请资源。
![image](https://user-images.githubusercontent.com/27406337/131957778-a510b1f8-612e-4a4f-8795-bf7949bbef1f.png)

**授权模式**

- 授权码模式：功能最完整，流程最严密的授权模式
  
  （1）用户访问客户端，后者将前者导向认证服务器，假设用户给予授权，认证服务器将用户导向客户端事先指定的"重定向URI"（redirection URI），同时附上一个授权码。

  （2）客户端收到授权码，附上早先的"重定向URI"，向认证服务器申请令牌：GET /oauth/token?response_type=code&client_id=test&redirect_uri=重定向页面链接。请求成功返回code授权码，一般有效时间是10分钟。

  （3）认证服务器核对了授权码和重定向URI，确认无误后，向客户端发送访问令牌（access token）和更新令牌（refresh token）。POST /oauth/token?response_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA&redirect_uri=重定向页面链接。

- 简化模式
   
   ![image](https://user-images.githubusercontent.com/27406337/131958726-323aa05c-bd38-479f-84b8-0d2854309b61.png)

- 用户名密码模式

   ![image](https://user-images.githubusercontent.com/27406337/131958858-15670a81-dabc-4d87-b338-70c50ee801a7.png)

- 客户端模式
   
   ![image](https://user-images.githubusercontent.com/27406337/131958926-86ec360d-1067-4ea9-a4ab-8c1f2fc74982.png)

# 异步编程
对于Python的异步编程，我个人的想法是要么直接用python的关键字asyncio或者用一些组件如redis或者rabbitmq。

## asyncio

## redis

## rabbitmq





# 参考

1. [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth)
2. [Flask-HTTPAuth-Document](https://flask-httpauth.readthedocs.io/en/latest/)
3. [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
4. [Flask应用](https://www.dreamer.im/tags/Flask/)
5. [How to Build an OAuth Service using Python, Flask, Postgres and JWT](https://www.grizzlypeaksoftware.com/articles?id=5SCpQMgookgKNtupzNHg9K)
6. [Flask与Vue的token认证](https://www.shangmayuan.com/a/82f95b1aaf6b4fd5a661d5f7.html)
7. [Flask-user](https://github.com/caitinggui/flask-user)
8. [Flask-oauthlib](https://github.com/lepture/flask-oauthlib)
