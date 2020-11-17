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
                            <a href="index.html">主页</a>
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
            <div class="row  border-bottom white-bg dashboard-header">
                <div class="col-md-3">
                    <!--主要部分-->
                    
                </div>
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
export default {
    data() {
        return {}
    },
    components: {
        Toolbox, Navbar, Header, Footer
    }
}

</script>
