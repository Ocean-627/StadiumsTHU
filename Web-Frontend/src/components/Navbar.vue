<template>
  <div id="Navbar" class="container">
    <ul class="nav nav-justified">
      <li class="nav-item">
        <a class="nav-link active" href="#/home">首页</a>
      </li>
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          data-toggle="dropdown"
          role="button"
          aria-haspopup="true"
          aria-expanded="false"
          >场馆管理</a
        >
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">场馆信息管理</a>
          <a class="dropdown-item" href="#">用户反馈管理</a>
          <a class="dropdown-item" href="#">场馆预留</a>
          <a class="dropdown-item" href="#">预订记录</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          data-toggle="dropdown"
          role="button"
          aria-haspopup="true"
          aria-expanded="false"
          >用户管理</a
        >
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">用户信息</a>
          <a class="dropdown-item" href="#">黑名单管理</a>
        </div>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">操作记录</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">统计分析</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">系统日志</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
#Navbar {
    padding-left: 10%;
    padding-right: 10%;
}
</style>

<script>
export default {
  data() {
    return {};
  },
};
</script>