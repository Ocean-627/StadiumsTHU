<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>操作记录 </h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>操作记录</strong>
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
                            return this.$axios.get(`history/`, {params: queryParams}).then(res => console.log(res.data))
                        },
                    }
                },
                columns: [
                    { type: 'checkbox', width: 50 },
                    { type: 'seq', width: 60 },
                    { 
                        field: 'name', 
                        title: '操作者',
                        sortable: true,
                        slots: {
                            default: ({row}, h) => {
                                return [
                                    h('u', {
                                        style: {
                                            color: '#007bff',
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
                    { 
                        field: 'type', 
                        title: '操作类型',
                        filters: [
                            { label: '第一种', value: 1 },
                            { label: '第二种', value: 2 },
                            { label: '第三种', value: 3 },
                            { label: '第四种', value: 4 },
                        ],
                        formatter: function(value) {
                            switch(value){
                                case 1: return '第一种';
                                case 2: return '第二种';
                                case 3: return '第三种';
                                case 4: return '第四种';
                            }
                        }
                    },
                    { field: 'detail', title: '操作详情' },
                    { field: 'comment', title: '备注' },
                    { 
                        field: 'time', 
                        sortable: true, 
                        title: '操作时间', 
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
