function TDL_App(eltId){
    var self=(this===window)?Object.create(TDL_App.prototype):this;
    superMain();
    return self;
}
TDL_App.prototype={
    Update:function(k,id,v){
	this.model.Update(k,id,v);
	this.dom.Update(k,id,v);
	this.svr.Update(k,id,v);
    },
    Create:function(id){
	this.model.Create(id);
	this.dom.Create(id);
	this.svr.Create(id);
    },
    Delete:function(id){
	this.model.Delete(id);
	this.dom.Delete(id);
	this.svr.Delete(id);
    },
    launch:function(eltId){
	self.model = new TDL_Model();
	self.dom   = new TDL_DOM(eltId);
	self.svr   = new TDL_Server();
	var self=this;
    }};
