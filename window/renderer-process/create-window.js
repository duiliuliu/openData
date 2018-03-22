const ipc = require('electron').ipcRenderer

const runSpiderBtn = document.getElementById('run-spider')
const skanWindowBtn = document.getElementById('manage-window-demo-toggle') //manage-window-demo-toggle  skan-window
const analWindowBtn = document.getElementById('anal-window')

const display = require('./display')
const write = require('./write')
const fs = require('fs')



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

  node = document.createElement('p')
  node.innerHTML = '下载...'
  node_load.appendChild(node)

  var request = require('request')
  request.post('http://127.0.0.1:8081/catalog?query=222',{'method':'getfsdata'},function(err,res,body){
    if(!err &&res.statusCode==200){

      node = document.createElement('p')
      node.innerHTML = '抓取数据完成'
      node_load.appendChild(node)

      node = document.createElement('p')
      node.innerHTML = '更新...'
      node_load.appendChild(node)

      body = JSON.parse(body)

      var header = body[0]  
      if ('myheader' in body[0]){
        header = header['myheader']
      } 

      write('fs_catalog.html',display(header,body,"fs-catalog-modal"))

      node = document.createElement('p')
      node.innerHTML = '更新数据完成'
      node_load.appendChild(node)
      
      ipc.send('skan-data')
    }

  })
 
})

ipc.on('skanning-data', function (event, dirpath) {

  let node_skan = document.getElementById('skan-data')
  
  node_skan.style.height = '400px'
  node_skan.style.overflow = 'auto'

  fs.readFile('./sections/cities/fs_catalog.html', function (err, data) {
    if (err) {
        return console.error(err);
    }
    data = data.toString().replace('<a style="position:fixed;font-color:#8aba87" href="javascript:window.close()">点这儿关闭</a>','')
    node_skan.innerHTML=data

  });
 
   
})

const path = require('path')
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