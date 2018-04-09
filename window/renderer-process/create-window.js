const ipc = require('electron').ipcRenderer

const skanWindowBtn = document.getElementById('manage-window-demo-toggle') //manage-window-demo-toggle  skan-window
const analWindowBtn = document.getElementById('analyse-window-demo-toggle')

skanWindowBtn.addEventListener('click', function () {
  ipc.send('skan-data')
})
analWindowBtn.addEventListener('click', function () {
  ipc.send('anal-data')
})



var tem2 = new Vue({
  el:'#catalog',
  data:{
      title:'资源目录',
      items:[],
      items_list:{}
  },
  methods:{
      init:function() {
          
            if (file in this.items_list){
                this.items = this.items_list[file]
                return
            }
            tem2.title="资源目录"

            var fs = require('fs')
            var path = require('path')
            var filename = path.join( __dirname, '../sections/cities/',file)
            fs.readFile(filename,function(err,data){
                if(!err){
        
                    tem2.items = JSON.parse(data)
                    
                    tem2.items_list[file] = tem2.items
                } else{
                    tem2.items = []
                    document.getElementById('skan-data').style.height = '50px'
                    tem2.title="暂无数据..."
                }
            
    
            })
         
      },
  }
})

 


ipc.on('skanning-data', function (event, dirpath) {
  
  let node_skan = document.getElementById('skan-data')
  node_skan.style.height = '400px'
  node_skan.style.overflow = 'auto'
  tem.init()
  tem2.init()
  
})


ipc.on('anlysing-data', function (event, dirpath) {
    
    let node_anal = document.getElementById('anal-data')
    let node_display = document.getElementById('main')
    var width = node_anal.offsetWidth
    var height = 600
    node_anal.style.height = height + 'px'
    node_anal.style.overflow = 'auto'

    node_display.style.height = height*0.5 + 'px'
    node_display.style.width = width*0.9 + 'px' 

    
    console.log(width)
    console.log(node_display.offsetHeight)
    console.log(node_display.offsetTop)
    console.log(node_display.offsetLeft) 
    paint()

})

var paint = function(){

    var fs = require('fs')
    var path = require('path')
    var filename = path.join( __dirname, '../sections/cities/',file)

    var painting = function(data){
               
            var myChart = echarts.init(document.getElementById('main'));
                console.log(data[0].indexOf('下载次数'))
                var sizeValue = '57%';
                var symbolSize = 2.5;
                option = {
                    animation:false,
                    legend: {
                        data:['下载次数','浏览次数']
                    },
                    backgroundColor: '#e3ebe2',   // '#2c343c',  //'#e3ebe2',
                  //  textStyle: { color: 'rgba(255, 255, 255, 0.3)'},
                    tooltip: {}, 
                    xAxis:   {type: 'category',  name: '数据目录名称', axisLabel: {rotate: 50, interval: 0}},
 
                    yAxis:    {type: 'value',  name: '数量'}, 
                    dataset: {
                        dimensions: data[0],
                        source: data
                    },
                    dataZoom: [
                        {
                            type: 'slider',
                            show: true,
                            xAxisIndex: [0],
                            start: 30,
                            end: 35
                        },
                        {
                            type: 'slider',
                            show: true,
                            yAxisIndex: [0],
                            left: '93%',
                            start: 15,
                            end: 45
                        },
                        {
                            type: 'inside',
                            xAxisIndex: [0],
                            start: 30,
                            end: 35
                        },
                        {
                            type: 'inside',
                            yAxisIndex: [0],
                            start: 15,
                            end: 45
                        }
                    ],
                    
                    series: [
                        {
                            name: '下载次数',
                            type: 'scatter',
                            symbolSize: function (val) {  
                                    return val[15] * 0.4;
                                }, 
                            itemStyle: {
                                normal: {
                                    opacity: 0.8
                                }
                            },
                            encode: {
                                x: '数据目录名称',
                                y: '下载次数',
                                tooltip: [0, 5, 6, 9,15,16]
                            }
                        },
                        {
                            name: '浏览次数',
                            type: 'scatter',
                            itemStyle: {
                                normal: {
                                    opacity: 0.8,
                                }
                            },
                            symbolSize: function (val) {
                                if (val[16]>500){
                                    return 500 *0.1
                                }
                                return val[16] * 0.3;
                            },
                            encode: {
                                x: '数据目录名称',
                                y: '浏览次数',
                                tooltip: [0, 5, 6, 9,15,16]
                            }
                        }
                          
                    ]
                };
            
                myChart.setOption(option);
                
            }

        fs.readFile(filename,function(err,data){
            if(!err){
    
                data = JSON.parse(data)
                
                painting(data)
            }  
        })
       
}
