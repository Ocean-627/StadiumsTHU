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
          <div class="small-chat-box">
        <div class="heading" draggable="true">
                <small class="chat-date float-right">02.19.2015

                </small>闲聊

            </div>

            <div class="content">

                <div class="left">
                    <div class="author-name">莫妮卡·杰克逊
                        <small class="chat-date">10： 上午2点

                        </small>
                    </div>
                    <div class="chat-message active">Lorem Ipsum只是虚拟文本输入。

                    </div>

                </div>
                <div class="right">
                    <div class="author-name">米克·史密斯

                        <small class="chat-date">11： 24点

                        </small>
                    </div>
                    <div class="chat-message">阴唇是简单的。

                    </div>
                </div>
                <div class="left">
                    <div class="author-name">爱丽丝·诺瓦克。

                        <small class="chat-date">晚上8:45

                        </small>
                    </div>
                    <div class="chat-message active">检查这个库存字符。

                    </div>
                </div>
                <div class="right">
                    <div class="author-name">安娜·拉姆森。

                        <small class="chat-date">11： 24点

                        </small>
                    </div>
                    <div class="chat-message">月牙草的标准块

                    </div>
                </div>
                <div class="left">
                    <div class="author-name">米克巷

                        <small class="chat-date">晚上8:45

                        </small>
                    </div>
                    <div class="chat-message active">我相信。Lorem Ipsum只是一个虚拟文本。

                    </div>
                </div>


            </div>
            <div class="form-chat">
                <div class="input-group input-group-sm">
                    <input type="text" class="form-control">
                    <span class="input-group-btn"> <button class="btn btn-primary" type="button">发送
                        </button> </span></div>
            </div>
          </div>
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
