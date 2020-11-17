<template>
    <div class="loginColumns animated fadeInDown">
        <div class="row">

            <div class="col-md-6">
                <h1 class="font-bold">清动家园管理系统</h1>
                <!--TODO: 这里可以放一些东西不然有点空。-->
            </div>
            <div class="col-md-6">
                <div class="ibox-content">
                    <form class="m-t" role="form" action="index.html">
                        <div class="form-group">
                            <input type="email" class="form-control" placeholder="用户名" required="">
                        </div>
                        <div class="form-group">
                            <input type="password" class="form-control" placeholder="密码" required="">
                        </div>
                        <button type="submit" class="btn btn-primary block full-width m-b">登录</button>

                        <a href="#">
                            <small>忘记密码?</small>
                        </a>

                        <p class="text-muted text-center">
                            <small>还没有账号?</small>
                        </p>
                        <a class="btn btn-sm btn-white btn-block" href="register.html">创建一个帐户</a>
                    </form>
                    <p class="m-t">
                    </p>
                </div>
            </div>
        </div>
        <hr/>
        <div class="row">
            <div class="col-md-6">
               <small><strong>Copyright</strong> THSS - Software Engineering Course @ 2020 Autumn</small>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    }
}
</script>