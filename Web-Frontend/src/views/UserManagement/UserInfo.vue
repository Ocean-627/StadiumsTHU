<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>用户信息 </h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            用户管理
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>用户信息</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <vxe-grid
                    border
                    resizable
                    height="530"
                    row-id="id"
                    :pager-config="{pageSize: 10}"
                    :proxy-config="tableProxy"
                    :checkbox-config="{reserve: true}"
                    :columns="tableColumn"></vxe-grid>
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
        return {
            tableProxy: {
                seq: true, // 启用动态序号代理
                props: {
                  result: 'result',
                  total: 'page.total'
                },
                ajax: {
                  // 任何支持 Promise API 的库都可以对接（fetch、jquery、axios、xe-ajax）
                  query: ({ page }) => this.$axios.get(`https://xuliangzhan_admin.gitee.io/api/user/page/list/${page.pageSize}/${page.currentPage}`)
                }
            },
            tableColumn: [
                { type: 'checkbox', width: 50 },
                { type: 'seq', width: 60 },
                { field: 'name', title: 'Name' },
                { field: 'nickname', title: 'Nickname' },
                { field: 'role', title: 'Role' },
                { field: 'describe', title: 'Describe', showOverflow: true }
            ]
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    mounted() {

    }
}

</script>
