
var fs = require('fs')

var write = function(filename,data){
    var dir = './sections/cities'

    stats = fs.statSync(dir)
    if(!stats.isDirectory()){
        fs.mkdir(dir)
    }    

    filename = dir +'/'+  filename

    fs.writeFileSync(filename,data)
}

module.exports = write

