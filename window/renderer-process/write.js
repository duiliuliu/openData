
var fs = require('fs')

const path = require('path')

var write = function(filename,data){
    var dir = path.join( __dirname, '../sections/cities')

    stats = fs.statSync(dir)
    if(!stats.isDirectory()){
        fs.mkdir(dir)
    }    

    filename = dir +'/'+  filename

    fs.writeFileSync(filename,data)
}

module.exports = write

