// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Common from './Common'

//import '@/assets/js/jquery-3.1.1.min.js'
//import '@/assets/js/popper.min.js'
//import '@/assets/js/bootstrap.js'
//import '@/assets/js/plugins/metisMenu/jquery.metisMenu.js'
//import '@/assets/js/plugins/slimscroll/jquery.slimscroll.min.js'
//
//import '@/assets/js/inspinia.js'
//import '@/assets/js/plugins/pace/pace.min.js'
//
//import '@/assets/js/plugins/jquery-ui/jquery-ui.min.js'
//
//import '@/assets/js/plugins/gritter/jquery.gritter.min.js'
//
//import '@/assets/js/plugins/sweetalert/sweetalert.min.js'


Vue.config.productionTip = false
Vue.prototype.Common = Common

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
