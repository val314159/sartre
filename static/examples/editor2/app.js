function EditorApplication(){
    var self={};
    self.app=1;
    self.launch=function(){self.main();return self};
    self.main=function(){
	$('#saveButton').click(self.saveFile);
	$('#revertButton').click(self.revertFile);
	$('#tree').treeview({data:[{text:"Not Loaded"}],levels:0,
			     onNodeSelected:function(event,node){
				 LOG("click:"+str(node));
				 if (node.data.cb) node.data.cb(event,node);
			     }});
	rpc_add_open(function(){
	    fs.walk(function(tree) {
		$('#tree').treeview({data:tree,levels:0});
	    });
	});
    };
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
    self.saveFile=function(){

	alert("XX:"+str(editor.getValue()));

	var fname=$('#dirname').html()+'/'+$('#filename').html();
	LOG("Save:"+str(fname));
	//var text=html2text($('#filebuf').html());
	var text=editor.getValue();
	LOG("Text:"+str(text));
	fs.save(fname,text,function(){
	    LOG("Saved.");
	});
    };
    self.loadFile=function(filename){
	LOG("PICKED A FILE "+filename);
	fs.load(filename,function(data){
	    LOG("OK GOT IT:1:"+str(data.result));
	    //var newText=text2html(data.result.data);
	    $( '#dirname'  ).html(data.result.dirname);
	    $( '#filename' ).html(data.result.filename);
	    //$( '#filebuf'  ).html(newText);
	    editor.setValue(data.result.data);
	});
    };
    self.revertFile=function(){
	var fname=$('#dirname').html()+'/'+$('#filename').html();
	self.loadFile(fname);
    };
    return self;
}

