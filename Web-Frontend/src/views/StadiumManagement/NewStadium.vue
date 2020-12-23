<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>添加新场馆</h2>
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
              <strong>添加新场馆</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight">
        <div class="panel-body white-bg">
          <div class="form-group row">
            <label class="col-lg-2 col-form-label"><h3>基本信息</h3></label>
          </div>
          <div class="form-group row">
            <label class="col-lg-2 col-form-label">场馆名称：</label>
            <div class="col-lg-2">
              <input type="text" class="form-control" ref="name" />
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-2 col-form-label">联系方式：</label>
            <div class="col-lg-4">
              <input
                type="text"
                class="form-control"
                placeholder="..."
                ref="contact"
              />
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-2 col-form-label">场馆说明:</label>
            <div class="col-lg-10">
              <textarea
                class="form-control"
                placeholder="输入场馆说明..."
                style="height: 100px;"
                ref="information"
              ></textarea>
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-2 col-form-label">场馆封面：</label>
            <div class="col-lg-10">
              <el-upload
                ref="upload"
                action="http://127.0.0.1:8000/api/manager/stadiumimage/"
                name="image"
                accept="image/png,image/gif,image/jpg,image/jpeg"
                list-type="picture-card"
                :headers="{ loginToken: this.loginToken }"
                :data="{ stadium_id: this.id }"
                :limit="5"
                :auto-upload="false"
                :on-exceed="handleExceed"
                :before-upload="handleBeforeUpload"
              >
                <i class="el-icon-plus"></i>
              </el-upload>
              <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="" />
              </el-dialog>
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-2 col-form-label">开放时间：</label>
            <div class="col-lg-2">
              <div class="input-group clockpicker" data-autoclose="true">
                <input
                  type="text"
                  id="startpicker"
                  class="form-control"
                  v-model="period.start"
                  ref="openTime"
                />
                <span class="input-group-addon">
                  <span class="fa fa-clock-o"></span>
                </span>
              </div>
            </div>
            <div class="col-lg-1 text-center" style="line-height: 35.5px">
              至
            </div>
            <div class="col-lg-2">
              <div class="input-group clockpicker" data-autoclose="true">
                <input
                  type="text"
                  id="endpicker"
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
            <label class="col-lg-2 col-form-label" ref="duration"
              >最长提前预约天数：</label
            >
            <div class="col-lg-1">
              <input type="text" class="form-control" ref="foreDays" />
            </div>
          </div>
          <div class="form-group row" id="data_1">
            <label class="col-lg-2 col-form-label">修改生效日期：</label>
            <div class="col-lg-2 input-group date">
              <span class="input-group-addon"
                ><i class="fa fa-calendar"></i
              ></span>
              <input type="text" class="form-control" ref="startDate" />
            </div>
          </div>
          <div
            class="form-group row"
            style="border-top: 1px solid #e7eaec; padding-top: 10px;"
          >
            <label class="col-lg-2 col-form-label"><h3>地理位置</h3></label>
          </div>
          <div class="form-group row">
            <label class="col-lg-1 col-form-label">搜索：</label>
            <div class="col-lg-2">
              <input
                type="text"
                class="form-control"
                placeholder="输入地点..."
                v-model="keyword"
              />
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-1 col-form-label">经度：</label>
            <div class="col-lg-2">
              <input
                class="form-control"
                v-model.number="locData.longitude"
                :disabled="true"
              />
            </div>
            <label class="col-lg-1 col-form-label"> 纬度：</label>
            <div class="col-lg-2">
              <input
                class="form-control"
                v-model.number="locData.latitude"
                :disabled="true"
              />
            </div>
          </div>
          <div class="form-group row">
            <label class="col-lg-1 col-form-label"> 位置：</label>
            <div class="col-lg-2">
              <input class="form-control" v-model="locData.address" />
            </div>
          </div>
          <baidu-map
            class="map row"
            :center="center"
            :zoom="zoom"
            :scroll-wheel-zoom="true"
            @ready="handler"
            @click="clickEvent"
            ak="tB2ecRUc4qn4tYHD8p5Mu49qXUZWPeLU"
          >
            <bm-navigation anchor="BMAP_ANCHOR_TOP_RIGHT"></bm-navigation>
            <bm-geolocation
              anchor="BMAP_ANCHOR_BOTTOM_RIGHT"
              :showAddressBar="true"
              :autoLocation="true"
              @locationSuccess="getLocationSuccess"
            ></bm-geolocation>
            <bm-view
              :style="{
                width: '75%',
                height: '500px',
                flex: 1,
                marginTop: '0px',
                marginLeft: '15px',
                display: 'inline-block'
              }"
              class="col-lg-8"
            ></bm-view>
            <bm-local-search
              :keyword="keyword"
              :auto-viewport="false"
              style="height: 500px; overflow-y: scroll; margin: 2px 0; display: inline-block;"
              class="col-lg-4"
            ></bm-local-search>
          </baidu-map>
          <div class="form-group row" style="text-align: center;">
            <div class="col-lg-12">
              <button
                type="button"
                class="btn btn-primary"
                style="margin: 5px;"
                v-on:click="submit()"
              >
                提交
              </button>
              <button
                type="button"
                class="btn btn-default"
                style="margin: 5px;"
                v-on:click="cancel()"
              >
                取消
              </button>
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
import {
  BaiduMap,
  BmNavigation,
  BmView,
  BmGeolocation,
  BmCityList,
  BmLocalSearch
} from "vue-baidu-map";
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";
export default {
  data() {
    return {
      id: null,
      loginToken: localStorage.getItem('loginToken'),
      period: {
        start: "",
        end: ""
      },
      active_time: "",
      name: "",
      openTime: "",
      closeTime: "",
      dialogImageUrl: "",
      dialogVisible: false,
      // params for map
      center: {
        lng: 116.3328,
        lat: 40.008
      },
      zoom: 16,
      keyword: "",
      // params for upload form
      locData: {
        longitude: "",
        latitude: "",
        address: ""
      }
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer,
    BaiduMap,
    BmNavigation,
    BmView,
    BmGeolocation,
    BmCityList,
    BmLocalSearch
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
    });
  },
  beforeUpdate() {
    this.openTime = $("#startpicker")[0].value;
    this.closeTime = $("#endpicker")[0].value;
  },
  updated() {
    this.$refs.openTime.value = this.openTime;
    this.$refs.closeTime.value = this.closeTime;
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
    });
  },
  methods: {
    submit() {
      swal(
        {
          title: "你确定？",
          text: "确认要创建新场馆",
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
            this.uploadForm();
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
    handleExceed(files, fileList) {
      swal({
        title: "图片数量超出限制",
        text: "最多上传5张场馆图片",
        type: "error"
      });
    },
    handleBeforeUpload(file) {
      if (
        !(
          file.type === "image/png" ||
          file.type === "image/gif" ||
          file.type === "image/jpg" ||
          file.type === "image/jpeg"
        )
      ) {
        swal({
          title: "图片格式错误",
          text: "请上传png/gif/jpg/jpeg格式的图片",
          type: "error"
        });
      }
      let size = file.size / 1024 / 1024 / 2;
      if (size > 5) {
        swal({
          title: "图片过大",
          text: "每张照片不得超过5M",
          type: "error"
        });
      }
    },
    uploadForm() {
      let request_body = {};
      request_body = {
        managerId: localStorage.getItem("id"),
        name: this.$refs.name.value,
        openState: 0,
        createTime: this.$refs.startDate.value,
        foreDays: this.$refs.foreDays.value,
        information: this.$refs.information.value,
        contact: this.$refs.contact.value,
        longitude: this.locData.longitude.toString(),
        latitude: this.locData.latitude.toString(),
        location: this.locData.address,
        openTime: $("#startpicker")[0].value,
        closeTime: $("#endpicker")[0].value
      };
      console.log(request_body);
      this.$axios
        .post("stadium/", request_body)
        .then(res => {
          this.id = res.data.id;
        })
        .then(id => {
          this.$refs.upload.submit();
        })
        .then(() => {
          swal(
            {
              title: "创建场馆成功",
              text: "请前往编辑场地信息。",
              type: "success"
            },
            function() {
              window.location.replace("/stadium_management/stadium_info");
            }
          );
        })
        .catch(err => {
          console.log(err);
        });
    },
    handler({ BMap, map }) {
      let _this = this; // 设置一个临时变量指向vue实例，因为在百度地图回调里使用this，指向的不是vue实例；
      let geolocation = new BMap.Geolocation();
      geolocation.getCurrentPosition(
        function(r) {
          //console.log(r);
          //_this.center = { lng: r.longitude, lat: r.latitude }; // 设置center属性值
          //_this.autoLocationPoint = { lng: r.longitude, lat: r.latitude }; // 自定义覆盖物
          //_this.initLocation = true;
        },
        { enableHighAccuracy: true }
      );
      window.map = map;
    },
    clickEvent(e) {
      map.clearOverlays();
      let myMarker = new BMap.Marker(new BMap.Point(e.point.lng, e.point.lat));
      map.addOverlay(myMarker);
      //用所定位的经纬度查找所在地省市街道等信息
      let point = new BMap.Point(e.point.lng, e.point.lat);
      let gc = new BMap.Geocoder();
      let _this = this;
      gc.getLocation(point, function(rs) {
        let addComp = rs.addressComponents;
        _this.locData.address = rs.address;
      });
      this.locData.longitude = e.point.lng;
      this.locData.latitude = e.point.lat;
    },
    getLocationSuccess(point, AddressComponent, marker) {
      map.clearOverlays();
      let Icon_0 = new BMap.Icon(
        "http://api0.map.bdimg.com/images/marker_red_sprite.png",
        new BMap.Size(64, 64),
        { anchor: new BMap.Size(18, 32), imageSize: new BMap.Size(36, 36) }
      );
      let myMarker = new BMap.Marker(
        new BMap.Point(point.point.lng, point.point.lat),
        { icon: Icon_0 }
      );
      map.addOverlay(myMarker);
      this.locData.longitude = point.point.lng;
      this.locData.latitude = point.point.lat;
    }
  }
};
</script>
