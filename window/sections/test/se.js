var express = require('express')
var fs = require('fs')

var app = express()

app.get('/data',function(req,res){
    fs.readFile('./data.json',function(err,data){
        res.send(data)
    })
})

var serve = app.listen(8081,function(){
    console.log('服务已启动！');
})