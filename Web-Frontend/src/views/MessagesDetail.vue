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
      <div
        class="wrapper wrapper-content white-bg animated fadeInRight ecommerce"
        style="margin-top: 15px;"
      >
        <div class="row">
          <div class="col-lg-8">
            <div class="small-chat-box active">
              <div class="heading" draggable="true">
                <small class="chat-date float-right">
                  {{ session.updateTime | datetime_format_2 }} </small
                >消息列表
              </div>
              <div class="content">
                <div
                  v-for="msg in messages"
                  :key="msg.id"
                  :class="msg | msg_class"
                >
                  <div class="author-name">
                    {{ msg | msg_name(session.user_name) }}
                    <small class="chat-date">
                      {{ msg.createTime | datetime_format }}
                    </small>
                  </div>
                  <div :class="msg | content_class">
                    {{ msg.content }}
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
.i-row {
  padding-top: 10px;
  padding-bottom: 10px;
}
.small-chat-box {
  position: relative;
  bottom: 0;
  right: 0;
  border: none;
  background-color: #fff;
}
.small-chat-box.active {
  display: inline;
}
.small-chat-box .heading {
    font-size: 16px;
}
.small-chat-box .content .author-name {
    font-size: 15px;
}
.small-chat-box .chat-date {
    font-size: 14px;
}
.small-chat-box .content .chat-message {
    font-size: 15px;
    padding: 10px 15px;
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
      session: {
        user_name: "cbx",
        updateTime: new Date() - 2e6
      },
      messages: [
        {
          id: 1,
          session: 1,
          sender: "U",
          manager_id: null,
          manager_name: null,
          content: "我就告诉你啥呢",
          createTime: new Date() - 2e7
        },
        {
          id: 2,
          session: 1,
          sender: "M",
          manager_id: 1,
          manager_name: "刘强",
          content: "就是说啥呢",
          createTime: new Date() - 1e7
        },
        {
          id: 3,
          session: 1,
          sender: "U",
          manager_name: null,
          manager_id: null,
          content: "就是为什么就是说啥呢",
          createTime: new Date() - 8e6
        },
        {
          id: 4,
          session: 1,
          sender: "M",
          manager_id: 1,
          manager_name: "刘强",
          content: "我这样跟你对话呢",
          createTime: new Date() - 7e6
        },
        {
          id: 6,
          session: 1,
          sender: "U",
          manager_id: null,
          manager_name: null,
          content: "因为咱们就是说啥呢",
          createTime: new Date() - 6e6
        },
        {
          id: 7,
          session: 1,
          sender: "U",
          manager_id: null,
          manager_name: null,
          content: "真的！",
          createTime: new Date() - 5e6
        },
        {
          id: 8,
          session: 1,
          sender: "M",
          manager_id: 1,
          content: "就是说啥呢",
          manager_name: "刘强",
          createTime: new Date() - 3e6
        },
        {
          id: 10,
          session: 1,
          sender: "M",
          manager_id: 1,
          content: "来你回来你回来",
          manager_name: "刘强",
          createTime: new Date() - 2e6
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
  mounted() {
    this.$axios
      .get("session/", {
        params: {
          id: this.$route.query.id
        }
      })
      .then(res => {
        this.session = res.data.results[0];
        console.log(this.session);
      });
  },
  updated() {},
  methods: {},
  filters: {
    msg_class: function(msg) {
      if (msg.sender === "U" || msg.manager_id != localStorage.getItem("id"))
        return "left";
      return "right";
    },
    content_class: function(msg) {
      if (msg.sender === "U" || msg.manager_id != localStorage.getItem("id"))
        return "chat-message active";
      return "chat-message";
    },
    msg_name: function(msg, default_name) {
      if (msg.sender === "U") return default_name;
      return msg.manager_name;
    }
  }
};
</script>
