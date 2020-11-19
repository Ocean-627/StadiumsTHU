<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>场地信息编辑 <small>@综合体育馆</small></h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            场馆管理
                        </li>
                        <li class="breadcrumb-item">
                            <a href="/stadium_management/stadium_info">场馆信息管理</a>
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>场地信息编辑</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <!-- TODO: 在路由里添加参数，控制是到哪一个场馆的编辑页面 -->
                <div class="row i-row">
                    <a href="/stadium_management/stadium_info/new_stadium" class="btn btn-outline btn-primary i-button">
                        <i class="fa fa-plus"></i> 添加新场馆 
                    </a>
                    <a href="/stadium_management/stadium_info/new_stadium" class="btn btn-outline btn-default i-button">
                        <i class="fa fa-check"></i> 完成 
                    </a>
                    <a href="/stadium_management/stadium_info/new_stadium" class="btn btn-outline btn-default i-button">
                        <i class="fa fa-mail-reply"></i> 返回 
                    </a>
                </div>
                <div class="grid">
                    <div class="grid-item" v-for="(ground, index) in grounds" v-bind:key="ground.name">
                        <div class="contact-box">
                            <!-- 主要部分 & 单个单元 -->
                            <div class="row i-row">
                                <div class="col-md-7">
                                    <img alt="image" class="rounded m-t-xs img-fluid i-img" src="/static/img/zongti.jpg">
                                </div>
                                <div class="col-md-5 i-infobox">
                                    <h2 class="i-title"><strong>综合体育馆</strong></h2>
                                    <i class="fa fa-comment-o i-icon"></i>1224 条评论 <br>
                                    <i class="fa fa-clock-o i-icon"></i> 开放时间：8:00 - 18:00<br>
                                    <i class="fa fa-location-arrow i-icon"></i> 新民路<br>
                                    <div class="i-score">
                                        <i class="fa fa-star i-star"></i>
                                        <i class="fa fa-star i-star"></i>
                                        <i class="fa fa-star i-star"></i>
                                        <i class="fa fa-star i-star"></i>
                                        <i class="fa fa-star i-star i-icon"></i>
                                        5
                                    </div>
                                </div>
                            </div>
                            <div class="row i-row i-groundinfo">
                                <div class="col-md-12">
                                    开放场地：羽毛球场 8 个、乒乓球场 8 个
                                </div>
                            </div>
                            <div class="contact-box-footer">
                                <button type="button" class="btn btn-outline btn-danger" v-on:click="deleteGround(index)">
                                    <i class="fa fa-trash"></i> 删除场地 
                                </button>
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

<style scoped>
.i-row [class^="col-"] {
    padding: 10px;
}
.i-row {
    margin: 0;
}
.contact-box {
    max-width: 500px;
    padding: 15px;
}
.i-button {
    margin-bottom: 20px;
    margin-right: 10px;
}
.i-title {
    margin-top: 10px;
    font-weight: bolder;
    text-align: center;
}
.i-infobox {
    line-height: 30px;
    font-size: 13px;
    font-weight: bold;
}
.i-star {
    color: orange;
}
.i-icon {
    margin-right: 10px;
}
.i-groundinfo {
    border-top: 1px solid #e7eaec;
    font-weight: bold;
}
</style>

<script>
import Navbar from "@/components/Navbar"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Toolbox from "@/components/Toolbox"
import 'jquery'
import 'masonry-layout'
export default {
    data() {
        return {
            grounds: [
                {
                    name: "羽毛球场",
                    count: 8
                },
                {
                    name: "乒乓球场",
                    count: 8
                }
            ]
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    mounted() {
        var msnry = new Masonry('.grid', {
            // options...
            itemSelector: ".grid-item",
            columnWidth: 500,
            gutter: 25
        });
    },
    methods: {
        deleteGround(index) {
            swal({
                title: "你确定？",
                text: "删除场地将同时删除所有的该场地预定记录！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: false 
            },
            () => {
                // TODO: 删除场地
                swal("成功", "场地已成功删除", "success")
            });
        }
    }
}

</script>