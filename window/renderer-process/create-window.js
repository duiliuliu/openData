const ipc = require('electron').ipcRenderer

const skanWindowBtn = document.getElementById('manage-window-demo-toggle') //manage-window-demo-toggle  skan-window
const analWindowBtn = document.getElementById('anal-window')

const display = require('./display')
const write = require('./write')
const fs = require('fs')

const path = require('path')

skanWindowBtn.addEventListener('click', function () {
  ipc.send('skan-data')
})
analWindowBtn.addEventListener('click', function () {
  ipc.send('anal-data')
})


var tem2 = new Vue({
  el:'#catalog',
  data:{
      items:[]
  },
  methods:{
      init:function() {
          var fs = require('fs')
          var path = require('path')
          var filename = path.join( __dirname, '../sections/cities/',file)
          console.log(file)
          var data = fs.readFile(filename,function(err,data){
            if(!err){
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
    
    
              for (d in data){
                  mi_list = []
                  for (h in header_list){
                      mi_list.push(data[d][header_list[h]])
                  }
                  this.items.push(mi_list)
                  //console.log(mi_list)
              }
            } 
           
  
          })
         
      },
  }
})

 


ipc.on('skanning-data', function (event, dirpath) {
  
  let node_skan = document.getElementById('skan-data')
  tem.init()
  tem2.init()
  node_skan.style.height = '400px'
  node_skan.style.overflow = 'auto'
   
})
/*
 

  filename = path.join( __dirname, '../sections/catalog.html')

  fs.readFile(filename, function (err, data) {
    if (err) {
        return console.error(err);
    }
    data = data.toString().replace('<div><button class="modal-hide">点我退出</button><div>','').replace('fs-catalog-modal','wrap-catalog')
      .replace('modal','').replace('about','')
      .replace('<template class="task-template">','')
      .replace('</template>','')
    node_skan.innerHTML=data

  });
 
*/