function str(x){return JSON.stringify(x)}
var xbase = "://localhost:8080";
//var xbase = "s://localhost:8443";
var obj = {};
var _id=0,callbacks={};
var _open=function(){};
function rpc_add_open(f){_open=f;}
function rpc_add_notify(method,fn){obj[method]=fn;}
function rpc_send(method,params,fn){
    var x={method:method,params:params};
    callbacks[x.id="id"+(_id++)]=fn;
    ws.send(str(x));
}
function rpc_close() {
    if (ws) ws.close();
}
function rpc_open(access_token) {
    ws = new WebSocket("ws"+xbase+"/websocket?t="+access_token);
    ws.onopen = function() {
	console.log("OPEN");
	_open();
    };
    ws.onerror = function() {
	console.log("ERR");
    };
    ws.onclose = function(x,y,z) {
	console.log("CLOSE"+[x,y,z]);
    };
    ws.onmessage = function(evt) {
	var data = JSON.parse(evt.data);
	data._ws = ws;
	var fn = callbacks[data.id] || obj[data.method];
	try {
	    if(fn) fn(data);
	    else console.log("not found");
	} catch(e) {
	    console.log("erred out");
	}
    };
    ws.ReloadPage=function(){
	ws.close();
	location.reload();
    };
    return ws;
}
