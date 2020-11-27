<template>
    <div>
        <nav class="navbar-default navbar-static-side" role="navigation">
            <div class="sidebar-collapse">
                <ul class="nav metismenu" id="side-menu">
                    <li class="nav-header">
                        <div class="dropdown profile-element">
                            <img alt="image" class="rounded-circle" src="../../static/img/mabaoguo.jpg" />
                            <a data-toggle="dropdown" class="dropdown-toggle" href="#">
                                <span class="block m-t-xs font-bold">马保国</span>
                                <span class="text-muted text-xs block">管理员 <b class="caret"></b></span>
                            </a>
                            <ul class="dropdown-menu animated fadeInRight m-t-xs">
                                <li><a class="dropdown-item" href="profile.html">个人信息</a></li>
                                <li><a class="dropdown-item" href="mailbox.html">信箱</a></li>
                                <li class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/login">登出</a></li>
                            </ul>
                        </div>
                        <div class="logo-element">
                            清动
                        </div>
                    </li>
                    <li>
                        <a href="/home"><i class="fa fa-home"></i> <span class="nav-label">首页</span></a>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-th-large"></i> <span class="nav-label">场馆管理</span> <span
                                class="fa arrow"></span></a>
                        <ul class="nav nav-second-level">
                            <li><a href="/stadium_management/stadium_info">场馆信息管理</a></li>
                            <li><a href="/stadium_management/user_feedback">用户反馈处理</a></li>
                            <li><a href="/stadium_management/ground_reserve">场地预留</a></li>
                            <li><a href="/stadium_management/reserve_record">预订记录</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#"><i class="fa fa-group"></i> <span class="nav-label">用户管理</span><span
                                class="fa arrow"></span></a>
                        <ul class="nav nav-second-level collapse">
                            <li><a href="/user_management/user_info">用户信息</a></li>
                            <li><a href="/user_management/black_list">黑名单管理</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="/operation_record"><i class="fa fa-check-square-o"></i> <span class="nav-label">操作记录</span></a>
                    </li>
                    <li>
                        <a href="/statistic"><i class="fa fa-bar-chart-o"></i> <span class="nav-label">统计分析</span></a>
                    </li>
                    <li>
                        <a href="/system_log"><i class="fa fa-info"></i> <span class="nav-label">系统日志</span>
                            <span class="label label-info float-right">新</span></a>
                    </li>
                </ul>
            </div>
        </nav>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    }
}
</script>