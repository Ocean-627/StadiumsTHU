<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>
            编辑场馆信息<small> @ {{ name }}</small>
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
              <strong>编辑场馆信息</strong>
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
                :file-list="fileList"
                :data="{ stadium_id: this.$route.query.id }"
                :limit="5"
                :auto-upload="false"
                :on-exceed="handleExceed"
                :on-remove="handleRemove"
                :before-upload="handleBeforeUpload"
              >
                <i class="el-icon-plus"></i>
              </el-upload>
              <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="" />
              </el-dialog>
            </div>
          </div>
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
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";
export default {
  data() {
    return {
      period: {
        start: "",
        end: ""
      },
      loginToken: localStorage.getItem('loginToken'),
      active_time: "",
      name: "",
      fileList: [],
      url2id: {},
      dialogImageUrl: "",
      dialogVisible: false
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
    });
    let request = {
      params: {
        id: this.$route.query.id
      }
    };
    this.$axios.get("stadium/", request).then(res => {
      this.name = res.data[0].name;
      this.$refs.name.value = res.data[0].name;
      this.$refs.contact.value = res.data[0].contact;
      this.$refs.information.value = res.data[0].information;
      for (let i of res.data[0].images) {
        this.fileList.push({
          url: i.image
        });
        this.url2id[i.image] = { id: i.id, deleted: false };
      }
    });
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
      format: "yyyy-mm-dd",
      startDate: new Date()
    });
  },
  methods: {
    submit() {
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
    handleRemove(file, fileList) {
      this.url2id[file.url].deleted = true;
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
      let request_body = {
        stadium_id: this.$route.query.id,
        managerId: localStorage.getItem("id"),
        name: this.$refs.name.value,
        information: this.$refs.information.value,
        contact: this.$refs.contact.value
      };
      this.$refs.upload.submit();
      for (let i in this.url2id) {
        if (this.url2id[i].deleted) {
          this.$axios
            .delete("stadiumimage/", { data: { id: this.url2id[i].id }})
        }
      }
      this.$axios({
        method: "put",
        url: "stadium/",
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        },
        data: request_body
      }).then(res => {
        swal(
          {
            title: "成功",
            text: "场馆信息修改成功",
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
