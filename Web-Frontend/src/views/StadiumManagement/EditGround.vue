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
                    <a href="/stadium_management/stadium_info/new_stadium" class="btn btn-outline btn-primary i-newstadium">
                        <i class="fa fa-plus"></i> 添加新场馆 
                    </a>
                </div>
                <div class="grid">
                    <div class="grid-item" v-for="(ground, index) in grounds" v-bind:key="ground.name">
                        <div class="contact-box">
                            <!-- 主要部分 & 单个单元 -->
                            <div class="panel-body">
                                <fieldset>
                                    <div class="form-group row"><label class="col-sm-4 col-form-label">场馆名称：</label>
                                        <div class="col-sm-8"><input type="text" class="form-control"></div>
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

<style>
@import '../../assets/css/plugins/chosen/bootstrap-chosen.css';
@import '../../assets/css/plugins/jasny/jasny-bootstrap.min.css';
@import '../../assets/css/plugins/clockpicker/clockpicker.css';
</style>

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
import '@/assets/js/plugins/clockpicker/clockpicker.js'
import '@/assets/js/plugins/chosen/chosen.jquery.js'
import '@/assets/js/plugins/jasny/jasny-bootstrap.min.js'
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
        })
        $('.chosen-select').chosen({ width: "100%" })
        var clocks = document.getElementsByClassName('clockpicker')
        for(var i = 0; i < clocks.length; i++){
            $(clocks[i]).clockpicker()
        }
    },
    methods: {

    }
}

</script>