<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>场馆信息编辑 <small>@{{this.name}}</small></h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item">
              场馆管理
            </li>
            <li class="breadcrumb-item">
              <a href="/stadium_management/stadium_info">场馆信息管理</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>场馆信息编辑</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce">
        <div class="row">
          <div class="col-lg-12">
            <div class="tabs-container">
              <ul class="nav nav-tabs">
                <li><a class="nav-link active" data-toggle="tab" href="#tab-1">基本信息</a></li>
                <li><a class="nav-link" data-toggle="tab" href="#tab-2">场馆图片</a></li>
                <li><a class="nav-link" data-toggle="tab" href="#tab-3">预约选项</a></li>
                <li><a class="nav-link" data-toggle="tab" href="#tab-4">地理位置</a></li>
              </ul>
              <div class="tab-content">
                <div id="tab-1" class="tab-pane active">
                  <div class="panel-body">
                    <fieldset>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label">场馆名称：</label>
                        <div class="col-sm-2">
                          <input type="text" class="form-control" ref="name" />
                        </div>
                      </div>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label">开放状态：</label>
                        <div class="col-sm-2">
                          <select data-placeholder="..." class="chosen-select" tabindex="2" ref="openState">
                            <option>开放</option>
                            <option>未开放</option>
                          </select>
                        </div>
                      </div>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label"
                          >联系方式：</label
                        >
                        <div class="col-sm-4">
                          <input
                            type="text"
                            class="form-control"
                            placeholder="..."
                            ref="contact"
                          />
                        </div>
                      </div>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label">场馆说明:</label>
                        <div class="col-sm-10">
                          <textarea
                            class="form-control"
                            placeholder="输入场馆说明..."
                            style="height: 100px;"
                            ref="information"
                          ></textarea>
                        </div>
                      </div>
                      <div class="form-group row">
                        <div class="col-sm-5"></div>
                        <div class="col-sm-2">
                          <button
                            type="button"
                            class="btn btn-primary"
                            v-on:click="submit(1)"
                          >
                            提交
                          </button>
                          <button
                            type="button"
                            class="btn btn-default"
                            v-on:click="cancel()"
                          >
                            取消
                          </button>
                        </div>
                      </div>
                    </fieldset>
                  </div>
                </div>
                <div id="tab-2" class="tab-pane">
                  <div class="panel-body">
                    <fieldset>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label"
                          >场馆封面：</label
                        >
                        <div class="col-sm-10">
                          <img
                            alt="image"
                            class="rounded m-t-xs img-fluid"
                            src="/static/img/zongti.jpg"
                          />
                        </div>
                      </div>
                      <div class="form-group row">
                        <label class="col-sm-8 col-form-label"></label>
                        <div class="col-sm-4">
                          <div
                            class="fileinput fileinput-new"
                            data-provides="fileinput"
                          >
                            <span class="btn btn-default btn-file"
                              ><span class="fileinput-new">选择文件</span
                              ><span class="fileinput-exists">Change</span
                              ><input type="file" name="..."
                            /></span>
                            <span class="fileinput-filename"></span>
                            <a
                              href="#"
                              class="close fileinput-exists"
                              data-dismiss="fileinput"
                              style="float: none;"
                              >&times;</a
                            >
                          </div>
                        </div>
                      </div>
                      <div class="form-group row">
                        <div class="col-sm-5"></div>
                        <div class="col-sm-2">
                          <button
                            type="button"
                            class="btn btn-primary"
                            v-on:click="submit()"
                          >
                            提交
                          </button>
                          <button
                            type="button"
                            class="btn btn-default"
                            v-on:click="cancel()"
                          >
                            取消
                          </button>
                        </div>
                      </div>
                    </fieldset>
                  </div>
                </div>
                <div id="tab-3" class="tab-pane">
                  <div class="panel-body">
                    <fieldset>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label"
                          >开放时间：</label
                        >
                        <div class="col-sm-2">
                          <div
                            class="input-group clockpicker"
                            data-autoclose="true"
                          >
                            <input
                              type="text"
                              class="form-control"
                              v-model="period.start"
                              ref="openTime"
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
                        <div class="col-sm-2">
                          <div
                            class="input-group clockpicker"
                            data-autoclose="true"
                          >
                            <input
                              type="text"
                              class="form-control"
                              v-model="period.end"
                              ref="closeTime"
                            />
                            <span class="input-group-addon">
                              <span class="fa fa-clock-o"></span>
                            </span>
                          </div>
                        </div>
                      </div>
                      <div class="form-group row">
                        <label class="col-sm-2 col-form-label" ref="duration"
                          >最长提前预约天数：</label
                        >
                        <div class="col-sm-1">
                          <input type="text" class="form-control" ref="foreDays"/>
                        </div>
                      </div>
                      <div class="form-group row" id="data_1">
                        <label class="col-sm-2 col-form-label"
                          >修改生效日期：</label
                        >
                        <div class="col-sm-2 input-group date">
                          <span class="input-group-addon"
                            ><i class="fa fa-calendar"></i></span
                          ><input
                            type="text"
                            class="form-control" ref="startDate"/>
                        </div>
                      </div>
                      <div class="form-group row">
                        <div class="col-sm-5"></div>
                        <div class="col-sm-2">
                          <button
                            type="button"
                            class="btn btn-primary"
                            v-on:click="submit(3)"
                          >
                            提交
                          </button>
                          <button
                            type="button"
                            class="btn btn-default"
                            v-on:click="cancel()"
                          >
                            取消
                          </button>
                        </div>
                      </div>
                    </fieldset>
                  </div>
                </div>
                <div id="tab-4" class="tab-pane">
                  <div class="panel-body">
                    <fieldset>
                      <!-- 预计接入百度地图API -->
                      <div class="col-lg-2">啊这，还没做呢</div>
                      <div class="form-group row">
                        <div class="col-sm-5"></div>
                        <div class="col-sm-2">
                          <button
                            type="button"
                            class="btn btn-primary"
                            v-on:click="submit(3)"
                          >
                            提交
                          </button>
                          <button
                            type="button"
                            class="btn btn-default"
                            v-on:click="cancel()"
                          >
                            取消
                          </button>
                        </div>
                      </div>
                    </fieldset>
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
@import "../../assets/css/plugins/datapicker/datepicker3.css";
.chosen-container-single .chosen-single {
  padding: 4px 12px;
}
</style>

