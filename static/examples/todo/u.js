////// Basic Utils
function LOG(x){console.log(x)}
function str(x){return JSON.stringify(x)}
function $E(x){return document.querySelector(x)}
function $$(x){return document.querySelectorAll(x)}
function U(x){return x===undefined || x===null}
var _id=1000;
function nextId(){return"i"+(++_id)}
function EACH(arr,callback){for(var i=0;i<arr.length;++i)callback(arr[i],i)}
////// Template stuff (Handlebars)
var D=document;
function initTemplates() {
    EACH($$('script[type="hbs"]'),function(v){
	    Handlebars.registerPartial(v.id, v.innerHTML)} )}
function getTmpl(id){
    return Handlebars.compile($E('script[type="hbs"]#'+id).innerHTML)}
function renderPage(args){    document.write(getTmpl('body')(args))}
function renderElt(id, elt, args){    elt.innerHTML = getTmpl(id)(args)}
////// RPC stuff
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
////// Sample Main stuff
function superMain(){
    if(!superMain.run_once){
	superMain.run_once = true;
	initTemplates();
	rpc_add_open(function(){
	    LOG("IM OPEN");
	});
	rpc_open('VALID');
    }
}
