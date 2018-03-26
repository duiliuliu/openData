const ipc = require('electron').ipcRenderer

const runSpiderBtn = document.getElementById('run-spider')
const skanWindowBtn = document.getElementById('manage-window-demo-toggle') //manage-window-demo-toggle  skan-window
const analWindowBtn = document.getElementById('anal-window')

const display = require('./display')
const write = require('./write')
const fs = require('fs')

const path = require('path')



runSpiderBtn.addEventListener('click', function () {
  ipc.send('run-spider')
})
skanWindowBtn.addEventListener('click', function () {
  ipc.send('skan-data')
})
analWindowBtn.addEventListener('click', function () {
  ipc.send('anal-data')
})


ipc.on('running-spider', function (event, dirpath) {
  let node_load = document.getElementById('load-data')
  node_load.style.height = '200px'
  node_load.style.overflow = 'auto'

var appendText = function(pNode,text){
  node = document.createElement('text')
  node.innerHTML = '<br>'+text
  node_load.appendChild(node)
}

  appendText(node_load,'下载...')

  var request = require('request')
  request.post('http://182.254.218.20:8081/catalog?query=222',{'method':'getfsdata'},function(err,res,body){
    if(!err &&res.statusCode==200){
 
      appendText(node_load,'抓取数据完成')  

      appendText(node_load,'更新...')

      body = JSON.parse(body)

      var header = body[0]  
      if ('myheader' in body[0]){
        header = header['myheader']
      } 

      write('fs_catalog.html',display(header,body,"fs-catalog-modal"))

      appendText(node_load,'更新数据完成')
      
      ipc.send('skan-data')
    }else{
      appendText(node_load,'连接服务器失败...')
    }

  })
 
})

ipc.on('skanning-data', function (event, dirpath) {

  let node_skan = document.getElementById('skan-data')
  
  node_skan.style.height = '400px'
  node_skan.style.overflow = 'auto'

  filename = path.join( __dirname, '../sections/cities/fs_catalog.html')

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
 
   
})
/*


const BrowserWindow = require('electron').remote.BrowserWindow
const globalShortcut = require('electron').remote.globalShortcut

document.getElementById('skan-window').addEventListener('click', function (event) {
  const modalPath = path.join('file://', __dirname, '../sections/cities/fs_catalog.html')
  let win = new BrowserWindow({
     frame: false,
     width: 1100,
     height: 600,
     title: '数据集'
    })
  win.setFullScreen(true)
  globalShortcut.register('ESC', () => {
    win.setFullScreen(false);
  })
  win.on('close', function () { win = null })
  win.loadURL(modalPath)
  win.show()
})
*/