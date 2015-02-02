var _tree = [{text:"Not Loaded"}];
function getTree() {
    // Some logic to retrieve, or generate tree structure
  return _tree;
}
function regetTree() {
    $('#tree').treeview({data: getTree(),levels:0});
}
function xregetTree() {
    $('#tree').treeview({data:getTree(),levels:0,
		onNodeSelected:function(event,node){
		LOG("click:"+str(node));
		if (node.data.cb) node.data.cb(event,node);
	    }});
}
function fs_walk() {
    rpc_send("fs_walk",["fs"],function(data){
	    var map = data.result;
	    function findlist(path,acc){
		if (!map[path]) return;
		var dirs = map[path][0];
		var files= map[path][1];
		$.each(dirs,function(ndx,val){
			LOG("D:"+path+'/'+val);
			var nodes = findlist(path+'/'+val,[]);
			acc.push({text:val+'/',nodes:nodes,
				    data:{t:'d',p:path,f:val} });
		    });
		$.each(files,function(ndx,val){
			LOG("F:"+path+'/'+val);
			acc.push({ text: val, data:{t:'f',p:path,f:val,
					cb:function(){
					loadFile(path +'/'+ val);
				    }}});
		    });
		return acc;
	    }
	    var lst = findlist('fs',[]);
	    LOG("LST:"+str(lst));
	    _tree = [{text:'Remote fs',nodes:lst}];
	    regetTree();
	});
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
    var text=html2text($('#filebuf').html());
    save(fname,text,function(){
	    LOG("Saved.");
	});
}
function loadFile(filename){
    LOG("PICKED A FILE "+filename);
    load(filename,function(data){
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
xregetTree();
