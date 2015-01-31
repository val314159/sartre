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
    var xstr="<blockquote id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
}
function QUOTE2(msg,who,title,id) {
    var xstr="<blockquote class='blockquote-reverse' id='"+id+"'>&ldquo;"+msg+"&rdquo;"+
	"<footer><cite><abbr title="+title+">"+who+
	"</abbr></cite></footer></blockquote>";
    $('#testimonials').append(xstr);
}
///
rpc_add_open(function(){
	var access_token = readCookie('access_token');
	document.getElementById('access_token').innerHTML = access_token;
	ping();
    });
rpc_add_notify('testimonial',function(data) {
	console.log("TESTIMONAIL:"+str(data));
	var result = data.result.replace(/\n/g,'<br>');
	LOG("New Fortune: "+str(result),'success');
	document.getElementById('fortune').innerHTML = result;
    });
rpc_add_open(function(){
	rpc_send("ping",["Hello, world"],function(data){
		console.log("PING RESPONSED TO!!!!"+str(data));
	    });
    });
