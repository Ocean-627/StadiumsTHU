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
                    height="700"
                    row-id="id"
                    :export-config="{}"
                    :pager-config="{pageSize: 10}"
                    :proxy-config="tableProxy"
                    :toolbar-config="tableToolbar"
                    :columns="tableColumn">
                </vxe-grid>
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
                seq: true,
                props: {
                    result: 'results',
                    total: 'count'
                },
                ajax: {
                    query: ({ page }) => this.$axios.get(`/user/?page=${page.currentPage}&size=${page.pageSize}`).then(res => res.data)
                }
            },
            tableColumn: [
                { type: 'checkbox', width: 50 },
                { type: 'seq', width: 60 },
                { 
                    field: 'name', 
                    title: '姓名',
                    slots: {
                        default: ({row}, h) => {
                            return [
                                h('span', {
                                    style: {
                                        color: 'blue'
                                    },
                                    on: {
                                        click: () => {
                                            window.location.replace('/user_management/user_info/detail/' + row.userId.toString())
                                        }
                                    }
                                }, row.name)
                            ]
                        }
                    }
                },
                { field: 'nickName', title: '昵称' },
                { field: 'userId', title: '学号/工号' },
                { field: 'email', title: '邮箱'},
                { field: 'phone', title: '手机'},
                { 
                    field: 'auth', 
                    title: '是否认证', 
                    formatter: function(value){
                        if(value) return "已认证"
                        return "未认证"
                    }
                }
            ],
            tableToolbar: {
                export: true,
                custom: true
            },
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    methods: {

    }
}

</script>
