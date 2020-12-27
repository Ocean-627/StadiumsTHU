<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>系统日志 </h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>系统日志</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <ul class="list-group">
                    <li class="list-group-item white-bg">
                        <h3>清动家园 v1.0.0 正式发布<small style="float: right;">2020/12/24</small></h3>
                        清动家园小程序、清动家园管理系统正式上线了！<br>
                        详情请见<a href="/static/doc.pdf">开发文档</a>。
                    </li>
                </ul>
            </div>
            <Footer></Footer>
        </div>
        <Toolbox></Toolbox>
    </div>
</template>

<style scoped>

</style>

<script>
import Navbar from "@/components/Navbar"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Toolbox from "@/components/Toolbox"
import "@/assets/js/jquery-3.1.1.min.js";
export default {
    data() {
        return {
            
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    methods: {

    },
    mounted() {
    
    }
}

</script>
