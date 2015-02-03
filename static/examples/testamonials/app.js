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
///
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert alert-dismissable small alert-"+typ+"' role='alert'>"+
		      '<button type="button" class="close" data-dismiss="alert">×</button>'+
		      msg+"</p>");
}

function add_left_quote(msg,who,title,id) {
    // use this for others' comments
    var xstr="<blockquote id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#add_to').before(xstr);
}
function add_right_quote(msg,who,title,id) {
    // use this for my comments
    var id2 = id+'__edit';
    var id3 = id+'__who';
    var xstr="<blockquote class='blockquote-reverse' id='"+id+
	"'>&ldquo;<span id='"+id2+"' contentEditable='true' style='background:cyan'>"+msg+"</span>&rdquo;"+
	"<footer><cite><abbr contentEditable='true' id='"+id3+"' title="+title+">"+who+
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
}
///
function add_to_convo(){
    add_right_quote("It's great!!!","Random User","Anonymous",nextId());
}

function start(){

    // this pub function will get called for every piece of data coming in
    rpc_add_notify('pub',function(data) {
	var params = data.params;
	add_left_quote(params[0].msg,params[0].who,"Anonymous",nextId());
    });

    rpc_add_open(function(){
	ps.sub(['Testamonials']);
    });
    return this;
}

start();
