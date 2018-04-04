const ipc = require('electron').ipcRenderer

const skanWindowBtn = document.getElementById('manage-window-demo-toggle') //manage-window-demo-toggle  skan-window
const analWindowBtn = document.getElementById('anal-window')

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
            var data = fs.readFile(filename,function(err,data){
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