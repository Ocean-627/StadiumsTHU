<template>
    <div class="loginColumns animated fadeInDown">
        <div class="row" style="text-align: center;">
            <div class="col-md-6">
                <h1 class="font-bold" style="color: white;">清动家园管理系统</h1>
                <!--TODO: 这里可以放一些东西不然有点空。-->
            </div>
            <div class="col-md-6">
                <div class="ibox-content">
                    <form class="m-t">
                        <div class="form-group">
                            <input type="text" class="form-control" placeholder="学号/工号" required="">
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="密码" required="">
                        </div>
                        <button v-on:click="submit()" class="btn btn-primary block full-width m-b">登录</button>
                    </form>
                </div>
            </div>
        </div>
      
        <div class="row m-t">
            <div class="col-md-6" style="color: white;">
               <small><strong>Copyright</strong> THSS - Software Engineering Course @ 2020 Autumn</small>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    },
    methods: {
        submit() {

        }
    }
}
</script>