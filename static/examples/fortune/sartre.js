function str(x){return JSON.stringify(x)}
///
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert alert-dismissable small alert-"+typ+"' role='alert'>"+
		      '<button type="button" class="close" data-dismiss="alert">×</button>'+
		      msg+
		      "</p>");
}
function login(){
    function get_u(){return document.getElementById("u").value}
    function get_p(){return document.getElementById("p").value}
    console.log("LOGIN");
    $("#xxx").click();
    LOG("Try Logging in");
    var args="?u="+get_u()+"&p="+get_p();
    //var xbase="s://localhost:7443";
    var xbase="://localhost:7080";
    var url="http"+xbase+"/auth/grant"+args;
    console.log("URL:"+url);
    LOG("Try Logging in to "+url);
    function done(a,b,c){
	LOG("Success Logging in","success");
	var j=JSON.parse(c.responseText);
	var access_token = AccessToken = j.access_token;
	createCookie('access_token',access_token,1);
	rpc_open(access_token);
    }
    function fail(a,b,c){
	LOG("Fail Logging in","danger");
	console.log("FAIL"+[a,b,c]);
    }
    $.ajax(url).done(done).fail(fail);
}
///
function unlog(){
    $('#log').html('');
}
function logout(){
    LOG("log out how?",'warning');
}
////////////
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
////////////
function fortune(){
    rpc_send("motd",[]);
    LOG("Please sir may I have another (fortune)?");
}
function ping(){
    var access_token = readCookie('access_token');
    rpc_send("ping",["Hello, world"],function(data){
	    console.log("PING RESPONSED TO!!!!"+str(data));
	    document.getElementById('pong').innerHTML = "pong:"+access_token;
	});
}
///
rpc_add_open(function(){
	var access_token = readCookie('access_token');
	document.getElementById('access_token').innerHTML = access_token;
	ping();
	fortune();
    });
rpc_add_notify('motd',function(data) {
	console.log("MOTD"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('motd').innerHTML = result;
    });
////////////
