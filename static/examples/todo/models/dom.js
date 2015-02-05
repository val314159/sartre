function TDL_DOM(id){
    var self=(this===window)?Object.create(TDL_DOM.prototype):this;
    self.id = id;
    self.arrElt = $E(id);
    return self;
}
TDL_DOM.prototype={
    $Description:function(id,v){
	var elt=$E(id+'>[name="value"]');
	if (U(v))	  return(elt.value);
	elt.value = v;
    },
    $Complete:function(id,v){
	var elt = $E(id+'>[name="complete"]');
	if (U(v))   return(elt.checked);
	var elt2= $E(id+'>[name="value"]');
	elt.checked = v ? true : false;
	elt2.style['text-decoration']=v?"line-through":"";
    },
    Update:function(k,id,v){ this[k]('$'+id,v); }, // dispatch
    Create:function(id){
	var self=this;
	var newElt=document.createElement('li');
	renderElt('todo_item0', newElt,{id: nextId()});
	self.arrElt.appendChild(newElt);
    },
    Delete:function(id){
	var elt = $E('#'+id);
	var node = elt.parentNode;
	node.parentNode.removeChild(node);
    }};
