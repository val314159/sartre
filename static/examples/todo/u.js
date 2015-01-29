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
////// Template stuff (Handlebars)
