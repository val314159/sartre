function TDL_Model(){
    var self=(this===window)?Object.create(TDL_Model.prototype):this;
    self.arr=[];
    self.ndx={};
    return self;
}
TDL_Model.prototype={
    Update:function(k,id,v){
	self.ndx[id][k]=v;
    },
    Create:function(id){
	var self=this;
	self.arr.push(self.ndx[id]={id:id});
    },
    Delete:function(id){
	var self=this;	
	var item = self.ndx[id];
	var pos = self.arr.indexOf(item);
	self.arr.splice(pos,1);
	self.ndx[id] = undefined;
    }};
