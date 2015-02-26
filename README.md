# Sartre

[![Join the chat at https://gitter.im/val314159/sartre](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/val314159/sartre?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Sartre - An existential framework.  It doesn't get in your way; it just *is*.

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

#### Just the auth server: *ports 7080 and 7443*

```
python -mauthenticity.auth_core
```

#### Just the websocket server: *ports 8080 and 8443*

```
python -msartre.websvr
```

(actually the websocket server serves up
	   <a href="http://localhost:8080/static/index.html">
	   static files</a>, too)

- <a href="http://localhost:8080/static/main.html">Main Page</a>
- <a href="http://localhost:8080/static/examples/index.html">Examples</a>
- <a href="http://localhost:8080/static/readme.html">README</a>

---

## Authenticity - *Authentication Server*

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
   *Note*: *This just invalidates the token,
    it doesn't end sessions or free any other resources.*

  Returns: {}

#### /auth/info?t=[token]
#### info(t)
- t = token

  Reget the user info using the token.

### Plug-in Interface

You can use this to switch backends (Auth objects)

#### set_auth(a)
- a = auth object

  sets the default backend (Auth object) to *a*

  returns: None

#### get_auth()

  Returns: default backend (Auth object)


### Admin Interface

#### create_user(dict)

*TBD*

#### read_users(filter)

*TBD*

#### update_user(overlay)

*TBD*

#### delete_user(filter)

*TBD*

---

## RPC Javascript->Python

- JSON-RPC2 influenced protocol
- uses websockets
- async

## Remote Filesystem w/Editor

- load(filename)
- fs_load(filename)
- save(filename,filedata)
- fs_save(filename,filedata)
- filesystem_walk(filename,filedata)
- fs_walk(filename,filedata)

## Pub/Sub

- pub(channel,message)
- sub(channellist)
