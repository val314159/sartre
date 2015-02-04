function tApplication(){
    var self={};
    self.prototype = tApplication.proto;
    self.app=1;
    self.add_left_quote=function(msg,who,title,id) {
	// use this for others' comments
	var xstr="<blockquote id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	    "<footer><cite><abbr title="+title+">"+who+
	    "</abbr></cite></footer></blockquote>";
	$('#add_to').before(xstr);
    };
    self.add_right_quote=function(msg,who,title,id) {
	// use this for my comments
	var id2 = id+'__edit';
	var id3 = id+'__who';
	var xstr="<blockquote class='blockquote-reverse' id='"+id+
	    "'>&ldquo;<span id='"+id2+"' contentEditable='true' style='background:cyan'>"+msg+"</span>&rdquo;"+
	    "<footer><cite><abbr contentEditable='true' id='"+id3+"' title='"+title+"'>"+who+
	    "</abbr></cite></footer></blockquote>";
	$('#add_to').before(xstr);
	setTimeout(function(){
	    $('#'+id2).focus();
	    $('#'+id2).blur(function(){
		var msg = $('#'+id2).html();
		var who = $('#'+id3).html();
		ps.pub("Testamonials",{msg:msg,who:who});
	    });
	},500);
    };
    self.add_to_convo=function(){
	self.add_right_quote("It's great!!!","Random User","Anonymous",nextId());
    };
    self.main=function(){
	$('#add_to').click(function(){
	    LOG("HI");
	    self.add_to_convo();return false;});

	// this pub function will get called for every piece of data coming in
	rpc_add_notify('pub',function(data) {
	    var params = data.params;
	    self.add_left_quote(params[0].msg,params[0].who,"Anonymous",nextId());
	});
	
	rpc_add_open(function(){
	    ps.sub(['Testamonials']);
	});
    };
    self.launch=function(){self.main();return self};
    return self;
}
