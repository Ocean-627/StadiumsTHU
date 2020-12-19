<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row wrapper border-bottom white-bg page-heading">
                <!--Breadcrum 导航-->
                <div class="col-lg-9">
                    <h2>预约记录 </h2>
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            场馆管理
                        </li>
                        <li class="breadcrumb-item">
                            <a href="/stadium_management/stadium_info">场馆列表</a>
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>预约记录</strong>
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
                    pageSize: 15,
                    pageSizes: [5, 10, 15, 20, 50, 100, 200, 500]
                },
                sortConfig: {
                    remote: true,
                    trigger: 'cell'
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
                            const queryParams = Object.assign({
                                stadium: this.$route.params.id,
                                sort: (sort.order === "desc") ? ("-" + sort.property) : sort.property,
                                page: page.currentPage,
                                size: page.pageSize
                            }, form)
                            filters.forEach(({ property, values }) => {
                                if(property === 'status'){
                                    console.log(values)
                                    if(values[0] === 'payed'){
                                        queryParams['payment'] = false;
                                        queryParams['cancel'] = false;
                                    }
                                    else if(values[0] === 'available'){
                                        queryParams['payment'] = true;
                                        queryParams['checked'] = false;
                                        queryParams['cancel'] = false;
                                    }
                                    else if(values[0] === 'using'){
                                        queryParams['checked'] = true;
                                        queryParams['leave'] = false;
                                        queryParams['cancel'] = false;
                                    }
                                    else if(values[0] === 'used'){
                                        queryParams['leave'] = true;
                                        queryParams['cancel'] = false;
                                    }
                                    else if(values[0] === 'canceled'){
                                        queryParams['cancel'] = true;
                                    }
                                }
                                else{
                                    queryParams[property] = values.join(',')
                                }
                            })
                            return this.$axios.get(`reserveevent/`, {params: queryParams}).then(res => res.data)
                        },
                    }
                },
                columns: [
                    { type: 'checkbox', width: 50 },
                    { type: 'seq', width: 60 },
                    { 
                        field: 'userName', 
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
                    { field: 'court', title: '场地' },
                    { 
                        field: 'duration', 
                        title: '时间',
                        formatter: function({cellValue, row, column}) {
                            return row.date + " " + row.startTime + "-" + row.endTime
                        }
                    },
                    { field: 'price', title: '预约金额'},
                    { 
                        field: 'status', 
                        title: '状态', 
                        filters: [
                            { label: '未付款', value: 'payed' },
                            { label: '未使用', value: 'available' },
                            { label: '使用中', value: 'using' },
                            { label: '已结束', value: 'used' },
                            { label: '已取消', value: 'canceled' },
                        ],
                        filterMultiple: false,
                        formatter: function({cellValue, row, column}){
                            if(row.cancel) return "已取消";
                            if(!row.payment) return "未付款";
                            if(row.leave) return "已结束";
                            if(row.checked && !row.leave) return "使用中";
                            return "未使用";
                        },
                        slots: {
                            default: ({ row }, h) => {
                                let content = "未使用", style = "#28a745";
                                if(row.cancel) {
                                    content = "已取消";
                                    style = "orange";
                                }
                                if(!row.payment) {
                                    content = "未付款";
                                    style = "#dc3545";
                                }
                                if(row.leave) {
                                    content = "已结束";
                                    style = "#6c757d";
                                }
                                if(row.checked && !row.leave) {
                                    content = "使用中";
                                    style = "#17a2b8";
                                }
                                return [
                                    h('span', {
                                        style: {
                                            color: style
                                        }
                                    }, content)
                                ]
                            }
                        },
                    },
                    { 
                        field: 'createTime', 
                        sortable: true, 
                        title: '预订时间', 
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
