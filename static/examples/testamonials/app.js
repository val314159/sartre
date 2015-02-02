function ping(){
    var access_token = readCookie('access_token');
    rpc_send("ping",["Hello, world"],function(data){
	    console.log("PING RESPONSED TO!!!!"+str(data));
	    document.getElementById('pong').innerHTML = "pong:"+access_token;
	});
}
function LOG(msg,typ) {
    typ = typ || 'info';
    $('#log').prepend("<p class='alert alert-dismissable small alert-"+typ+"' role='alert'>"+
		      '<button type="button" class="close" data-dismiss="alert">×</button>'+
		      msg+
		      "</p>");
}
function QUOTE(msg,who,title,id) {
    // use this for others' comments
    LOG("Q1");
    var xstr="<blockquote id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
}
function QUOTE2(msg,who,title,id) {
    // use this for my comments
    var id2 = id+'__edit';
    var id3 = id+'__who';
    LOG("id2=["+id2+"]");
    var xstr="<blockquote class='blockquote-reverse' id='"+id+
	"'>&ldquo;<span id='"+id2+"' contentEditable='true' style='background:cyan'>"+msg+"</span>&rdquo;"+
	"<footer><cite><abbr contentEditable='true' id='"+id3+"' title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
    setTimeout(function(){
	$('#'+id2).focus();
	$('#'+id2).blur(function(){
	    LOG("BLUR IT");
	    var msg = $('#'+id2).html();
	    var who = $('#'+id3).html();
	    LOG("BLUR IT1["+id2+"]");
	    LOG("BLUR IT1["+id3+"]");
	    rpc_send("pub",["Testamonials",{msg:msg,who:who}],function(data){
		console.log("PUB RESPONSED TO!!!!"+str(data));
		///document.getElementById('pong').innerHTML = "pong:"+access_token;
	    });

	});
    },500);
}
///
function sub(chlist) {
    rpc_send("sub",[chlist],function(data){
	console.log("SUB RESPONSED TO!!!!"+str(data));
	///document.getElementById('pong').innerHTML = "pong:"+access_token;
    });
}
function pub(ch,msg) {
    rpc_send("pub",[ch,msg],function(data){
	console.log("PUB RESPONSED TO!!!!"+str(data));
	///document.getElementById('pong').innerHTML = "pong:"+access_token;
    });
}
///
function add_to_convo(x,y,z){
    QUOTE2("It's great!!!","Random User","Anonymous",nextId());
}

rpc_add_notify('pub',function(data) {
    console.log("PUBBBBB"+str(data));
    var params = data.params;
    LOG("New Pub: "+str(params));
});

rpc_add_notify('testimonial',function(data) {
	console.log("TESTIMONAIL:"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('fortune').innerHTML = result;
    });
rpc_add_open(function(){
    var access_token = readCookie('access_token');
    document.getElementById('access_token').innerHTML = access_token;

    rpc_send("ping",["Hello, world"],function(data){
		console.log("PING RESPONSED TO!!!!"+str(data));
	    });
    sub(['Testamonials']);
    });
