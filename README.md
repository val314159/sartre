# authenticity
OAuth-ish Authentication Server Framework

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

(actually the websocket server serves up <a href="http://localhost:8080/static/index.html">static files</a>, too)
