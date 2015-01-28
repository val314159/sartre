function ToDoList(id){
    this.arrElt = $E(id);
}
ToDoList.prototype = {
    $$Description: function(id,desc){
	console.log("$$Description"+id+desc);
	var elt=$E(id+'>[name="value"]');
	if (U(desc))	  return(elt.value);
	elt.value = desc;
    },
    $$Complete: function(id,complete){
	console.log("$$Complete"+id+complete);
	var elt = $E(id+'>[name="complete"]');
	if (U(complete))   return(elt.checked);
	var elt2= $E(id+'>[name="value"]');
	elt.checked = complete ? true : false;
	elt2.style['text-decoration']=complete?"line-through":"";
    },
    Create: function(id){
	console.log("Create " + id);
	var newElt=document.createElement('li');
	renderElt('todo_item', newElt,
	    {id: nextId()});
	this.arrElt.appendChild(newElt);
    },
    Delete: function(id){
	console.log("Delete " + id);
	var elt = $E(id);
	var node = elt.parentNode;
	node.parentNode.removeChild(node);
    }
};
var ToDo = new ToDoList('#todolist');

initTemplates();
