function TDL_Server(){
    var self=(this===window)?Object.create(TDL_Server.prototype):this;
    return self;
}
TDL_Server.prototype={
    Update:function(k,id,v){
	var self=this;
	rpc_send("db_update",[{id:id,k:v}],function(data){});
    },
    Create:function(id){
	var self=this;
	rpc_send("db_create",[{id:id}],function(data){});
	},
    Delete:function(id){
	var self=this;
	rpc_send("db_delete",[{id:id}],function(data){});
    }};
