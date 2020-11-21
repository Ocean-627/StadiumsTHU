<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {}
  },
  watch: {
    //'$route'(to, from) {
    //  this.$router.go(0);
    //}
  }
}
</script>

<style>
@import '/assets/css/bootstrap.min.css';
@import '/assets/font-awesome/css/font-awesome.css';
@import '/assets/css/plugins/toastr/toastr.min.css';
@import '/assets/js/plugins/gritter/jquery.gritter.css';
@import '/assets/css/plugins/sweetalert/sweetalert.css';
@import '/assets/css/animate.css';
@import '/assets/css/style.css';
</style>
