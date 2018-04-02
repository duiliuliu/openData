const storage = require('electron-json-storage')
const write = require('../renderer-process/write')

// Default to the view that was active the last time the app was open
storage.get('activeSectionButtonId', function (err, id) {
  if (err) return console.error(err)

  if (id && id.length) {
    showMainContent()
    const section = document.getElementById(id)
    if (section) section.click()
  } else {
    activateDefaultSection()
    displayAbout()
  }
})

document.body.addEventListener('click', function (event) {

  if (event.target.dataset.section) {
    handleSectionTrigger(event)
  } else if (event.target.dataset.modal) {
    handleModalTrigger(event)
  } else if (event.target.classList.contains('modal-hide')) {
    hideAllModals()
  }
})

function handleSectionTrigger (event) {
  hideAllSectionsAndDeselectButtons()

  // Highlight clicked button and show view
  event.target.classList.add('is-selected')

  // Display the current section
  const sectionId = event.target.dataset.section + '-section'
  document.getElementById(sectionId).classList.add('is-shown')

  // Save currently active button in localStorage
  const buttonId = event.target.getAttribute('id')
  storage.set('activeSectionButtonId', buttonId, function (err) {
    if (err) return console.error(err)
  })
  tem3.select(buttonId)
}

function activateDefaultSection () {
  document.getElementById('button-about').click()
}

function showMainContent () {
  document.querySelector('.js-nav').classList.add('is-shown')
  document.querySelector('.js-content').classList.add('is-shown')
}

function handleModalTrigger (event) {
  hideAllModals()
  const modalId = event.target.dataset.modal + '-modal'
  document.getElementById(modalId).classList.add('is-shown')
}

function hideAllModals () {
  const modals = document.querySelectorAll('.modal.is-shown')
  Array.prototype.forEach.call(modals, function (modal) {
    modal.classList.remove('is-shown')
  })
  showMainContent()
}

function hideAllSectionsAndDeselectButtons () {
  const sections = document.querySelectorAll('.js-section.is-shown')
  Array.prototype.forEach.call(sections, function (section) {
    section.classList.remove('is-shown')
  })

  const buttons = document.querySelectorAll('.nav-button.is-selected')
  Array.prototype.forEach.call(buttons, function (button) {
    button.classList.remove('is-selected')
  })
}

function displayAbout () {
  document.querySelector('#about-modal').classList.add('is-shown')
}

var tem3 = new Vue({
  el:'body',
  data:{
    data:'data',
    title:'',
    theme:'',
    icon:'',
    message:['点击Run进行抓取！'],
    i:1,
    items:[
      {
          id:'button-fs',
          name:'佛山',
          title:'佛山市开放数据',
          data:'fs_catalog',
          theme:'section js-section u-category-windows',
          icon:'assets/img/icons.svg#icon-native-ui',
          message:['点击Run进行抓取！'],
      },
      {
          id:'button-gz',
          name:'贵州',
          title:'贵州市开放数据',
          data:'gz_catalog',
          theme:'section js-section u-category-menu',
          icon:'assets/img/icons.svg#icon-menu',
          message:['点击Run进行抓取！'],
      },
      {
          id:'button-hrb',
          name:'哈尔滨',
          title:'哈尔滨市开放数据',
          data:'hrb_catalog',
          theme:'section js-section u-category-system',
          icon:'assets/img/icons.svg#icon-system',
          message:['点击Run进行抓取！'],
      },
      {
        id:'button-qd',
        name:'青岛',
        title:'青岛市开放数据',
        data:'qd_catalog',
        theme:'section js-section u-category-native-ui',
        icon:'assets/img/icons.svg#icon-system',
        message:['点击Run进行抓取！'],
    }
    ]
  },
  methods:{
    addMessage: function(msg){
      this.items[this.i].message.push(msg)
    },
    select: function(id){
      for( i in this.items){
        if (this.items[i].id==id){
          this.i = i;
          this.data = this.items[i].data;
          this.title = this.items[i].title;
          this.icon = this.items[i].icon;
          this.theme = this.items[i].theme;
          this.message = this.items[i].message;
          file = this.items[i].data + '.json'
        }
      }
    },
    query:function(para){

      let node_load = document.getElementById('load-data')
      node_load.style.height = '200px'
      node_load.style.overflow = 'auto'
      tem3.addMessage('下载...')
      var request = require('request')
      request.post('http://182.254.218.20:8081/catalog?query='+para,function(err,res,body){
        if(!err &&res.statusCode==200){
    
          tem3.addMessage('抓取数据完成')  

          tem3.addMessage('更新...')
    
          write(file,body) //display(header,body,"fs-catalog-modal")

          tem3.addMessage('更新数据完成')
          
        }else{
          //console.log(err)
          tem3.addMessage('连接服务器失败...')
        }

      })
    }
  }

})
