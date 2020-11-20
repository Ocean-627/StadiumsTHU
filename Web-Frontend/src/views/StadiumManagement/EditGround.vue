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
                            <div class="panel-body">
                                <fieldset>
                                    <div class="form-group row"><label class="col-sm-4 col-form-label">场地类型：</label>
                                        <div class="col-sm-8"><input type="text" class="form-control"></div>
                                    </div>
                                    <div class="form-group row"><label class="col-sm-4 col-form-label">开放状态：</label>
                                        <div class="col-sm-8"><select data-placeholder="..." class="chosen-select" tabindex="2">
                                            <option>开放</option>
                                            <option>未开放</option>
                                        </select></div>
                                    </div>
                                    <div class="form-group row"><label class="col-sm-4 col-form-label">场地数量：</label>
                                        <div class="col-sm-5"><input class="touchspin" type="text" v-model="ground.count"></div>
                                    </div>
                                </fieldset>
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
@import '../../assets/css/plugins/touchspin/jquery.bootstrap-touchspin.min.css';
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
.chosen-container-single .chosen-single {
    padding: 4px 12px;
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
import '@/assets/js/plugins/touchspin/jquery.bootstrap-touchspin.min.js'
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
        $(".touchspin").TouchSpin();
        var clocks = document.getElementsByClassName('clockpicker')
        for(var i = 0; i < clocks.length; i++){
            $(clocks[i]).clockpicker()
        }
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