<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>用户反馈 </h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            场馆管理
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>用户反馈</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <vxe-grid v-bind="gridOptions" class="white-bg" style="padding: 15px;"></vxe-grid>
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
import moment from "moment"

export default {
    data() {
        return {
            gridOptions: {
                border: true,
                resizable: true,
                showHeaderOverflow: true,
                showOverflow: true,
                highlightHoverRow: true,
                keepSource: true,
                height: 850,
                rowId: 'id',
                sortConfig: {
                    trigger: 'cell'
                },
                filterConfig: {
                    remote: true
                },
                pagerConfig: {
                    pageSize: 10,
                    pageSizes: [5, 10, 15, 20, 50, 100, 200, 500]
                },
                sortConfig: {
                    remote: true,
                    trigger: 'cell'
                },
                formConfig: {
                    titleWidth: 100,
                    titleAlign: 'right',
                    items: [
                        { 
                            field: 'name',
                            title: '姓名', 
                            span: 6, 
                            itemRender: { name: '$input', props: { placeholder: '请输入姓名' } } 
                        },
                        { 
                            field: 'nickName', 
                            title: '昵称', 
                            span: 6, 
                            itemRender: { name: '$input', props: { placeholder: '请输入昵称' } } 
                        },
                        { 
                            field: 'userId',
                            title: '学号/工号', 
                            span: 6, 
                            itemRender: { name: '$input', props: { placeholder: '请输入学号/工号' } } 
                        },
                        {
                            field: 'type',
                            title: '用户类型', 
                            span: 6, 
                            itemRender: { 
                                name: '$select', 
                                options: [
                                    { label: '在校学生', value: '在校学生' },
                                    { label: '教工', value: '教工' }
                                ]
                            } 
                        },
                        { 
                            field: 'email', 
                            title: '邮箱', 
                            span: 6, 
                            folding: true,
                            itemRender: { name: '$input', props: { placeholder: '请输入邮箱' } } 
                        },
                        { 
                            field: 'phone', 
                            title: '手机', 
                            span: 6, 
                            folding: true,
                            itemRender: { name: '$input', props: { placeholder: '请输入手机号' } } 
                        },
                        { 
                            field: 'auth', 
                            title: '是否认证', 
                            span: 6, 
                            folding: true, 
                            itemRender: { 
                                name: '$select', 
                                options: [
                                    { label: '已认证', value: true },
                                    { label: '未认证', value: false }
                                ]
                            } 
                        },
                        { 
                            span: 24, 
                            align: 'center', 
                            collapseNode: true, 
                            itemRender: { 
                                name: '$buttons', 
                                children: [
                                    { props: { type: 'submit', content: '查询', status: 'primary' } }, 
                                    { props: { type: 'reset', content: '重置' } }
                                ] 
                            } 
                        }
                    ]
                },
                toolbarConfig: {
                    buttons: [
                        { code: 'delete', name: '删除', icon: 'fa fa-trash-o', status: 'danger' },
                    ],
                    refresh: true,
                    export: true,
                    print: true,
                    custom: true
                },
                proxyConfig: {
                    seq: true,
                    sort: true, // 启用排序代理
                    filter: true, // 启用筛选代理
                    form: true, // 启用表单代理
                    props: {
                        result: 'results',
                        total: 'count'
                    },
                    ajax: {
                        query: ({ page, sort, filters, form  }) => {
                            const queryParams = Object.assign({
                                sort: (sort.order === "desc") ? ("-" + sort.property) : sort.property,
                                page: page.currentPage,
                                size: page.pageSize
                            }, form)
                            filters.forEach(({ property, values }) => {
                                queryParams[property] = values.join(',')
                            })
                            return this.$axios.get(`/user/`, {params: queryParams}).then(res => res.data)
                        },
                        delete: ({ body }) => {
                            console.log(body)
                        }
                    }
                },
                columns: [
                    { type: 'checkbox', width: 50 },
                    { type: 'seq', width: 60 },
                    { 
                        field: 'name', 
                        title: '姓名',
                        sortable: true,
                        slots: {
                            default: ({row}, h) => {
                                return [
                                    h('u', {
                                        style: {
                                            color: 'blue',
                                            cursor: 'pointer'
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
                    { field: 'nickName', sortable: true, title: '昵称' },
                    { field: 'userId', sortable: true, title: '学号/工号' },
                    { field: 'type', sortable: true, title: '用户类型' },
                    { field: 'email', sortable: true, title: '邮箱', visible: false },
                    { field: 'phone', sortable: true, title: '手机'},
                    { 
                        field: 'auth', 
                        title: '是否认证', 
                        filters: [
                            { label: '已认证', value: true },
                            { label: '未认证', value: false }
                        ],
                        formatter: function(value){
                            if(value === "true") return "已认证"
                            return "未认证"
                        }
                    },
                    { 
                        field: 'loginTime', 
                        sortable: true, 
                        title: '最近登陆时间', 
                        visible: false,
                        formatter: function(value) {
                            return moment(value).format("YYYY-MM-DD HH:mm:ss");
                        }
                    }
                ],
                exportConfig: {},
                printConfig: {},
                checkboxConfig: {
                    reserve: true,
                    highlight: true,
                    range: true
                },
            }
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    methods: {

    }
}

</script>
