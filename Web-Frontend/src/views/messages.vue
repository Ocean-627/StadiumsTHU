<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>
            信箱
          </h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>信箱</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce"
       style="text-align: center;">
       
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
