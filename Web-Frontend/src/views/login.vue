<template>
  <div class="loginColumns animated fadeInDown">
    <div class="row" style="text-align: center;">
      <div class="col-md-6">
        <h1 class="font-bold" style="color: white;">清动家园管理系统</h1>
        <!--TODO: 这里可以放一些东西不然有点空。-->
      </div>
      <div class="col-md-6">
        <div class="ibox-content">
          <div class="m-t">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                placeholder="学号/工号"
                required=""
                v-model="id"
              />
            </div>
            <div class="form-group">
              <input
                type="password"
                class="form-control"
                placeholder="密码"
                required=""
                v-model="pwd"
              />
            </div>
            <button
              v-on:click="submit()"
              class="btn btn-primary block full-width m-b"
            >
              登录
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="row m-t">
      <div class="col-md-6" style="color: white;">
        <small
          ><strong>Copyright</strong> THSS - Software Engineering Course @ 2020
          Autumn</small
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      pwd: ""
    }
  },
  methods: {
    submit() {
      this.$axios.post("login/", { userId: this.id, password: this.pwd }).then(res => {
        if (res.data.error){
          alert("Error! Please try again.");
        }
        else{
          localStorage.setItem('loginToken',res.data.loginToken);
          localStorage.setItem("username", res.data.username);
          localStorage.setItem("id", res.data.id);
          window.location.replace("/home");
        }
      });
    }
  }
};
</script>
