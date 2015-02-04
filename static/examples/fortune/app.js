function FortuneApplication(){
    var self={};
    self.app = 1;
    self.launch = function(){self.main(); return self};
    self.fortune = function(){
        rpc_send("fortune",[]);
        LOG("Please sir may I have another (fortune)?");
    };
    self.main = function(){
        rpc_add_open(function(){
            document.getElementById('access_token').innerHTML = readCookie('access_token');
            self.fortune();
        });
        rpc_add_notify('fortune',function (data) {
            console.log("FORTUNE"+str(data));
            var result = data.result.replace(/\n/g,'<br>');
            LOG("New Fortune: "+str(result),'success');
            document.getElementById('fortune').innerHTML = result;
        });
    };
    return self;
}