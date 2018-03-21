/*
    连接MongoDB，进行查询
*/
var async = require('async')
var MongoClient = require('mongodb').MongoClient;
 
var query = function(collection_name,res){

    url = 'mongodb://localhost:27017';
    db_name = 'opendata'
    collection_name = collection_name||'fs_catalog'

    MongoClient.connect(url,function(err,db){
        if(err)
            throw err;
        var dbo = db.db(db_name)
        var collection = dbo.collection(collection_name);
 
        collection.find({}).toArray(function(err,result){
            if(err)
                throw err;
            console.log(result.length);
            res.send(result)

            db.close();
        })
    })

    

}



module.exports = query