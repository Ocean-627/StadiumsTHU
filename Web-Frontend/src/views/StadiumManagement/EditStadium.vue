<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>场馆信息编辑</h2>
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
                            <strong>场馆信息编辑</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <!-- TODO: 在路由里添加参数，控制是到哪一个场馆的编辑页面 -->
                <div class="row">
                    <div class="col-lg-12">
                        <div class="tabs-container">
                            <ul class="nav nav-tabs">
                                <li><a class="nav-link active" data-toggle="tab" href="#tab-1"> 基本信息</a></li>
                                <li><a class="nav-link" data-toggle="tab" href="#tab-2"> 场馆图片</a></li>
                                <li><a class="nav-link" data-toggle="tab" href="#tab-3"> 预约选项</a></li>
                                <li><a class="nav-link" data-toggle="tab" href="#tab-4"> 地理位置</a></li>
                            </ul>
                            <div class="tab-content">
                                <div id="tab-1" class="tab-pane active">
                                    <div class="panel-body">
                                        <fieldset>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">场馆名称：</label>
                                                <div class="col-sm-10"><input type="text" class="form-control"></div>
                                            </div>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">开放状态：</label>
                                                <div class="col-sm-10"><select data-placeholder="..." class="chosen-select" tabindex="2">
                                                    <option>开放</option>
                                                    <option>未开放</option>
                                                </select></div>
                                            </div>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">联系方式：</label>
                                                <div class="col-sm-10"><input type="text" class="form-control" placeholder="..."></div>
                                            </div>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">场馆说明:</label>
                                                <div class="col-sm-10">
                                                    <textarea class="form-control" placeholder="输入场馆说明..." style="height: 100px;"></textarea>
                                                </div>
                                            </div>
                                        </fieldset>
                                    </div>
                                </div>
                                <div id="tab-2" class="tab-pane">
                                    <div class="panel-body">
                                        <fieldset>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">场馆封面：</label>
                                                <div class="col-sm-10"><img alt="image" class="rounded m-t-xs img-fluid" src="/static/img/zongti.jpg"></div>
                                            </div>
                                            <div class="form-group row"><label class="col-sm-8 col-form-label"></label>
                                                <div class="col-sm-4">
                                                    <div class="fileinput fileinput-new" data-provides="fileinput">
                                                        <span class="btn btn-default btn-file"><span class="fileinput-new">选择文件</span><span class="fileinput-exists">Change</span><input type="file" name="..."></span>
                                                        <span class="fileinput-filename"></span>
                                                        <a href="#" class="close fileinput-exists" data-dismiss="fileinput" style="float: none;">&times;</a>
                                                    </div>
                                                </div>
                                            </div>
                                        </fieldset>
                                    </div>
                                </div>
                                <div id="tab-3" class="tab-pane">
                                    <div class="panel-body">
                                        <fieldset>
                                            <div class="form-group row"><label class="col-sm-2 col-form-label">开放时间：</label>
                                                
                                            </div>
                                        </fieldset>
                                    </div>
                                </div>
                                <div id="tab-4" class="tab-pane">
                                    <div class="panel-body">
                                        <fieldset>
                                            <!-- 预计接入百度地图API -->
                                        </fieldset>
                                    </div>
                                </div>
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
@import '../../assets/css/plugins/jasny/jasny-bootstrap.min.css';
</style>

<script>
import Navbar from "@/components/Navbar"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Toolbox from "@/components/Toolbox"
import $ from 'jquery'
import '@/assets/js/plugins/chosen/chosen.jquery.js'
import '@/assets/js/plugins/jasny/jasny-bootstrap.min.js'
export default {
    data() {
        return {}
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    mounted() {
        $('.chosen-select').chosen({ width: "100%" })
    },
    methods: {
        fileSelected(e){
            var filename = e.target.files
            $(this).next('.custom-file-label').addClass("selected").html(fileName)
        }
    }
}

</script>