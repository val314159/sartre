function ToDoList(id){
    this.arrElt = $E(id);
}
var PUB = {
    Create: function(obj){
	rpc_send("dbCreate",[obj],function(data){
	    LOG("::CREATED::");
	    console.log(data);
	});
    },
    Read  : function(obj,cb){
	rpc_send("dbRead",[obj],function(data){
	    LOG("::READ::");
	    console.log(data);
	    cb(data);
	});
    },
    Update: function(obj){
	rpc_send("dbUpdate",[obj],function(data){
	    LOG("::UPDATED::");
	    console.log(data);
	});
    },
    Delete: function(obj){
	rpc_send("dbDelete",[obj],function(data){
	    LOG("::DELETED::");
	    console.log(data);
	});
    }};
ToDoList.prototype = {
    $$Description: function(id,desc){
	console.log("$$Description"+id+desc);
	var elt=$E(id+'>[name="value"]');
	if (U(desc))	  return(elt.value);
	elt.value = desc;
	PUB.Update({id:id,description:desc});
    },
    $$Complete: function(id,complete){
	console.log("$$Complete"+id+complete);
	var elt = $E(id+'>[name="complete"]');
	if (U(complete))   return(elt.checked);
	var elt2= $E(id+'>[name="value"]');
	elt.checked = complete ? true : false;
	elt2.style['text-decoration']=complete?"line-through":"";
	PUB.Update({id:id,complete:complete});
    },
    Create: function(id){
	console.log("Create " + id);
	var newElt=document.createElement('li');
	renderElt('todo_item', newElt,
	    {id: nextId()});
	this.arrElt.appendChild(newElt);
	PUB.Create({id:id});
    },
    Delete: function(id){
	console.log("Delete " + id);
	var elt = $E(id);
	var node = elt.parentNode;
	node.parentNode.removeChild(node);
	PUB.Delete({id:id});
    }
};
var ToDo = new ToDoList('#todolist');

initTemplates();
rpc_add_open(function(){
});
console.log("////////////////////");
rpc_open('VALID');
