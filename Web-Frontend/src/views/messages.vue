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
      <div class="wrapper wrapper-content animated fadeInRight ecommerce">
        <div class="row">
          <div class="col-lg-12">
            <div class="ibox-content forum-post-container">
              <div class="forum-post-info">
                <h4>
                  <span class="text-navy"
                    ><i class="fa fa-globe"></i>一般性讨论 </span
                  >-公告- <span class="text-muted">自由会谈</span>
                </h4>
              </div>
              <div class="media" v-for="session in sessions" :key="session.id">
                <a class="forum-avatar" href="#">
                  <img src="/static/img/a1.jpg" class="rounded-circle" alt="image" />
                  <div class="author-info">
                    <strong>{{ session.user }}</strong><br />
                    {{ session.latestUpdateTime | datetime_format_2 }}<br />
                  </div>
                </a>
                <div class="media-body">
                  <h4 class="media-heading">月牙草的标准块</h4>
                  与普遍的看法相反，Lorem
                  Ipsum并不是简单的随机文本。它起源于公元前45年的一部古典拉丁文学作品，距今已有2000多年的历史。

                  <br /><br />弗吉尼亚州汉普顿悉尼学院（Hampden Sydney
                  College）的拉丁文教授理查德麦克林托克（Richard
                  McClintock）查阅了一段洛伦伊普苏姆（Lorem
                  Ipsum）的文章中较为晦涩的拉丁文单词consectetur，并查阅了古典文学中对这个单词的引用，发现了不容置疑的来源。Lorem
                  Ipsum来自西塞罗在公元前45年所著的《德菲尼布斯博诺勒姆和马洛勒姆》（善与恶的极端）的第1.10.32节和第1.10.33节。这本书是一本关于伦理学的论文，在文艺复兴时期非常流行。Lorem
                  Ipsum的第一行“Lorem Ipsum dolor sit
                  amet…”来自第1.10.32节中的一行。

                  <br /><br />迈克·史密斯，Zender公司首席执行官。
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
        sessions: [
            {
                id: 1,
                user: "cbx",
                latestUpdateTime: new Date() - 100000
            }
        ]
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
  },
  mounted() {}
};
</script>