<script>
import Navbar from "@/components/Navbar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Toolbox from "@/components/Toolbox";
import "jquery";
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";
export default {
  data() {
    return {
      period: {
        start: "08:00",
        end: "12:00"
      },
      active_time: "",
      name:"",
      openTime:"",
      closeTime:""
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
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
      format: "yyyy-mm-dd",
      startDate: new Date()
    })
    let request = {
        params: {
            id: this.$route.query.id,
        }
    }
    this.$axios.get('stadium/', request)
        .then(res => {
                this.name = res.data[0].name
                this.openTime = res.data[0].openTime
                this.closeTime = res.data[0].closeTime
                this.$refs.name.value = res.data[0].name
                // TODO:根据res.data.stadiums[0].openState 设置默认option
                this.$refs.contact.value = res.data[0].contact
                this.$refs.information.value = res.data[0].information
                this.$refs.foreDays.value = res.data[0].foreDays
                this.$refs.openTime.value = res.data[0].openTime
                this.$refs.closeTime.value = res.data[0].closeTime
        })
  },
  updated() {
    this.$refs.openTime.value = this.openTime
    this.$refs.closeTime.value = this.closeTime
    $(".chosen-select").chosen({ width: "100%" });
    var clocks = document.getElementsByClassName("clockpicker");
    for (var i = 0; i < clocks.length; i++) {
      $(clocks[i]).clockpicker();
    }
    $("#data_1 .input-group.date").datepicker({
      todayBtn: "linked",
      keyboardNavigation: false,
      autoclose: true,
      format: "yyyy-mm-dd",
      startDate: new Date()
    })
  },
  methods: {
    fileSelected(e) {
      var filename = e.target.files;
      $(this)
        .next(".custom-file-label")
        .addClass("selected")
        .html(fileName);
    },
    submit(index) {
      swal(
        {
          title: "你确定？",
          text: "确认提交现有的更改",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          closeModal: false
        },
        res => {
          if (res) {
            // 检查表单合法性
            // if (!this.validate()) return;
            this.uploadForm(index);
          }
        }
      );
    },
    cancel() {
      swal(
        {
          title: "你确定？",
          text: "取消将返回上一页，你将失去在此处的所有更改",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          closeModal: false
        },
        res => {
          if (res) {
            window.location.replace("/stadium_management/stadium_info");
          }
        }
      );
    },
    validate() {
      if (this.periods.length === 0) return true;
      for (var period in this.periods) {
        if (period.start >= period.end) return true;
      }
      return true;
    },

    uploadForm(index) {
      let request_body = {};
      switch (index) {
        // 修改场馆基本信息
        case 1:
          request_body = {
            stadium_id: this.$route.query.id,
            managerId: 3,
            name: this.$refs.name.value,
            openState: this.$refs.openState.value === "开放",
            information: this.$refs.information.value,
            contact: this.$refs.contact.value
          };
                this.$axios.post("stadium/", request_body).then(res => {
        console.log(res);
        if (res.data.error) {
          alert("Error! Please try again.");
        } else {
          setTimeout(
            () =>
              swal({
                title: "成功",
                text: "场馆信息修改成功",
                type: "success"
              }),
            1000
          );
          window.location.replace("/stadium_management/stadium_info");
        }
      });
          break;
        case 2:
          break;

        // 修改场馆开放关闭时间
        case 3:
          request_body = {
            stadium_id: this.$route.query.id,
            managerId: 3,
            openState:1,
            startDate: this.$refs.startDate.value,
            openTime: this.$refs.openTime.value,
            closeTime: this.$refs.closeTime.value,
            foreDays: this.$refs.foreDays.value
          };
          this.$axios.post("changeschedule/", request_body,).then(res => {
            console.log(res);
            if (res.data.error) {
              alert("Error! Please try again.");
            } else {
            setTimeout(
              () =>
              swal({
                title: "成功",
                text: "场馆信息修改成功",
                type: "success"
                }),1000
              );
          window.location.replace("/stadium_management/stadium_info");
        }
      });
          break;
        default:
          break;
      }

    }
  }
};
</script>
