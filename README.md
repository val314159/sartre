# Sartre
Sartre - An existential framework.  It doesn't get in your way; it just _is_.

### Includes:

- Authenticity: A Standalone Token-based Authentication Server Framework (sorta OAuth-ishy)
- RPC Javascript->Python
- Remote Filesystem w/Editor
- Pub/Sub
- Key/Value Store

---
## Quickstart

### To install:

```
sh install.sh
```

or 

```
source install.sh
```

or 

```
. install.sh
```

### To run:

#### Just the auth server:

```
python -mauthenticity.wsgi_auth
```

#### Just the websocket server:

```
python -mauthenticity.ws
```

(actually the websocket server serves up
	   <a href="http://localhost:8080/static/index.html">
	   static files</a>, too)

- <a href="http://localhost:8080/static/main.html">Main Page</a>
- <a href="http://localhost:8080/static/examples/index.html">Examples</a>
- <a href="http://localhost:8080/static/readme.html">README</a>

---

## Authenticity - _Authentication Server_

Designed to be a mostly-dependency free, standalone, token-based authentication server that's sorta OAuth-ishy.  Since OAuth is more of a guideline instead of a protocol, interop doesn't really exist.

Originally, I used bottle for this but I eventually just used straight WSGI for ease of use.

Authenticity uses a pluggable backend.  It defaults to an in-memory backend.

Standalone: exists in its own package, seperate from the rest of sartre.

### User Interface

These two will be the most frequently used calls:

#### /auth/grant?u=[username]&p=[password]
#### grant(u,p)
- u = username
- p = password

  If you authenticate, returns (access_token,username,userinfo)

  If you fail, returns ('','',{})

#### /auth/valid?t=[accesstoken]&g=[groupname]
#### valid(t,g)
- t = access token
- g = group name

  Returns: [bool] whether your token is authorized for the group *group name*

These two are used less often:

#### /auth/revoke?t=[token]
#### revoke(t)
- t = token

  What the auth server giveth, it can also taketh away.
   *Note*: _This just invalidates the token,
    it doesn't end sessions or free any other resources._

  Returns: {}

#### /auth/info?t=[token]
#### info(t)
- t = token

  Reget the user info using the token.

### Plug-in Interface

You can use this to switch backends (Auth objects)

#### set_auth(a)
- a = auth object

  sets the default backend (Auth object) to _a_

  returns: None

#### get_auth()

  Returns: default backend (Auth object)


### Admin Interface

#### createUser(obj)

*TBD*

#### readUsers(filter)

*TBD*

#### updateUser(obj)

*TBD*

#### deleteUser(filter)

*TBD*

---

## RPC Javascript->Python

- JSON-RPC2 influenced protocol
- uses websockets
- async

## Remote Filesystem w/Editor

- load(filename)
- save(filename,filedata)

## Pub/Sub

- pub(channel,message)
- sub(channellist)
