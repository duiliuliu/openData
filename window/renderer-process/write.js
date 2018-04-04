
var fs = require('fs')

const path = require('path')

var write = function(filename,data){
    var dir = path.join( __dirname, '../sections/cities')

    stats = fs.statSync(dir)
    if(!stats.isDirectory()){
        fs.mkdir(dir)
    }    

    data = JSON.parse(data)
    var header = data[0]
    if ('myheader' in data[0]){
        header = header['myheader']
        data[0] = header
    } 
    var header_list = []
    
    //获取表头 
    if ('header_sort' in header){
        header_list = header['header_sort']
    }else{
        for(h in header){
            header_list.push(h)
        }
    }

    items = []
    for (d in data){
        mi_list = []
        for (h in header_list){
            mi_list.push(data[d][header_list[h]])
        }
        items.push(mi_list)
        //console.log(mi_list)
    }
 
    filename = dir +'\\'+  filename
    fs.writeFileSync(filename,JSON.stringify(items))
}

module.exports = write

