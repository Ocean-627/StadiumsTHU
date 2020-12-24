<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>
            场地信息编辑 <small>@{{ this.name }}</small>
          </h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item">
              场馆管理
            </li>
            <li class="breadcrumb-item">
              <a href="/stadium_management/stadium_info">场馆列表</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>场地信息编辑</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce">
        <div class="row i-row">
          <a
            href="#modal-form"
            class="btn btn-outline btn-primary i-button"
            data-toggle="modal"
          >
            <i class="fa fa-plus"></i> 添加新场地
          </a>
          <div id="modal-form" class="modal fade">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-body">
                  <div class="row">
                    <div class="col-sm-12">
                      <h3 class="m-t-none m-b">添加新场地</h3>
                      <form role="form">
                        <div class="form-group">
                          <label>场地类型</label>
                          <input
                            type="text"
                            class="form-control"
                            v-model="newGroundType"
                          />
                        </div>
                        <div class="form-group">
                          <label>场地数量</label>
                          <input
                            type="text"
                            class="form-control"
                            v-model="newGroundAmount"
                          />
                        </div>
                      </form>
                      <div>
                        <button
                          class="btn btn-ontline btn-primary float-right"
                          v-on:click="newGround()"
                          data-dismiss="modal"
                        >
                          添加
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <a class="btn btn-outline btn-default i-button" v-on:click="cancel()">
            <i class="fa fa-mail-reply"></i> 返回
          </a>
        </div>
        <div class="row" style="text-align: right; margin-bottom: 10px;">
          <label class="col-sm-3 col-form-label">修改生效日期：</label>
          <div class="col-sm-3 input-group date">
            <span class="input-group-addon"
              ><i class="fa fa-calendar"></i
            ></span>
            <input type="text" class="form-control" />
          </div>
        </div>
        <div class="row" style="margin-bottom: 10px;">
          <label class="col-sm-3 col-form-label"></label>
          <div class="col-sm-3">
            <small>*为了不影响现有预约，该页面的修改将在指定日期后生效</small>
          </div>
        </div>
        <div
          class="grid"
          v-masonry
          transition-duration="0.3s"
          item-selector=".grid-item"
          horizontal-order="true"
          gutter="25"
        >
          <div
            class="grid-item"
            v-masonry-tile
            v-for="(ground, _index) in grounds"
            v-bind:key="ground.name"
          >
            <div class="contact-box">
              <!-- 主要部分 & 单个单元 -->
              <div class="panel-body">
                <fieldset>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label">场地类型：</label>
                    <label class="col-sm-6 col-form-label"
                      ><strong>{{ ground.type }}</strong></label
                    >
                  </div>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label">场地数量：</label>
                    <label class="col-sm-6 col-form-label"
                      ><strong>{{ ground.amount }}</strong></label
                    >
                  </div>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label">开放状态：</label>
                    <div class="col-sm-4">
                      <el-select v-model="models[_index]">
                        <el-option label="开放" value="1"></el-option>
                        <el-option label="未开放" value="0"></el-option>
                      </el-select>
                    </div>
                  </div>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label"
                      >最短预约时间：</label
                    >
                    <div class="col-sm-3">
                      <input
                        type="text"
                        class="form-control"
                        v-model="ground.duration"
                      />
                    </div>
                    <label class="col-sm-2 col-form-label">分钟</label>
                  </div>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label">预约费用：</label>
                    <div class="col-sm-3">
                      <input
                        type="text"
                        class="form-control"
                        v-model="ground.price"
                      />
                    </div>
                    <label class="col-sm-4 col-form-label">元/小时</label>
                  </div>
                  <div class="form-group row">
                    <label class="col-sm-4 col-form-label"
                      >场地人数限制：</label
                    >
                    <div class="col-sm-3">
                      <input
                        type="text"
                        class="form-control"
                        v-model="ground.membership"
                      />
                    </div>
                    <label class="col-sm-4 col-form-label">人</label>
                  </div>
                  <div
                    class="form-group row"
                    style="border-top: 1px solid #e7eaec; padding-top: 10px"
                  >
                    <label class="col-sm-10 col-form-label">开放时间：</label>
                    <div class="col-sm-2">
                      <button
                        type="button"
                        class="btn btn-primary"
                        v-on:click="newPeriod(_index)"
                      >
                        <i class="fa fa-plus"></i>
                      </button>
                    </div>
                  </div>
                  <div
                    class="form-group row"
                    v-for="(period, index) in ground.periods"
                    :key="period.start"
                  >
                    <label class="col-sm-1 col-form-label"></label>
                    <div class="col-sm-4">
                      <div
                        class="input-group clockpicker"
                        data-autoclose="true"
                      >
                        <input
                          type="text"
                          class="form-control"
                          v-model="period.start"
                        />
                        <span class="input-group-addon">
                          <span class="fa fa-clock-o"></span>
                        </span>
                      </div>
                    </div>
                    <div
                      class="col-sm-1 text-center"
                      style="line-height: 35.5px;"
                    >
                      至
                    </div>
                    <div class="col-sm-4">
                      <div
                        class="input-group clockpicker"
                        data-autoclose="true"
                      >
                        <input
                          type="text"
                          class="form-control"
                          v-model="period.end"
                        />
                        <span class="input-group-addon">
                          <span class="fa fa-clock-o"></span>
                        </span>
                      </div>
                    </div>
                    <div class="col-sm-2">
                      <button
                        class="btn btn-danger"
                        v-on:click="deletePeriod(_index, index)"
                      >
                        <i class="fa fa-times"></i>
                      </button>
                    </div>
                  </div>
                  <div
                    class="form-group row"
                    style="border-top: 1px solid #e7eaec; padding-top: 10px"
                  >
                    <label class="col-sm-5 col-form-label"></label>
                    <div
                      class="col-sm-2 btn btn-outline btn-info"
                      v-on:click="submit(ground, _index)"
                      v-if="!ground.new"
                    >
                      提交
                    </div>
                  </div>
                  <div
                    class="form-group row"
                    style="border-top: 1px solid #e7eaec; padding-top: 10px"
                    v-if="ground.new"
                  >
                    <label class="col-sm-3 col-form-label"></label>
                    <div
                      class="col-sm-2 btn btn-outline btn-info"
                      v-on:click="add(ground, _index)"
                    >
                      提交
                    </div>
                    <label class="col-sm-2 col-form-label"></label>
                    <div
                      class="col-sm-2 btn btn-outline btn-danger"
                      v-on:click="remove(ground, _index)"
                    >
                      删除
                    </div>
                  </div>
                </fieldset>
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
</style>

