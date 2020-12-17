<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>
            个人信息
          </h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>个人信息</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce"
       style="text-align: center;">
       <div class="row dashboard-header">
          <div class="col-md-3">
            <img
              alt="image"
              class="img-circle img-responsive"
              :src="manager.image"
              style="height: 150px; width:150px;"
            />
          </div>
          <div class="col-md-2">
            <h1 style="padding-top: 30px"><strong>{{ username }}</strong></h1>
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>姓名</strong>
          </div>
          <div class="col-md-2">
            {{ manager.name }}
          </div>
          <div class="col-md-1 border-right"></div>
          <div class="col-md-3">
            <strong>邮箱</strong>
          </div>
          <div class="col-md-2">
            {{ manager.email }}
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>管理员id</strong>
          </div>
          <div class="col-md-2">
            {{ manager.id }}
          </div>
          <div class="col-md-1 border-right"></div>
          <div class="col-md-3">
            <strong>手机</strong>
          </div>
          <div class="col-md-2">
            {{ manager.phone }}
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>最近登录时间</strong>
          </div>
          <div class="col-md-2">
            {{ manager.loginTime | datetime_format }}
          </div>
          <div class="col-md-1 border-right"></div>
        </div>
      </div>
      <Footer></Footer>
    </div>
    <Toolbox></Toolbox>
  </div>
</template>

<style scoped>
.i-row {
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>

<script>
import Navbar from "@/components/Navbar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Toolbox from "@/components/Toolbox";
export default {
  data() {
    return {
      username: localStorage.getItem("username"),
      manager: {
          image: "/static/img/dog.jpg",
          phone: 62782865,
          email: "cbx@qq.com",
          name: "孙笑川",
          id: 1
        }
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
  },
  mounted() {
    
  }
};
</script>
