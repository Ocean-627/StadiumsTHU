<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>场地预留 <small>@综合体育馆</small></h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item">场馆管理</li>
            <li class="breadcrumb-item active">
              <strong>场地预留</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce">
        <!-- TODO: 在路由里添加参数，控制是到哪一个场馆的编辑页面 -->
        <div class="row" style="margin-bottom: 20px">
          <div class="col-lg-3">
            <select
              class="chosen-select"
              v-model="current_date"
              @changed="changeDate()"
            >
              <option v-for="(date, index) in dates" :key="date" :value="index">
                {{ date }}
              </option>
            </select>
          </div>
        </div>
        <div
          class="row"
          v-for="(ground, ground_index) in grounds"
          :key="ground.name"
        >
          <div class="col-lg-12">
            <div class="ibox">
              <div class="ibox-title">
                <h5>{{ ground.name }}</h5>
                <div class="ibox-tools">
                  <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                    <i class="fa fa-wrench" style="color: green"></i>
                  </a>
                  <ul class="dropdown-menu dropdown-user">
                    <li>
                      <a
                        class="dropdown-item"
                        data-toggle="modal"
                        data-target="#myModal"
                        >场地预留</a
                      >
                    </li>
                    <li>
                      <a class="dropdown-item" v-on:click="manage(ground)"
                        >预约管理</a
                      >
                    </li>
                  </ul>
                  <a class="collapse-link">
                    <i class="fa fa-chevron-up"></i>
                  </a>
                </div>
              </div>
              <div class="ibox-content">
                <div v-for="data in ground.datas" :key="data.id">
                  <h5>{{ data.id }}</h5>
                  <div class="progress">
                    <div
                      v-for="reserve in data.reserves"
                      :key="reserve.start"
                      :class="reserve.type | progress_type"
                      :style="reserve | progress_length"
                      role="progressbar"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      :title="reserve.type | progress_title"
                    ></div>
                  </div>
                  <br />
                </div>
              </div>
              <div
                class="modal inmodal"
                id="myModal"
                tabindex="-1"
                role="dialog"
                aria-hidden="true"
              >
                <div class="modal-dialog">
                  <div class="modal-content animated fadeIn">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal">
                        <span aria-hidden="true">&times;</span
                        ><span class="sr-only">关闭</span></button
                      ><br />
                      <h4 class="modal-title">场地预留</h4>
                    </div>
                    <div class="modal-body">
                      <p>
                        场地类型：<strong>{{ ground.name }}</strong>
                      </p>
                      <div class="form-group" id="data_1">
                        <label class="font-normal">使用日期</label>
                        <div class="input-group date">
                          <span class="input-group-addon"
                            ><i class="fa fa-calendar"></i></span
                          ><input
                            type="text"
                            class="form-control"
                            v-model="form_time"
                          />
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="font-normal">使用时段</label>
                        <div class="form-group row">
                          <div class="col-sm-5">
                            <div
                              class="input-group clockpicker"
                              data-autoclose="true"
                            >
                              <input
                                type="text"
                                class="form-control"
                                v-model="form_start"
                              />
                              <span class="input-group-addon">
                                <span class="fa fa-clock-o"></span>
                              </span>
                            </div>
                          </div>
                          <div
                            class="col-sm-1 text-center"
                            style="line-height: 35.5px"
                          >
                            至
                          </div>
                          <div class="col-sm-5">
                            <div
                              class="input-group clockpicker"
                              data-autoclose="true"
                            >
                              <input
                                type="text"
                                class="form-control"
                                v-model="form_end"
                              />
                              <span class="input-group-addon">
                                <span class="fa fa-clock-o"></span>
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="font-normal">使用者</label>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button
                        type="button"
                        class="btn btn-white"
                        data-dismiss="modal"
                      >
                        关闭
                      </button>
                      <button type="button" class="btn btn-primary">
                        保存更改
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer></Footer>
    </div>
    <Toolbox></Toolbox>
  </div>
</template>

<style>
@import "../../assets/css/plugins/chosen/bootstrap-chosen.css";
@import "../../assets/css/plugins/jasny/jasny-bootstrap.min.css";
@import "../../assets/css/plugins/clockpicker/clockpicker.css";
@import "../../assets/css/plugins/touchspin/jquery.bootstrap-touchspin.min.css";
@import "../../assets/css/plugins/datapicker/datepicker3.css";
.i-row [class^="col-"] {
  padding: 10px;
}

.i-row {
  margin: 0;
}

.contact-box {
  max-width: 450px;
  padding: 10px;
}

.i-button {
  margin-bottom: 20px;
  margin-right: 10px;
}

.i-title {
  margin-top: 10px;
  font-weight: bolder;
  text-align: center;
}

.i-infobox {
  line-height: 30px;
  font-size: 13px;
  font-weight: bold;
}

.i-star {
  color: orange;
}

.i-icon {
  margin-right: 10px;
}

.i-groundinfo {
  border-top: 1px solid #e7eaec;
  font-weight: bold;
}

.chosen-container-single .chosen-single {
  padding: 4px 12px;
}

