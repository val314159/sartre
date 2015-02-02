////////////
function fortune(){
    rpc_send("fortune",[]);
    LOG("Please sir may I have another (fortune)?");
}
function ping(){
    var access_token = readCookie('access_token');
    rpc_send("ping",["HW"],function(data){
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
rpc_add_notify('fortune',function(data) {
	console.log("FORTUNE"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('fortune').innerHTML = result;
    });
////////////
