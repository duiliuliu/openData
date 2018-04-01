const app = require('electron').app
const ipc = require('electron').ipcMain
/*
ipc.on('run-spider', function (event) {
  event.sender.send('running-spider')
})
*/
ipc.on('skan-data', function (event) {
  event.sender.send('skanning-data')
})

ipc.on('anal-data', function (event) {
  event.sender.send('anlysing-data')
})
