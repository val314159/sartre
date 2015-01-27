function get_u(){return document.getElementById("u").value}
function get_p(){return document.getElementById("p").value}
function another_one(){
    rpc_send("motd",["Hello, world2"]);
    LOG("Please sir may I have another (fortune)?");
}
function ping(){
    var access_token = readCookie('access_token');
    rpc_send("ping",["Hello, world"],function(data){
	    console.log("PING RESPONSED TO!!!!"+str(data));
	    document.getElementById('pong').innerHTML = "pong:"+access_token;
	});
}
function load(filename,cb){
    rpc_send("load",[filename],function(data){
	    console.log("LOAD RESPONSED TO!!!!"+str(data));
	    cb(data);
	});
}
function save(filename,data){
    rpc_send("save",[filename,data],function(data){
	    console.log("LOAD RESPONSED TO!!!!"+str(data));
	    cb(data);
	});
}
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert alert-dismissable small alert-"+typ+"' role='alert'>"+
		      '<button type="button" class="close" data-dismiss="alert">×</button>'+
		      msg+
		      "</p>");
}
function QUOTE(msg,who,title,id) {
    var xstr="<blockquote id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
}
function QUOTE2(msg,who,title,id) {
    var xstr="<blockquote class='blockquote-reverse' id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
}
function login(){
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
rpc_add_open(function(){
	var access_token = readCookie('access_token');
	document.getElementById('access_token').innerHTML = access_token;
	ping();
	another_one();
	filesystem_walk();
    });
rpc_add_notify('motd',function(data) {
	console.log("MOTD"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('motd').innerHTML = result;
    });
