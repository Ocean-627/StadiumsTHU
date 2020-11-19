<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>场馆信息管理</h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            场馆管理
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>场馆信息管理</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="row i-row">
                    <a href="/stadium_management/stadium_info/new_stadium" class="btn btn-outline btn-primary i-newstadium">
                        <i class="fa fa-plus"></i> 添加新场馆 
                    </a>
                </div>
                <div class="grid">
                    <div class="grid-item" v-for="(stadium, index) in stadiums" v-bind:key="stadium.name">
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
                                <button type="button" class="btn btn-outline btn-default" v-on:click="editStadium(index)">
                                    <i class="fa fa-edit"></i> 编辑场馆信息 
                                </button>
                                <button type="button" class="btn btn-outline btn-default" v-on:click="editGround(index)">
                                    <i class="fa fa-clock-o"></i> 修改预定时间段 
                                </button>
                                <button type="button" class="btn btn-outline btn-danger" v-on:click="deleteStadium(index)">
                                    <i class="fa fa-trash"></i> 移除场馆 
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
.i-newstadium {
    margin-bottom: 20px;
    float: right;
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
            stadiums: [
                {
                    name: '综合体育馆'
                },
                {
                    name: '综合体育馆2'
                },
                {
                    name: '综合体育馆3'
                },
                {
                    name: '综合体育馆4'
                },
                {
                    name: '综合体育馆5'
                },
                {
                    name: '综合体育馆9'
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
        editStadium(index) {
            this.$router.push('/stadium_management/stadium_info/edit_stadium')
        },
        editGround(index) {
            this.$router.push('/stadium_management/stadium_info/edit_ground')
        },
        deleteStadium(index) {
            swal({
                title: "你确定？",
                text: "删除场馆将删除附带的场地信息和所有的预定记录！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                closeOnConfirm: false 
            },
            () => {
                // TODO: 删除场馆
                swal("成功", "场馆已成功删除", "success")
            });
        }
    }
}

</script>
