<template>
    <div id="wrapper">
        <nav class="navbar-default navbar-static-side" role="navigation">
            <div class="sidebar-collapse">
                <ul class="nav metismenu" id="side-menu">
                    <li class="nav-header">
                        <div class="dropdown profile-element">
                            <img alt="image" class="rounded-circle" src="img/profile_small.jpg" />
                            <a data-toggle="dropdown" class="dropdown-toggle" href="#">
                                <span class="block m-t-xs font-bold">马保国</span>
                                <span class="text-muted text-xs block">管理员 <b class="caret"></b></span>
                            </a>
                            <ul class="dropdown-menu animated fadeInRight m-t-xs">
                                <li><a class="dropdown-item" href="profile.html">个人信息</a></li>
                                <li><a class="dropdown-item" href="mailbox.html">信箱</a></li>
                                <li class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="login.html">登出</a></li>
                            </ul>
                        </div>
                        <div class="logo-element">
                            清动
                        </div>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-home"></i> <span class="nav-label">首页</span></a>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-th-large"></i> <span class="nav-label">场馆管理</span> <span
                                class="fa arrow"></span></a>
                        <ul class="nav nav-second-level">
                            <li><a href="#">场馆信息管理</a></li>
                            <li><a href="#">用户反馈处理</a></li>
                            <li><a href="#">场馆预留</a></li>
                            <li><a href="#">预订记录</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-group"></i> <span class="nav-label">用户管理</span><span
                                class="fa arrow"></span></a>
                        <ul class="nav nav-second-level collapse">
                            <li><a href="#">用户信息</a></li>
                            <li><a href="#">黑名单管理</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-check-square-o"></i> <span class="nav-label">操作记录</span></a>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-bar-chart-o"></i> <span class="nav-label">统计分析</span></a>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-info"></i> <span class="nav-label">系统日志</span><span
                                class="label label-info float-right">新</span></a>
                    </li>
                </ul>
            </div>
        </nav>
        <div id="page-wrapper" class="gray-bg dashbard-1">
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
                                            <img alt="image" class="rounded-circle" src="img/a7.jpg">
                                        </a>
                                        <div class="media-body">
                                            <small class="float-right">46 小时前</small>
                                            <strong>小明</strong> 评论了 <strong>小红</strong>. <br>
                                            <small class="text-muted">2017.10.06 7:58</small>
                                        </div>
                                    </div>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <div class="dropdown-messages-box">
                                        <a class="dropdown-item float-left" href="profile.html">
                                            <img alt="image" class="rounded-circle" src="img/a4.jpg">
                                        </a>
                                        <div class="media-body ">
                                            <small class="float-right text-navy">5 小时前</small>
                                            <strong>小红</strong> 打电话给了 <strong>小黑</strong>. <br>
                                            <small class="text-muted">2017.10.06 7:58</small>
                                        </div>
                                    </div>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <div class="dropdown-messages-box">
                                        <a class="dropdown-item float-left" href="profile.html">
                                            <img alt="image" class="rounded-circle" src="img/profile.jpg">
                                        </a>
                                        <div class="media-body ">
                                            <small class="float-right">23 小时前</small>
                                            <strong>小黑</strong> 点赞了 <strong>小红</strong>. <br>
                                            <small class="text-muted">2017.10.06 7:58</small>
                                        </div>
                                    </div>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <div class="text-center link-block">
                                        <a href="mailbox.html" class="dropdown-item">
                                            <i class="fa fa-envelope"></i> <strong>阅读所有消息</strong>
                                        </a>
                                    </div>
                                </li>
                            </ul>
                        </li>
                        <li class="dropdown">
                            <a class="dropdown-toggle count-info" data-toggle="dropdown" href="#">
                                <i class="fa fa-bell"></i> <span class="label label-primary">8</span>
                            </a>
                            <ul class="dropdown-menu dropdown-alerts">
                                <li>
                                    <a href="mailbox.html" class="dropdown-item">
                                        <div>
                                            <i class="fa fa-envelope fa-fw"></i> 你有16条消息
                                            <span class="float-right text-muted small">4 分钟前</span>
                                        </div>
                                    </a>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <a href="profile.html" class="dropdown-item">
                                        <div>
                                            <i class="fa fa-twitter fa-fw"></i> 3 个新的关注者
                                            <span class="float-right text-muted small">12 分钟前</span>
                                        </div>
                                    </a>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <a href="grid_options.html" class="dropdown-item">
                                        <div>
                                            <i class="fa fa-upload fa-fw"></i> 重启服务器
                                            <span class="float-right text-muted small">4 分钟前</span>
                                        </div>
                                    </a>
                                </li>
                                <li class="dropdown-divider"></li>
                                <li>
                                    <div class="text-center link-block">
                                        <a href="notifications.html" class="dropdown-item">
                                            <strong>查看所有信息</strong>
                                            <i class="fa fa-angle-right"></i>
                                        </a>
                                    </div>
                                </li>
                            </ul>
                        </li>
                        <li style="padding: 20px">
                            <span class="m-r-sm text-muted welcome-message">2020/11/16</span>
                        </li>
                        <li>
                            <a href="login.html">
                                <i class="fa fa-sign-out"></i> 注销
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
            <div class="row  border-bottom white-bg dashboard-header">
                <div class="col-md-3">
                    <h2>欢迎您，马保国</h2>
                    <small>您有42条消息和6条通知。</small>
                </div>
            </div>
            <div class="footer">
                <div>
                    <strong>Copyright</strong> THSS - Software Engineering Course @ 2020 Autumn
                </div>
            </div>
        </div>
        <Toolbox></Toolbox>
    </div>
</template>

<style scoped>

</style>

<script>

import Toolbox from "@/components/Toolbox"

export default {
    data() {
        return {}
    },
    components: {
        Toolbox
    }
}

</script>
