rpc_add_notify('motd',function(data) {
	console.log("MOTD"+str(data));
	document.getElementById('motd').innerHTML = data.result;
    });
