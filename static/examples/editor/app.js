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
			     loadFile(path +'/'+ val);
			 }}});
    });
    return acc;
}

var fs={
    load:function(filename,cb){
	rpc_send("fs_load",[filename],function(data){
	    console.log("LOAD RESPONSED TO!!!!"+str(data));
	    cb(data);
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
	    Tree = [{text:'Remote fs',nodes:transmogrify(data.result,'fs',[])}];
	    renderFn();
	});
    }
};
///
rpc_add_open(function(){
    fs.walk(renderTree);
});
///
var Tree = [{text:"Not Loaded"}];
function renderTree() {
    $('#tree').treeview({data:Tree,levels:0,
		onNodeSelected:function(event,node){
		LOG("click:"+str(node));
		if (node.data.cb) node.data.cb(event,node);
	    }});
}
function text2html(text){
    text = text.replace(/\&/g,'&amp;');
    text = text.replace(/\>/g,'&gt;');
    text = text.replace(/\</g,'&lt;');
    return text;
}
function html2text(text){
    text = text.replace(/&lt;/g,'<');
    text = text.replace(/&gt;/g,'>');
    text = text.replace(/&amp;/g,'&');
    return text;
}
function saveFile(){
    var fname=$('#dirname').html()+'/'+$('#filename').html();
    LOG("Save:"+str(fname));
    var text=html2text($('#filebuf').html());
    LOG("Text:"+str(text));
    fs.save(fname,text,function(){
	LOG("Saved.");
    });
}
function loadFile(filename){
    LOG("PICKED A FILE "+filename);
    fs.load(filename,function(data){
	LOG("OK GOT IT:1:"+str(data.result));
	var newText=text2html(data.result.data);
	$( '#dirname'  ).html(data.result.dirname);
	$( '#filename' ).html(data.result.filename);
	$( '#filebuf'  ).html(newText);
    });
}
function revertFile(){
    var fname=$('#dirname').html()+'/'+$('#filename').html();
    loadFile(fname);
}
renderTree();