.progress-bar-default {
  background-color: #e9ecef;
}

.progress-bar-disabled {
  background-color: #9ca8b3;
}

.popover {
  z-index: 10000;
}
</style>

<script>
import Navbar from "@/components/Navbar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Toolbox from "@/components/Toolbox";
import Common from "@/Common";
import "jquery";
import "masonry-layout";
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/touchspin/jquery.bootstrap-touchspin.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";

export default {
  data() {
    // TODO: 在获取到信息之后，要对每种场地的每个场地的预定列表做预处理 fix_reserves()
    //          如果要改对应的属性名称的话，Common.vue里的预处理函数也需要改一点点
    let res = {
      grounds: [],
      dates: [
        // 应该获取到管理员可以查看的日期的列表
        "2020-11-26",
        "2020-11-27",
        "2020-11-28"
      ],
      current_date: 0,
      form_date: "",
      form_time: "",
      form_start: "",
      form_end: ""
    };

    return res;
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
  },
  methods: {
    reserve(ground) {
      // TODO: 弹出窗口填写表单
    },
    manage(ground) {
      // TODO: 跳转到相应的预约信息管理界面就行
    }
  },
  filters: {
    progress_type: function(type) {
      if (type === 0) {
        return "progress-bar progress-bar-default";
      } else if (type === 1) {
        return "progress-bar progress-bar-primary";
      } else if (type === 2) {
        return "progress-bar progress-bar-warning";
      } else if (type === -1) {
        return "progress-bar progress-bar-disabled";
      }
    },
    progress_length: function(reserve) {
      var h, m;
      h = parseInt(reserve.start.split(":")[0]);
      m = parseInt(reserve.start.split(":")[1]);
      var start_time = h * 60 + m;
      h = parseInt(reserve.end.split(":")[0]);
      m = parseInt(reserve.end.split(":")[1]);
      var end_time = h * 60 + m;
      var delta = (end_time - start_time) / 14.4;
      return "width: " + delta.toString() + "%";
    },
    progress_title: function(type) {
      if (type === 0) {
        return "空闲时段";
      } else if (type === 1) {
        return "已预订时段";
      } else if (type === 2) {
        return "预留时段";
      } else if (type === -1) {
        return "不可用时段";
      }
    }
  },
  updated() {
    $(".chosen-select").chosen({ width: "100%" });
    var clocks = document.getElementsByClassName("clockpicker");
    for (var i = 0; i < clocks.length; i++) {
      $(clocks[i]).clockpicker();
    }
    $("#data_1 .input-group.date").datepicker({
      todayBtn: "linked",
      keyboardNavigation: false,
      autoclose: true,
      format: "yyyy-mm-dd"
    });
  },
  mounted() {
    $(".chosen-select").chosen({ width: "100%" });
    var clocks = document.getElementsByClassName("clockpicker");
    for (var i = 0; i < clocks.length; i++) {
      $(clocks[i]).clockpicker();
    }
    $("#data_1 .input-group.date").datepicker({
      todayBtn: "linked",
      keyboardNavigation: false,
      autoclose: true,
      format: "yyyy-mm-dd"
    });

    let grounds = [
      {
        name: "羽毛球场",
        open_times: [
          {
            start: "08:00",
            end: "13:00"
          },
          {
            start: "14:00",
            end: "22:00"
          }
        ],
        datas: [
          {
            id: 0,
            reserves: [
              {
                type: 1,
                start: "08:00",
                end: "10:00"
              },
              {
                type: 1,
                start: "12:00",
                end: "13:00"
              },
              {
                type: 2,
                start: "14:00",
                end: "17:30"
              }
            ]
          },
          {
            id: 1,
            reserves: [
              {
                type: 1,
                start: "09:00",
                end: "10:30"
              },
              {
                type: 1,
                start: "14:30",
                end: "16:00"
              },
              {
                type: 1,
                start: "20:00",
                end: "21:30"
              }
            ]
          }
        ]
      },
      {
        name: "乒乓球场",
        open_times: [
          {
            start: "06:00",
            end: "13:00"
          },
          {
            start: "14:00",
            end: "22:00"
          }
        ],
        datas: [
          {
            id: 0,
            reserves: [
              {
                type: 1,
                start: "08:00",
                end: "10:00"
              },
              {
                type: 1,
                start: "12:00",
                end: "13:00"
              },
              {
                type: 1,
                start: "15:00",
                end: "18:30"
              }
            ]
          },
          {
            id: 1,
            reserves: [
              {
                type: 1,
                start: "09:00",
                end: "10:30"
              },
              {
                type: 1,
                start: "14:00",
                end: "16:00"
              },
              {
                type: 1,
                start: "19:50",
                end: "22:00"
              }
            ]
          }
        ]
      }
    ];
    for (let i = 0; i < grounds.length; i++) {
      for (let j = 0; j < grounds[i].datas.length; j++) {
        grounds[i].datas[j].reserves = Common.fix_reserves(
          grounds[i].datas[j].reserves,
          grounds[i].open_times
        );
      }
    }
    this.grounds = grounds;
  }
};
</script>
