rpc_add_open(function(){
	rpc_send("ping",["Hello, world"],function(data){
		console.log("PING RESPONSED TO!!!!"+str(data));
	    });
	rpc_send("motd",["Hello, world"]);
    });
rpc_add_notify('motd',function(data) {
	console.log("MOTD"+str(data));
	document.getElementById('motd').innerHTML = data.result;
    });
