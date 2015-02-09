var fs={
    reboot:function(cb){
	rpc_send("fs_reboot",[],function(data){
	    console.log("REBOOT RESPONSED TO!!!! 1 ");
	    cb(data);
	    console.log("REBOOT RESPONSED TO!!!! 3 ");
	 });
     },
    load:function(filename,cb){
	rpc_send("fs_load",[filename],function(data){
	    console.log("LOAD RESPONSED TO!!!! 1 "+str(data));
	    cb(data);
	    console.log("LOAD RESPONSED TO!!!! 3 ");

	});
    },
    save:function(filename,data,cb){
	rpc_send("fs_save",[filename,data],function(data){
	    console.log("SAVE RESPONSED TO!!!!"+str(data));
	    cb(data);
	});
    },
    walk:function(renderFn) {
	rpc_send("fs_walk",["fs"],function(data){

	    function transmogrify(map,path,acc){
		if (!map[path]) return;
		var dirs = map[path][0];
		var files= map[path][1];
		$.each(dirs,function(ndx,val){
		    var nodes = transmogrify(map,path+'/'+val,[]);
		    acc.push({text:val+'/',nodes:nodes,
			      data:{t:'d',p:path,f:val} });
		});
		$.each(files,function(ndx,val){
		    acc.push({ text: val,
			       data:{t:'f',p:path,f:val,
				     cb:function(){
					 EditApp.loadFile(path +'/'+ val);
				     }}});
		});
		return acc;
	    }

	    renderFn([{text:'Remote fs',nodes:transmogrify(data.result,'fs',[])}]);
	});
    }
};
