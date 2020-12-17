<template>
    <div class="row border-bottom">
        <nav class="navbar navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <a class="navbar-minimalize minimalize-styl-2 btn btn-primary " href="#"><i
                        class="fa fa-bars"></i> </a>
            </div>
            <ul class="nav navbar-top-links navbar-right">
                <li class="dropdown">
                    <a class="dropdown-toggle count-info" data-toggle="dropdown" href="#">
                        <i class="fa fa-envelope"></i> <span class="label label-warning">16</span>
                    </a>
                    <ul class="dropdown-menu dropdown-messages dropdown-menu-right">
                        <li>
                            <div class="dropdown-messages-box">
                                <a class="dropdown-item float-left" href="profile.html">
                                    <img alt="image" class="rounded-circle" :src="messages[0].image">
                                </a>
                                <div class="media-body">
                                    <small class="float-right">{{ messages[0].time | datetime_format_2 }}</small>
                                    来自 <strong>{{ messages[0].user }}</strong> 的消息<br>
                                    <small class="text-muted">{{ messages[0].time | datetime_format }}</small>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown-divider"></li>
                        <li>
                            <div class="dropdown-messages-box">
                                <a class="dropdown-item float-left" href="profile.html">
                                    <img alt="image" class="rounded-circle" :src="messages[1].image">
                                </a>
                                <div class="media-body">
                                    <small class="float-right">{{ messages[1].time | datetime_format_2 }}</small>
                                    来自 <strong>{{ messages[1].user }}</strong> 的消息<br>
                                    <small class="text-muted">{{ messages[1].time | datetime_format }}</small>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown-divider"></li>
                        <li>
                            <div class="dropdown-messages-box">
                                <a class="dropdown-item float-left" :src="messages[2].image">
                                    <img alt="image" class="rounded-circle" src="../../static/img/a7.jpg">
                                </a>
                                <div class="media-body">
                                    <small class="float-right">{{ messages[2].time | datetime_format_2 }}</small>
                                    来自 <strong>{{ messages[2].user }}</strong> 的消息<br>
                                    <small class="text-muted">{{ messages[2].time | datetime_format }}</small>
                                </div>
                            </div>
                        </li>
                        <li class="dropdown-divider"></li>
                        <li>
                            <div class="text-center link-block">
                                <a href="/messages" class="dropdown-item">
                                    <i class="fa fa-envelope"></i> <strong>阅读所有消息</strong>
                                </a>
                            </div>
                        </li>
                    </ul>
                </li>
                <li style="padding: 20px">
                    <span class="m-r-sm text-muted welcome-message">{{ time }}</span>
                </li>
                <li>
                    <a href="/login">
                        <i class="fa fa-sign-out"></i> 注销
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    data() {
        return {
            time: "",
            messages: [
                {
                    user: "cbx",
                    time: new Date(),
                    image: "/static/img/dog.jpg"
                },
                {
                    user: "cnx",
                    time: new Date() - 200000,
                    image: "/static/img/a1.jpg"
                },
                {
                    user: "hhy",
                    time: new Date() - 3890000,
                    image: "/static/img/a3.jpg"
                }
            ]
        }
    },
    created() {
        this.time += new Date().getFullYear() + "-" + (new Date().getMonth() + 1) + "-" + new Date().getDate()
    },
    mounted(){
        this.$axios.get('manager/', {})
        .then(res => {
            console.log(res.data);
        })
    }
}
</script>