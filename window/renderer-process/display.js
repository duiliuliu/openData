
var display = function (headers,data,id){
    var header_list = []

    //获取表头 
    if ('header_sort' in headers){
        header_list = headers['header_sort']
    }else{
        for(h in headers){
            header_list.push(h)
        }
    }

    id = id ||"catalog-modal"

    var htm = ''

    htm +=       '<div id="' + id + '" class="tab-pane fade in active" >'
        +   '<a style="position:fixed;font-color:#8aba87" href="javascript:window.close()">点这儿关闭</a>'
        +    '<table class="table table-bordered table-hover">'
        +    '<caption class="h3 text-info">资源目录</caption>'   
        +   createTh(header_list,headers)
        +   createTd(header_list,data)  
        +   ' </table></div> '
        
    return htm
}

var createTh = function(header,headers){
    var htm = '<tr>'
    for(h in header){
        htm += '<th class="text-center">' + headers[header[h]] + '</th>'
    }
    htm += '</tr>'
    return htm
}

var createTd = function(header,items){
    var htm = ''
    for(i in items){
        htm += '<tr>'
        for(h in header){
            htm += '<td class="text-center">' + items[i][header[h]] + '</td>'
        }
        htm += '</tr>'
    }
    return htm
}

module.exports = display;