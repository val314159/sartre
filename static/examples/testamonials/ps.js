var ps={
    sub:function(chlist) {
	rpc_send("sub",[chlist],function(data){
	    console.log("SUB RESPONSED TO!!!!"+str(data));
	});
    },
    pub:function(ch,msg) {
	rpc_send("pub",[ch,msg],function(data){
	    console.log("PUB RESPONSED TO!!!!"+str(data));
	});
    }
};
