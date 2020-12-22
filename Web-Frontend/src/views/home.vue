<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row border-bottom white-bg dashboard-header">
                <div class="col-md-3">
                    <h2>欢迎您，{{ this.username }}</h2>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight ecommerce">
                <div class="row" style="margin-bottom: 20px" v-show="loaded">
                    <div class="col-lg-5">
                        <el-select v-model="cur_stadium" id="stadium" @change="updateChart()">
                            <el-option v-for="s in stadiums" :key="s.id" :value="s.id" :label="s.name" />
                        </el-select>
                        <el-select v-model="cur_courttype" id="courttype" @change="updateChart()">
                            <el-option v-for="c in courttypes" :key="c" :value="c" />
                        </el-select>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-6">
                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>过去七天预约次数</h5>
                            </div>
                            <div class="ibox-content" v-if="loaded">
                                <Chart id="chart1" :chartdata="this.chartdata" :options="this.options" />
                            </div>
                            <div class="spiner-example" v-if="!loaded">
                                <div class="sk-spinner sk-spinner-circle">
                                    <div class="sk-circle1 sk-circle"></div>
                                    <div class="sk-circle2 sk-circle"></div>
                                    <div class="sk-circle3 sk-circle"></div>
                                    <div class="sk-circle4 sk-circle"></div>
                                    <div class="sk-circle5 sk-circle"></div>
                                    <div class="sk-circle6 sk-circle"></div>
                                    <div class="sk-circle7 sk-circle"></div>
                                    <div class="sk-circle8 sk-circle"></div>
                                    <div class="sk-circle9 sk-circle"></div>
                                    <div class="sk-circle10 sk-circle"></div>
                                    <div class="sk-circle11 sk-circle"></div>
                                    <div class="sk-circle12 sk-circle"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="ibox">
                            <div class="ibox-title">
                                <h5>过去七天预约比例</h5>
                            </div>
                            <div class="ibox-content" v-if="loaded">
                                <Chart id="chart2" :chartdata="this.chartdata2" :options="this.options2" />
                            </div>
                            <div class="spiner-example" v-if="!loaded">
                                <div class="sk-spinner sk-spinner-circle">
                                    <div class="sk-circle1 sk-circle"></div>
                                    <div class="sk-circle2 sk-circle"></div>
                                    <div class="sk-circle3 sk-circle"></div>
                                    <div class="sk-circle4 sk-circle"></div>
                                    <div class="sk-circle5 sk-circle"></div>
                                    <div class="sk-circle6 sk-circle"></div>
                                    <div class="sk-circle7 sk-circle"></div>
                                    <div class="sk-circle8 sk-circle"></div>
                                    <div class="sk-circle9 sk-circle"></div>
                                    <div class="sk-circle10 sk-circle"></div>
                                    <div class="sk-circle11 sk-circle"></div>
                                    <div class="sk-circle12 sk-circle"></div>
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

</style>

<script>
import Navbar from "@/components/Navbar"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Toolbox from "@/components/Toolbox"
import Chart from "@/components/Chart"

export default {
    data() {
        return {
            username: localStorage.getItem("username"),
            stadiums: [],
            courttypes: [],
            cur_stadium: 0,
            cur_courttype: "全部场地",
            loaded: false,
            chartdata: {
                labels: [],
                datasets: [{
                    label: '预约次数',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            },
            chartdata2: {
                labels: [],
                datasets: [{
                    label: '预约比例',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options2: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        }
    },
    components: {
        Toolbox, Navbar, Header, Footer, Chart
    },
    methods: {
        updateChart(){
            this.loaded = false;
            let queryParams = {
                stadium_id: (this.cur_stadium === 0) ? null : this.cur_stadium,
                type: (this.type === "全部场地") ? null : this.cur_courttype
            }
            this.$axios
                .get('statistics/', { params: queryParams })
                .then(res => {
                    // 读入数据
                    this.chartdata.datasets[0].data = []
                    this.chartdata2.datasets[0].data = []
                    for(let v in res.data){
                        let ratio = (res.data[v].availableDurations) ? (res.data[v].reservedDurations / res.data[v].availableDurations) : 0;
                        this.chartdata.datasets[0].data.push(res.data[v].reservedDurations || 0)
                        this.chartdata2.datasets[0].data.push(ratio)
                    }
                    this.loaded = true;
                })
        }
    },
    mounted() {
        let _this = this
        setTimeout(function () {
            toastr.options = {
                closeButton: true,
                progressBar: true,
                showMethod: 'slideDown',
                timeOut: 4000
            };
            toastr.success('清动家园管理者', '欢迎您 ' + _this.username);
        }, 1300);
        let p = Promise.all([
            this.$axios.get('statistics/'),
            this.$axios.get('stadium/'),
            this.$axios.get('courttype/'),
        ])
        p.then(res => {
            // 读入数据
            this.loaded = false;
            this.chartdata.labels = []
            this.chartdata.datasets[0].data = []
            this.chartdata2.labels = []
            this.chartdata2.datasets[0].data = []
            for(let v in res[0].data){
                this.chartdata.labels.push(v);
                this.chartdata2.labels.push(v);
                let ratio = (res[0].data[v].availableDurations) ? (res[0].data[v].reservedDurations / res[0].data[v].availableDurations) : 0;
                this.chartdata.datasets[0].data.push(res[0].data[v].reservedDurations || 0)
                this.chartdata2.datasets[0].data.push(ratio)
            }
            this.loaded = true;
            // 读入场馆
            this.stadiums = [{ id: 0, name: '全部场馆' }];
            for(let s of res[1].data){
                this.stadiums.push({ id: s.id, name: s.name })
            }
            // 读入场地
            this.courttypes = ['全部场地'];
            let buf = {}
            for(let c of res[2].data){
                if(!buf[c.type]){
                    buf[c.type] = 1
                    this.courttypes.push(c.type)
                }
            }
        })
    }
}

</script>
