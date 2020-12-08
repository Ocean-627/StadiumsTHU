// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import cookie from 'vue-cookie'
import router from "./router";
import Common from "./Common";
import axios from "axios";

import "xe-utils";
import VXETable from "vxe-table";
import "vxe-table/lib/style.css";
import VXETablePluginExportXLSX from "vxe-table-plugin-export-xlsx";
import moment from "moment";
import { VueMasonryPlugin } from "vue-masonry";

Vue.use(VXETable);
VXETable.use(VXETablePluginExportXLSX);

Vue.use(VueMasonryPlugin);

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

axios.defaults.withCredentials = true;
Vue.prototype.$http = axios
axios.defaults.baseURL = "http://127.0.0.1:8000/api/manager";
Vue.config.productionTip = false;
Vue.prototype.Common = Common;
Vue.prototype.$axios = axios;
Vue.prototype.$cookie = cookie;


/* eslint-disable no-new */

Vue.filter("datetime_format", function(str, pattern = "YYYY-MM-DD HH:mm:ss") {
    return moment(str).format(pattern);
});

Vue.filter("datetime_format_2", function(str) {
  if (!str) return "";
  var date = new Date(str);
  var time = new Date().getTime() - date.getTime(); //现在的时间-传入的时间 = 相差的时间（单位 = 毫秒）
  if (time < 0) {
    return "";
  } else if (time / 1000 < 30) {
    return "刚刚";
  } else if (time / 1000 < 60) {
    return parseInt(time / 1000) + "秒前";
  } else if (time / 60000 < 60) {
    return parseInt(time / 60000) + "分钟前";
  } else if (time / 3600000 < 24) {
    return parseInt(time / 3600000) + "小时前";
  } else if (time / 86400000 < 31) {
    return parseInt(time / 86400000) + "天前";
  } else if (time / 2592000000 < 12) {
    return parseInt(time / 2592000000) + "月前";
  } else {
    return parseInt(time / 31536000000) + "年前";
  }
});

new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});