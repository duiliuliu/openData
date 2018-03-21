/*
    node服务器
*/

var express = require('express')
var app = express()

var query = require('./mongo')

app.post('/catalog',function(req,res){
    console.log(req.query);
    query('fs_catalog',res);
})

var serve = app.listen(8081,function(){
    console.log('服务已启动！');
})
