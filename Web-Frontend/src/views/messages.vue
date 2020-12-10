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
        <div class="row" style="margin-bottom: 20px">
          <div class="col-sm-2">
            <select
              class="chosen-select"
              value="0"
              id="type"
            >
              <option v-for="(type, index) in type_list" :key="type" :value="index">
                {{ type }}
              </option>
            </select>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-12">
            <div class="ibox-content forum-post-container">
              <div class="media" v-for="session in sessions" :key="session.id" :class="session.type | style_filter">
                <a class="forum-avatar" :href="'/user_management/user_info/detail/' + session.userId">
                  <img
                    :src="session.usericon"
                    class="rounded-circle"
                    alt="image"
                  />
                  <div class="author-info">
                    <strong>{{ session.user }}</strong
                    ><br />
                    {{ session.updateTime | datetime_format_2 }}<br />
                  </div>
                </a>
                <div class="media-body">
                  <h4 class="media-heading" v-on:click="goDetail(session.id)" style="cursor: pointer;">
                      “{{ session.digest }}...”
                  </h4>
                  {{ (session.latestmsg.sendertype === "manager") ? "管理员" : "用户" }} <strong>{{ session.latestmsg.sender }}</strong> 的最新回复：
                  <br /><br />
                  {{ session.latestmsg.content }}
                </div>
              </div>
              <nav aria-label="navigation">
                <ul class="pagination justify-content-center" style="margin-top: 15px; margin-bottom: 10px;">
                  <li class="page-item" v-show="page > page_size">
                    <a class="page-link" aria-label="Previous" v-on:click="prepage()">
                      <span aria-hidden="true">&laquo;</span>
                    </a>
                  </li>
                  <li class="page-item" v-for="i in cur_pages()" :key="i">
                    <a class="page-link" v-on:click="setpage(i)">{{ page_size * Math.floor((page-1) / page_size) + i }}</a>
                  </li>
                  <li class="page-item" v-show="page + page_size < total">
                    <a class="page-link" aria-label="Next" v-on:click="nextpage()">
                      <span aria-hidden="true">&raquo;</span>
                    </a>
                  </li>
                </ul>
              </nav>
              <div style="text-align: center;">
                  第 {{ this.page }}/{{ this.total }} 页
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
@import "../assets/css/plugins/chosen/bootstrap-chosen.css";
.i-row {
  padding-top: 10px;
  padding-bottom: 10px;
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
import "@/assets/js/plugins/chosen/chosen.jquery.js";
export default {
  data() {
    return {
      sessions: [
        {
          id: 1,
          user: "马保国",
          userId: 3,
          usericon: "../../static/img/mabaoguo.jpg",
          updateTime: new Date() - 100000,
          digest: "朋友们好，我是混元形意",
          type: 0,
          latestmsg: {
              content: "马老师，发生什么事了？",
              sendertype: "manager",
              sender: "cbx"
          }
        },
        {
          id: 2,
          user: "马保国",
          userId: 3,
          usericon: "../../static/img/mabaoguo.jpg",
          updateTime: new Date() - 100000,
          digest: "朋友们好，我是混元形意",
          type: 1,
          latestmsg: {
              content: "马老师，发生什么事了？",
              sendertype: "manager",
              sender: "cbx"
          }
        },
        {
          id: 3,
          user: "马保国",
          userId: 3,
          usericon: "../../static/img/mabaoguo.jpg",
          updateTime: new Date() - 100000,
          digest: "朋友们好，我是混元形意",
          type: 2,
          latestmsg: {
              content: "马老师，发生什么事了？",
              sendertype: "manager",
              sender: "cbx"
          }
        }
      ],
      page: 1,
      page_size: 10,
      total: 123,   // total page count
      type_list: ["全部", "待处理", "已处理", "已关闭"],
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
      this.$axios.get("messages/")
  },
  updated(){
      $(".chosen-select").chosen({ width: "100%" });
  },
  methods: {
      prepage(){
          this.page -= this.page % this.page_size + this.page_size - 1
      },
      nextpage(){
          this.page -= this.page % this.page_size
          this.page += this.page_size + 1
      },
      cur_pages(){
          let tmp = this.page - this.page % this.page_size
          return Math.min(this.page_size, this.total - tmp);
      },
      setpage(i){
          this.page = this.page_size * Math.floor((this.page - 1) / this.page_size) + i
      },
      goDetail(id){
          window.location.replace("/messages/detail?id=" + id)
      },
  },
  filters: {
      style_filter(type){
          if(type === 0) return "black-bg";     // solved
          if(type === 1) return "gray-bg";      // open
          if(type === 2) return "yellow-bg";    // unsolved
      }
  },
};
</script>
