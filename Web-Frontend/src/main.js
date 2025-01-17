// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import cookie from "vue-cookie";
import router from "./router";
import Common from "./Common";
import axios from "axios";
// 导入组件库
import ElementUI from "element-ui"; // 导入组件相关样式
import "element-ui/lib/theme-chalk/index.css"; // 配置vue插件

import "xe-utils";
import VXETable from "vxe-table";
import "vxe-table/lib/style.css";
import VXETablePluginExportXLSX from "vxe-table-plugin-export-xlsx";
import moment from "moment";
import { VueMasonryPlugin } from "vue-masonry";
import $ from "jquery";

Vue.use(ElementUI);
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
//import '@/assets/js/plugins/gritter/jquery.gritter.min.js'
//import '@/assets/js/plugins/toastr/toastr.min.js'

import "@/assets/js/plugins/sweetalert/sweetalert.min.js";

axios.interceptors.request.use(
  function(config) {
    let token = window.localStorage.getItem("loginToken");
    if (token) {
      // 添加headers
      config.headers.loginToken = `${token}`;
    }
    return config;
  },
  function(err) {
    return Promise.reject(err);
  }
);

axios.interceptors.response.use(
  response => {
    //console.log(response);
    if (response.data.error) {
      swal({
        title: "错误",
        text: response.data.error,
        type: "error"
      });
    }
    return response;
  },
  error => {
    console.log(error);
    if (error.response.status === 403) {
      swal(
        {
          title: "错误",
          text: "未登录或登陆信息失效！",
          type: "error"
        },
        function() {
          window.location.replace("/login");
        }
      );
    } else if (error.response.status === 400) {
      swal({
        title: "错误",
        text: "信息填写不完整！",
        type: "error"
      });
    } else if (error.response.status === 500) {
      swal({
        title: "错误",
        text: "未知的服务器错误！请刷新页面重试或联系开发人员。",
        type: "error"
      });
    } else if (error.code === "ECONNABORTED") {
    } else {
      swal({
        title: "错误",
        text: error,
        type: "error"
      });
    }
    return Promise.reject(error.response.status);
  }
);

axios.defaults.withCredentials = true;
Vue.prototype.$http = axios;
axios.defaults.baseURL = "https://cbx.iterator-traits.com/api/manager";
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
