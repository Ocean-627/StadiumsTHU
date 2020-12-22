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
                                sort: (sort.order === "desc") ? ("-" + sort.property) : sort.property,
                                page: page.currentPage,
                                size: page.pageSize
                            }, form)
                            filters.forEach(({ property, values }) => {
                                queryParams[property] = values.join(',')
                            })
                            return this.$axios.get(`history/`, {params: queryParams}).then(res => res.data)
                        },
                    }
                },
                columns: [
                    { type: 'checkbox', width: 50 },
                    { type: 'seq', width: 60 },
                    { 
                        field: 'type', 
                        title: '操作类型',
                        filters: [
                            { label: "添加场馆", value: "添加场馆" },
                            { label: "编辑场馆信息", value: "编辑场馆信息" },
                            { label: "移入黑名单", value: "移入黑名单" },
                            { label: "移除黑名单", value: "移除黑名单" },
                            { label: "撤销信用记录", value: "撤销信用记录" },
                            { label: "场馆预留", value: "场馆预留" },
                            { label: "修改场馆预约时段", value: "修改场馆预约时段" },
                        ]
                    },
                    { field: 'details', title: '操作详情' },
                    { field: 'content', title: '备注' },
                    { 
                        field: 'state', 
                        title: '状态', 
                        slots: {
                            default: ({row}, h) => {
                                var content, color
                                if(row.state == 0) {
                                    content = "成功";
                                    color = "#28a745"
                                }
                                if(row.state == 1) {
                                    content = "已取消";
                                    color = "#6c757d"
                                }
                                if(row.state == 2) {
                                    content = "已过期";
                                }
                                return [
                                    h('div', {
                                        style: {
                                            color: color,
                                            cursor: 'pointer'
                                        }
                                    }, content)
                                ]
                            }
                        }
                    },
                    {
                        field: 'op',
                        title: '操作',
                        slots: {
                            default: ({row}, h) => {
                                if(row.state != 0) return []
                                if(row.type === "添加场馆"
                                || row.type === "编辑场馆信息"
                                || row.type === "移除黑名单"
                                || row.type === "撤销信用记录") return []
                                let func = (res) => {
                                    if(!res) return;
                                    let req = {}
                                    if(row.type === "添加黑名单"){
                                        req.url = 'blacklist/';
                                        req.method = 'put';
                                        req.data = {
                                            id: row.id
                                        }
                                    }
                                    else if(row.type === "场馆预留"){
                                        req.url = 'addevent/';
                                        req.method = 'put';
                                        req.data = {
                                            id: row.id
                                        }
                                    }
                                    else if(row.type === "修改场馆预定时段"){
                                        req.url = 'changeduration/';
                                        req.method = 'put';
                                        req.data = {
                                            id: row.id
                                        }
                                    }
                                    this.$axios(req).then(res => {
                                        swal("成功", "撤销操作成功", "success");
                                        refreshColumn();
                                    })
                                }
                                return [
                                    h('button', {
                                        class: "btn btn-sm btn-outline btn-danger",
                                        on: {
                                            click: () => {
                                                swal({
                                                    title: "确定要撤销这条操作吗？",
                                                    type: "warning",
                                                    showCancelButton: true,
                                                    confirmButtonColor: "#DD6B55",
                                                    confirmButtonText: "确认",
                                                    cancelButtonText: "取消",
                                                },
                                                func)
                                            }
                                        }
                                    }, "撤销")
                                ]
                            }
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
