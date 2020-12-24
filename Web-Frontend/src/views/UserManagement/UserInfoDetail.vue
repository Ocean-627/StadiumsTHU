<template>
  <div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
      <Header></Header>
      <div class="row wrapper border-bottom white-bg page-heading">
        <!--Breadcrum 导航-->
        <div class="col-lg-9">
          <h2>用户信息</h2>
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <a href="/home">主页</a>
            </li>
            <li class="breadcrumb-item">
              <a href="/user_management">用户管理</a>
            </li>
            <li class="breadcrumb-item active">
              <strong>详细信息</strong>
            </li>
          </ol>
        </div>
      </div>
      <div
        class="wrapper wrapper-content animated fadeInRight ecommerce white-bg"
        style="text-align: center;"
        v-if="loaded"
      >
        <div class="row dashboard-header">
          <div class="col-md-3">
            <img
              class="img-circle img-responsive"
              :src="user.image"
              :onerror="defaultImg"
              style="height: 150px; width:150px;"
            />
          </div>
          <div class="col-md-2">
            <h1 style="padding-top: 30px">
              <strong>{{ user.nickName }}</strong>
            </h1>
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>姓名</strong>
          </div>
          <div class="col-md-2">
            {{ user.name }}
          </div>
          <div class="col-md-1 border-right"></div>
          <div class="col-md-3">
            <strong>邮箱</strong>
          </div>
          <div class="col-md-2">
            {{ user.email }}
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>学号/工号</strong>
          </div>
          <div class="col-md-2">
            {{ user.userId }}
          </div>
          <div class="col-md-1 border-right"></div>
          <div class="col-md-3">
            <strong>手机</strong>
          </div>
          <div class="col-md-2">
            {{ user.phone }}
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>用户类别</strong>
          </div>
          <div class="col-md-2">
            {{ user.type }}
          </div>
          <div class="col-md-1 border-right"></div>
          <div class="col-md-3">
            <strong>最近登录时间</strong>
          </div>
          <div class="col-md-2">
            {{ user.loginTime | datetime_format }}
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>黑名单状态</strong>
          </div>
          <div class="col-md-1" v-if="user.inBlacklist">
            是
          </div>
          <div class="col-md-4" v-if="user.inBlacklist">
            （拉黑于{{ user.inBlacklistTime | datetime_format("YYYY-MM-DD") }}）
            <button
              class="btn btn-sm btn-outline btn-danger"
              style="float: right;"
              v-on:click="black_out()"
            >
              移出黑名单
            </button>
          </div>
          <div class="col-md-3" v-if="!user.inBlacklist">
            否
            <button
              class="btn btn-sm btn-outline btn-danger"
              style="float: right;"
              v-on:click="black_in()"
            >
              移入黑名单
            </button>
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>预约记录</strong>
          </div>
          <div class="col-md-8">
            <table class="table">
              <thead>
                <th>#</th>
                <th>地点</th>
                <th>使用时间</th>
                <th>预约时间</th>
                <th>状态</th>
              </thead>
              <tbody
                v-for="(reserve_record, index) in reserve_records"
                :key="reserve_record.id"
              >
                <tr>
                  <td>{{ index + 1 }}</td>
                  <td>{{ reserve_record | reserve_place }}</td>
                  <td>
                    {{
                      reserve_record.date +
                        " " +
                        reserve_record.startTime +
                        "-" +
                        reserve_record.endTime
                    }}
                  </td>
                  <td>{{ reserve_record.createTime | datetime_format }}</td>
                  <td :style="reserve_record | reserve_status_class">
                    {{ reserve_record | reserve_status }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="row" v-if="this.reserve_total > this.reserve_page * 15">
          <div class="col-md-11">
            <button
              class="btn btn-sm btn-outline btn-info"
              style="float: right; margin-top: -10px; margin-right: 10px; margin-bottom: 15px;"
              v-on:click="page_reserve()"
            >
              加载更多
            </button>
          </div>
        </div>
        <div class="row i-row">
          <div class="col-md-3">
            <strong>信用记录</strong>
          </div>
          <div class="col-md-8">
            <table class="table">
              <thead>
                <th>#</th>
                <th>内容</th>
                <th>时间</th>
                <th>生效状态</th>
                <th>操作</th>
              </thead>
              <tbody
                v-for="(credit_record, index) in credit_records"
                :key="credit_record.id"
              >
                <tr>
                  <td>{{ index }}</td>
                  <td>{{ credit_record.detail }}</td>
                  <td>{{ credit_record.date + " " + credit_record.time }}</td>
                  <td :style="credit_record | credit_status_style">
                    {{ credit_record | credit_status }}
                  </td>
                  <td style="padding: 5px;">
                    <button
                      class="btn btn-xs btn-danger btn-outline"
                      v-show="!credit_record.cancel && credit_record.valid"
                      v-on:click="cancel_credit(credit_record.id)"
                    >
                      撤销
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="row" v-if="this.credit_total > this.credit_page * 15">
          <div class="col-md-11">
            <button
              class="btn btn-sm btn-outline btn-info"
              style="float: right; margin-top: -10px; margin-right: 10px; margin-bottom: 15px;"
              v-on:click="page_reserve()"
            >
              加载更多
            </button>
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
      loaded: false,
      user: {},
      reserve_records: [],
      reserve_page: 1,
      reserve_total: null,
      credit_records: [],
      credit_page: 1,
      credit_total: null,
      blacklist_records: []
    };
  },
  components: {
    Toolbox,
    Navbar,
    Header,
    Footer
  },
  filters: {
    reserve_place: function(reserve_record) {
      return reserve_record.stadium + "(" + reserve_record.court + ")";
    },
    reserve_status: function(record) {
      if (record.cancel) return "已取消";
      if (!record.payment) return "未付款";
      if (record.leave) return "已结束";
      if (record.checked && !record.leave) return "使用中";
      return "未使用";
    },
    reserve_status_class: function(record) {
      if (record.cancel) return "color: orange;";
      if (!record.payment) return "color: #dc3545";
      if (record.leave) return "color: #6c757d";
      if (record.checked && !record.leave) return "color: #17a2b8";
      return "color: #28a745";
    },
    credit_status: function(r) {
      if (r.cancel) return "已撤销";
      if (!r.valid) return "已过期";
      return "生效中";
    },
    credit_status_style: function(r) {
      if (r.cancel) return "color: orange;";
      if (!r.valid) return "";
      return "color: #23c6c8;";
    }
  },
  methods: {
    page_reserve() {
      this.$axios
        .get("reserveevent/", {
          params: { user_id: this.user.id, page: ++this.reserve_page }
        })
        .then(res => {
          this.reserve_records.push(...res.data.results);
        });
    },
    page_credit() {
      this.$axios
        .get("default/", {
          params: { user_id: this.user.id, page: ++this.credit_page }
        })
        .then(res => {
          this.credit_records.push(...res.data.results);
        });
    },
    cancel_credit(id) {
      let func = this.axios
        .get("default/", { params: { id: id } })
        .then(res => {
          swal(
            {
              title: "成功",
              text: "撤销成功",
              type: "success"
            },
            () => {
              location.reload(0);
            }
          );
        });
      swal(
        {
          title: "确定要撤销这条操作吗？",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "确认",
          cancelButtonText: "取消"
        },
        res => {
          if (!res) return;
          func;
        }
      );
    },
    black_in() {
      swal(
        {
          title: "确定要拉黑该用户吗？",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          closeModal: false
        },
        res => {
          if (!res) return;
          this.$axios
            .post("blacklist/", {
              user_id: this.user.id
            })
            .then(res => {
              swal(
                {
                  title: "成功",
                  text: "成功加入黑名单",
                  type: "success"
                },
                () => {
                  location.reload(0);
                }
              );
            });
        }
      );
    },
    black_out() {
      swal(
        {
          title: "确定要解除黑名单吗？",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          closeModal: false
        },
        res => {
          if (!res) return;
          this.$axios
            .put("blacklist/", {
              user_id: this.user.id
            })
            .then(res => {
              swal(
                {
                  title: "成功",
                  text: "成功移除黑名单",
                  type: "success"
                },
                () => {
                  location.reload(0);
                }
              );
            });
        }
      );
    }
  },
  mounted() {
    this.$axios
      .get("user/", {
        params: { userId: this.$route.params.userId }
      })
      .then(res => {
        this.user = res.data.results[0];
        return Promise.all([
          this.$axios.get("reserveevent/", {
            params: { user_id: this.user.id }
          }),
          this.$axios.get("default/", {
            params: { user_id: this.user.id }
          })
        ]);
      })
      .then(res => {
        this.reserve_records = res[0].data.results;
        this.reserve_total = res[0].data.count;
        this.credit_records = res[1].data.results;
        this.credit_total = res[1].data.count;
        this.loaded = true;
      });
  },
  computed: {
    defaultImg() {
      return 'this.src="' + require("../../../static/img/white.jpg") + '"';
    }
  },
};
</script>
