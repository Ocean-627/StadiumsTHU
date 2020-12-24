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
            name2id: {},
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
                            field: 'stadiumName', 
                            title: '场馆名称', 
                            span: 6, 
                            itemRender: { name: '$input', props: { placeholder: '请输入场馆名称' } } 
                        },
                        {
                            field: 'content',
                            title: '评论内容', 
                            span: 8, 
                            itemRender: { name: '$input', props: { placeholder: '请输入评论内容' } } 
                        },
                        { 
                            span: 4, 
                            align: 'right', 
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
                            form.stadium_id = this.name2id[form.stadiumName];
                            const queryParams = Object.assign({
                                sort: (sort.order === "desc") ? ("-" + sort.property) : sort.property,
                                page: page.currentPage,
                                size: page.pageSize
                            }, form)
                            filters.forEach(({ property, values }) => {
                                queryParams[property] = values.join(',')
                            })
                            return this.$axios.get(`comment/`, {params: queryParams}).then(res => res.data)
                        },
                    }
                },
                columns: [
                    { type: 'checkbox', width: 50 },
                    { type: 'seq', width: 60 },
                    { 
                        field: 'user', 
                        title: '姓名',
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
                                                window.location.replace('/user_management/detail/' + row.user.toString())
                                            }
                                        }
                                    }, row.userName)
                                ]
                            }
                        }
                    },
                    { 
                        field: 'stadium_id', 
                        title: '使用场馆',
                        formatter: (cell) => {
                            return cell.row.stadiumName
                        }
                    },
                    { field: 'courtName', title: '使用场地' },
                    { field: 'content', title: '评论内容' },
                    { 
                        field: 'score', 
                        title: '评分',
                        filters: [
                            { label: '1', value: 1 },
                            { label: '2', value: 2 },
                            { label: '3', value: 3 },
                            { label: '4', value: 4 },
                            { label: '5', value: 5 },
                        ],
                        filterMultiple: false
                    },
                    { 
                        field: 'createTime', 
                        title: '评论时间', 
                        visible: false,
                        formatter: function(value) {
                            return moment(value.cellValue).format("YYYY-MM-DD HH:mm:ss");
                        }
                    },
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
        
    },
    beforeCreate() {
        this.$axios.get("stadium/").then(res => {
            for(let s of res.data) {
                this.name2id[s.name] = s.id
            }
        })
    }
}

</script>
