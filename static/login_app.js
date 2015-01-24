function get_u(){return document.getElementById("u").value}
function get_p(){return document.getElementById("p").value}
function another_one(){
    rpc_send("motd",["Hello, world2"]);
    LOG("Please sir may I have another!");
}
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert small alert-"+typ+"' role='alert'>"+msg+"</p>");
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
	console.log("DONE"+[a,b,c]);
	console.log("DONE"+[a,b,c.responseText]);
	console.log("DONE"+[a,b,JSON.parse(c.responseText)]);
	var j=JSON.parse(c.responseText);
	var access_token = AccessToken = j.access_token;
	createCookie('qwert','yuiop',1);
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
	document.getElementById('access_token').innerHTML = readCookie('access_token');
	
	rpc_send("ping",["Hello, world"],function(data){
		console.log("PING RESPONSED TO!!!!"+str(data));
		document.getElementById('pong').innerHTML = "pong:"+readCookie('access_token');
	    });
	rpc_send("motd",["Hello, world"]);
    });
rpc_add_notify('motd',function(data) {
	console.log("MOTD"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('motd').innerHTML = result;
    });
