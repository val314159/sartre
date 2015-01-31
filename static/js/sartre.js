// from http://stackoverflow.com/questions/1458724/how-to-set-unset-cookie-with-jquery
function createCookie(name, value, days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
}
function readCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}
function eraseCookie(name) {
    createCookie(name, "", -1);
}
///
function str(x){return JSON.stringify(x)}
///
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert alert-dismissable small alert-"+typ+"' role='alert'>"+
		      '<button type="button" class="close" data-dismiss="alert">×</button>'+
		      msg+
		      "</p>");
}
///
function login(){
    console.log("LOGIN");
    var u=document.getElementById("u").value;
    var p=document.getElementById("p").value;
    $("#xxx").click();
    LOG("Try Logging in");
    var args="?u="+u+"&p="+p;
    // var xbase="s://localhost:7443";
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
    rpc_close();
    document.getElementById('access_token').innerHTML = 'unknown';
    createCookie('access_token','',1);    
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
	    console.log("erred out:"+e);
	}
    };
    ws.ReloadPage=function(){
	ws.close();
	location.reload();
    };
    return ws;
}
////////////
