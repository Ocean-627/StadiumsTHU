<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>
            消息详情
          </h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item active">
              <a href="/messages">信箱</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>消息详情</strong>
            </li>
          </ol>
        </div>
      </div>
      <div class="wrapper wrapper-content animated fadeInRight ecommerce">
        
      </div>
      <Footer></Footer>
    </div>
    <Toolbox></Toolbox>
  </div>
</template>

<style>
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
      session: {}
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
  },
  mounted() {
      this.$axios.get("session/", {
          params: {
              id: this.$route.query.id
          }
      })
      .then(res => {
          this.session = res.data.results[0]
          console.log(this.session)
      })
  },
  updated(){
    
  },
  methods: {

  },
  filters: {

  },
};
</script>