<script>
import Navbar from "@/components/Navbar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Toolbox from "@/components/Toolbox";
import "jquery";
import "masonry-layout";
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/touchspin/jquery.bootstrap-touchspin.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";
export default {
  data() {
    return {
      grounds: [],
      newGroundType: "",
      newGroundAmount: null,
      name: "",
      models: "",
      date: null
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
    $(".input-group.date").datepicker({
      todayBtn: "linked",
      keyboardNavigation: false,
      autoclose: true,
      format: "yyyy-mm-dd",
      startDate: new Date()
    });
    this.updateClock();
    let request = {
      params: {
        id: this.$route.query.id
      }
    };
    this.$axios.get("stadium/", request).then(res => {
      this.name = res.data[0].name;
      this.grounds = res.data[0].courtTypes;
      this.models = Array(this.grounds.length).fill("");
      for (var i = 0; i < this.grounds.length; i++) {
        if (this.grounds[i].openState == 1) {
          this.models[i] = "开放";
        } else {
          this.models[i] = "未开放";
        }
      }
      for (var i = 0; i < this.grounds.length; i++) {
        let duration = this.grounds[i].duration.split(":");
        this.grounds[i].duration =
          Number(duration[0]) * 60 + Number(duration[1]);
        let openHours = this.grounds[i].openingHours.split(" ");
        this.grounds[i].periods = [];
        for (var j = 0; j < openHours.length; j++) {
          let time = openHours[j].split("-");
          this.grounds[i].periods.push({ start: time[0], end: time[1] });
        }
      }
    });
  },
  updated() {
    $(".chosen-select").chosen({ width: "100%" });
    this.updateClock();
  },
  methods: {
    updateClock() {
      let i = 0,
        j = 0,
        k = 0;
      var clocks = document.getElementsByClassName("clockpicker");
      for(; i < this.grounds.length; i++){
        for(; j < this.grounds[i].periods.length; j++) {
            let p = this.grounds[i].periods[j]
            $(clocks[k]).clockpicker().find('input').change(function(){
                p.start = this.value;
            })
            k++;
            $(clocks[k]).clockpicker().find('input').change(function(){
                p.end = this.value;
            })
            k++;
        }
      }
    },
    newGround() {
      this.grounds.push({
        type: this.newGroundType,
        amount: this.newGroundAmount,
        periods: [],
        new: true
      });
      toastr.options = {
        closeButton: true,
        debug: false,
        progressBar: true,
        preventDuplicates: false,
        positionClass: "toast-top-right",
        onclick: null,
        showDuration: "400",
        hideDuration: "1000",
        timeOut: "7000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
      };
      toastr.success("在真正添加场地之前你需要补全场地信息。", "成功");
    },
    add(ground, _index) {
      this.date = $(".input-group.date").datepicker("getDate");
      swal(
        {
          title: "确认新建场地吗？",
          text: "提交后将不可更改",
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
            if (!this.validate()) return;
            this.uploadAddForm(ground, _index);
          }
        }
      );
    },
    remove(ground, _index) {
      this.grounds.splice(_index, 1);
    },
    newPeriod(_index) {
      var period = {
        start: "00:00",
        end: "01:00"
      };
      this.grounds[_index].periods.push(period);
      this.$nextTick(function() {
        var clocks = document.getElementsByClassName("clockpicker");
        for (var i = 0; i < clocks.length; i++) {
          $(clocks[i]).clockpicker();
        }
      });
      this.$forceUpdate();
    },
    deletePeriod(_index, index) {
      this.grounds[_index].periods.splice(index, 1);
      this.$forceUpdate();
    },
    submit(ground, index) {
      this.date = $(".input-group.date").datepicker("getDate");
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
            if (!this.validate()) return;
            this.uploadForm(ground, index);
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
      if (!this.date) {
        swal({
          title: "错误",
          text: "请设置生效日期。",
          type: "error"
        });
      }
      return true;
    },
    uploadForm(ground, index) {
      let duration =
        (Array(2).join("0") + ground.duration / 60).slice(-2) +
        ":" +
        (Array(2).join("0") + (ground.duration % 60)).slice(-2);
      let openingHours = "";
      for (var i = 0; i < ground.periods.length; i++) {
        openingHours +=
          ground.periods[i].start + "-" + ground.periods[i].end + " ";
      }
      let date = this.date;
      let openState = 0;
      if (this.models[index] == "开放" || this.models[index] == 1) {
        openState = 1;
      }
      let request_body = {
        courtType_id: ground.id,
        date:
          date.getFullYear() +
          "-" +
          (date.getMonth() + 1) +
          "-" +
          date.getDate(),
        duration: duration,
        price: ground.price,
        membership: ground.membership,
        openState: openState,
        openingHours: openingHours
      };
      let _this = this;

      this.$axios.post("changeduration/", request_body).then(res => {
        swal(
          {
            title: "成功",
            text: "场地信息修改成功",
            type: "success"
          },
          function() {
            window.location.replace("/stadium_management/stadium_info");
          }
        );
      });
    },
    uploadAddForm(ground, index) {
      let duration =
        (Array(2).join("0") + ground.duration / 60).slice(-2) +
        ":" +
        (Array(2).join("0") + (ground.duration % 60)).slice(-2);
      let openingHours = "";
      for (var i = 0; i < ground.periods.length; i++) {
        openingHours +=
          ground.periods[i].start + "-" + ground.periods[i].end + " ";
      }
      let date = $(".input-group.date").datepicker("getDate");
      let openState = 0;
      if (this.models[index] == "开放" || this.models[index] == 1) {
        openState = 1;
      }
      let request_body = {
        stadium_id: this.$route.query.id,
        num: ground.amount,
        type: ground.type,
        date:
          date.getFullYear() +
          "-" +
          (date.getMonth() + 1) +
          "-" +
          date.getDate(),
        duration: duration,
        price: ground.price,
        membership: ground.membership,
        openState: openState,
        openingHours: openingHours
      };
      let _this = this;

      this.$axios.post("courttype/", request_body).then(res => {
        swal(
          {
            title: "成功",
            text: "新建场地成功！",
            type: "success"
          },
          function() {
            window.location.replace("/stadium_management/stadium_info");
          }
        );
      });
    }
  }
};
</script>
