<template>
<div id="wrapper">
    <Navbar></Navbar>
    <div id="page-wrapper" class="gray-bg dashbard-1">
        <Header></Header>
        <div class="row wrapper border-bottom white-bg page-heading">
            <!--Breadcrum 导航-->
            <div class="col-lg-9">
                <h2>
                    场地预留 <small>@{{ stadiumName }}</small>
                </h2>
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="/home">主页</a>
                    </li>
                    <li class="breadcrumb-item">场馆管理</li>
                    <li class="breadcrumb-item">
                        <a href="/stadium_management/stadium_info">场馆列表</a>
                    </li>
                    <li class="breadcrumb-item active">
                        <strong>场地预留</strong>
                    </li>
                </ol>
            </div>
        </div>
        <div class="wrapper wrapper-content animated fadeInRight ecommerce">
            <div class="row" style="margin-bottom: 20px">
                <div class="col-lg-3">
                    <el-select v-model="current_date" id="date" @change="setDate(dates[current_date].label)">
                        <el-option v-for="date in dates" :key="date.value" :value="date.value" :label="date.label" />
                    </el-select>
                </div>
            </div>
            <div class="row" v-for="(ground, index) in grounds" :key="ground.type">
                <div class="col-lg-12">
                    <div class="ibox">
                        <div class="ibox-title">
                            <h5>{{ ground.type }}</h5>
                            <div class="ibox-tools">
                                <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                                    <i class="fa fa-tasks" style="color: green"></i>
                                </a>
                                <ul class="dropdown-menu dropdown-user">
                                    <li>
                                        <a class="dropdown-item" v-on:click="selectCourtType(index)" data-toggle="modal" :data-target="'#myModal'+index">场地预留</a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item" v-on:click="manage(ground)">预约管理</a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="ibox-content">
                            <div v-for="data in ground.courts" :key="data.id">
                                <h5>{{ data.name }}</h5>
                                <div class="progress">
                                    <div v-for="reserve in data.reservedDuration" :key="reserve.id" :class="reserve.type | progress_type" :style="0, reserve, data.reservedDuration | progress_length" role="progressbar" aria-valuemin="0" aria-valuemax="100" :title="reserve | progress_title">
                                    </div>
                                </div>
                                <div>
                                    <div v-for="reserve in data.reservedDuration" :key="reserve.id" :style="1, reserve, data.reservedDuration | progress_length">
                                        {{reserve.startTime}}
                                    </div>
                                </div>
                                <br />
                            </div>
                        </div>
                        <div class="modal inmodal" :id="'myModal'+index" tabindex="-1" role="dialog" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content animated fadeIn">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal">
                                            <span aria-hidden="true">&times;</span>
                                            <span class="sr-only">关闭</span></button>
                                        <br />
                                        <h4 class="modal-title">场地预留</h4>
                                    </div>
                                    <div class="modal-body">
                                        <p>
                                            场地类型：<strong>{{ ground.type }}</strong>
                                        </p>
                                        <div class="form-group" id="data_1">
                                            <label class="font-normal">使用日期</label>
                                            <div class="input-group date">
                                                <span class="input-group-addon"><i class="fa fa-calendar"></i></span>
                                                <input type="text" class="form-control" style="width:20px" ref="useDate" />
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label class="font-normal">使用时段</label>
                                            <div class="form-group row">
                                                <div class="col-sm-5">
                                                    <div class="input-group clockpicker" data-autoclose="true">
                                                        <input type="text" class="form-control" v-model="form_start" id="setEventDate" ref="startTime" />
                                                        <span class="input-group-addon">
                                                            <span class="fa fa-clock-o"></span>
                                                        </span>
                                                    </div>
                                                </div>
                                                <div class="col-sm-1 text-center" style="line-height: 35.5px">
                                                    至
                                                </div>
                                                <div class="col-sm-5">
                                                    <div class="input-group clockpicker" data-autoclose="true">
                                                        <input type="text" class="form-control" v-model="form_end" ref="endTime" />
                                                        <span class="input-group-addon">
                                                            <span class="fa fa-clock-o"></span>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label class="font-normal">使用者（选填）</label><br />
                                            <div>
                                                <small>请在下方输入使用者的学号/工号（或留空）。预约信息将通过站内消息通知他们。</small>
                                            </div>
                                            <input class="tagsinput form-control" type="text" ref="user_id" />
                                        </div>
                                        <div class="form-group">
                                            <label class="font-normal">预留场地数</label>
                                            <div class="row">
                                                <div class="col-sm-4">
                                                    <!--
                                                            <input class="touchspin" type="text" ref="number" />
                                                        -->
                                                    <input class="form-control" type="text" ref="number" @change="setNumber(index)" />
                                                </div>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label class="font-normal">预留场地（选填）</label><br />
                                            <div>
                                                <small>
                                                    如果指定了该项，那么将预留指定的场地，即使场地上原本有预约（该预约将被取消并通过站内信通知用户）。如果未指定序号，那么后台将会自动选择空闲的场地进行预留。若空闲场地不足，则必须手动指定序号。
                                                </small>
                                            </div>
                                            <select data-placeholder="Choose a Country..." class="chosen-select" multiple style="width:350px;">
                                                <option v-for="court in ground.courts" :key="court.id" :value="court.id">{{ court.name }}</option>
                                            </select>
                                        </div>
                                        <div class="form-group">
                                            <label class="font-normal">备注（选填）</label>
                                            <input class="form-control" type="text" ref="content" />
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-white" data-dismiss="modal">
                                            取消
                                        </button>
                                        <button type="button" class="btn btn-primary" data-dismiss="modal" v-on:click="submit(ground,index)">
                                            确认
                                        </button>
                                    </div>
                                </div>
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

<style>
@import "../../assets/css/plugins/chosen/bootstrap-chosen.css";
@import "../../assets/css/plugins/jasny/jasny-bootstrap.min.css";
@import "../../assets/css/plugins/clockpicker/clockpicker.css";
@import "../../assets/css/plugins/touchspin/jquery.bootstrap-touchspin.min.css";
@import "../../assets/css/plugins/datapicker/datepicker3.css";
@import "../../assets/css/plugins/bootstrap-tagsinput/bootstrap-tagsinput.css";

.i-row [class^="col-"] {
    padding: 10px;
}

.i-row {
    margin: 0;
}

.contact-box {
    max-width: 450px;
    padding: 10px;
}

.i-button {
    margin-bottom: 20px;
    margin-right: 10px;
}

.i-title {
    margin-top: 10px;
    font-weight: bolder;
    text-align: center;
}

.i-infobox {
    line-height: 30px;
    font-size: 13px;
    font-weight: bold;
}

.i-star {
    color: orange;
}

.i-icon {
    margin-right: 10px;
}

.i-groundinfo {
    border-top: 1px solid #e7eaec;
    font-weight: bold;
}

.chosen-container-single .chosen-single {
    padding: 4px 12px;
}

.progress-bar-default {
    background-color: #e9ecef;
}

.progress-bar-disabled {
    background-color: #9ca8b3;
}

.popover {
    z-index: 10000;
}

.bootstrap-tagsinput {
    border: 1px solid #e5e6e7;
    border-radius: 1px;
    margin-top: 10px;
    box-shadow: none;
    -webkit-box-shadow: none;
}
</style>

<script>
import Navbar from "@/components/Navbar";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Toolbox from "@/components/Toolbox";
import Common from "@/Common";
import "jquery";
import "masonry-layout";
import "@/assets/js/plugins/clockpicker/clockpicker.js";
import "@/assets/js/plugins/chosen/chosen.jquery.js";
import "@/assets/js/plugins/jasny/jasny-bootstrap.min.js";
import "@/assets/js/plugins/touchspin/jquery.bootstrap-touchspin.min.js";
import "@/assets/js/plugins/datapicker/bootstrap-datepicker.js";
import "@/assets/js/plugins/bootstrap-tagsinput/bootstrap-tagsinput.js";
import {
    duration
} from "moment";

export default {
    
    data() {
        let res = {
            grounds: [],
            dates: [],
            current_date: 0,
            form_date: "",
            form_time: "",
            form_start: "",
            form_end: "",
            stadiumName: "",
            courts: "",
            map_id_to_court: "",
            foreDays: 0,
            myDurations: [],
            flag: 0,
            current_court: 0,
            old_startTime: "",
            old_endTime: ""
        };

        return res;
    },
    components: {
        Toolbox,
        Navbar,
        Header,
        Footer
    },
    methods: {
        selectCourtType(index) {
            this.current_court = index;
        },
        setNumber(index) {
            // TODO: 检查或强制设置预约场地数量一栏的合法性
            Array.prototype.indexValue = function (arr) {
                for (var i = 0; i < this.length; i++) {
                    if (this[i] == arr) {
                        return i;
                    }
                }
                return -1;
            }
            let number = parseInt(this.$refs.number[index].value)
            let useDate = this.$refs.useDate[index].value
            let startTime = this.$refs.startTime[index].value
            let endTime = this.$refs.endTime[index].value
            var myStartTime = new Date(1, 1, 1, parseInt(startTime.split(":")[0]), parseInt(startTime.split(":")[1]));
            var myEndTime = new Date(1, 1, 1, parseInt(endTime.split(":")[0]), parseInt(endTime.split(":")[1]));
            if (startTime != '' && endTime != '' && useDate != '' && number != "") {
                let courtlist = [];
                for (var j = 0; j < this.grounds[index].courts.length; j++) {
                    courtlist.push(this.grounds[index].courts[j].id)
                }
                for (var w = 0; w < parseInt(this.grounds[index].courts[0].foreDays); w++) {
                    if (this.myDurations[w][0].date == useDate) {
                        var tmp = this.grounds[index].courts[0].courtType;
                        var list = this.myDurations[w].filter(function (x) {
                            return ( x.courtType == tmp && x.date == useDate )
                        })
                        for (var i = 0; i < list.length; i++) {
                            if (courtlist.indexValue(list[i].court) < 0) {
                                continue;
                            }
                            let start = list[i].startTime
                            let end = list[i].endTime
                            var myStart = new Date(1, 1, 1, parseInt(start.split(":")[0]), parseInt(start.split(":")[1]));
                            var myEnd = new Date(1, 1, 1, parseInt(end.split(":")[0]), parseInt(end.split(":")[1]));
                            if ((((myStart <= myStartTime) && (myStartTime <= myEnd)) || ((myStartTime <= myStart) && (myStart <= myEndTime))) && (list[i].accessible == false)) {
                                courtlist.splice(courtlist.indexValue(list[i].court),1 )
                            }
                        }
                        break;
                    }
                }
                courtlist = courtlist.slice(0, number);
                // TODO: 根据courtlist中的序号设置场地默认选中（courtlist为智能推荐场地id结果列表）
            }
        },
        submit(ground, index) {
            let number = this.$refs.number[index].value
            
            // TODO: 获取选中的场地的id列表并命名为courts
            let courts = this.$refs.court_id[index].value.split(',')

            let useDate = this.$refs.useDate[index].value
            let startTime = this.$refs.startTime[index].value
            let endTime = this.$refs.endTime[index].value
            let content = this.$refs.content[index].value
            var myStartTime = new Date(1, 1, 1, parseInt(startTime.split(":")[0]), parseInt(startTime.split(":")[1]));
            var myEndTime = new Date(1, 1, 1, parseInt(endTime.split(":")[0]), parseInt(endTime.split(":")[1]));
            if (number != courts.length) {
                swal({
                    title: "错误",
                    text: "请确认输入场地编号数与预留场地数相等",
                    type: "error"
                });
            } else if (useDate == '') {
                swal({
                    title: "错误",
                    text: "请输入日期",
                    type: "error"
                });
            } else if (startTime == "" || endTime == "") {
                swal({
                    title: "错误",
                    text: "请输入正确的起始和终止时间",
                    type: "error"
                });
            } else {
                var obj = new Date();
                var hour = parseInt(obj.getHours());
                var minute = parseInt(obj.getMinutes());
                var myDate = new Date(useDate);
                var nowDate = new Date(obj.getFullYear() + "-" + (obj.getMonth() + 1) + "-" + obj.getDate());
                let sh = parseInt(startTime.split(":")[0]);
                let sm = parseInt(startTime.split(":")[1]);
                let eh = parseInt(endTime.split(":")[0]);
                let em = parseInt(endTime.split(":")[1]);
                if (eh < sh || (eh == sh && em <= sm) || (myDate.getTime() == nowDate.getTime() && (hour > sh || (hour == sh && minute > sm)))) {
                    swal({
                        title: "错误",
                        text: "请输入正确的起始和终止时间",
                        type: "error"
                    });
                } else {
                    for (var i = 0; i < courts.length; i++) {
                        var request = {
                            court_id: parseInt(courts[i]),
                            startTime: startTime,
                            endTime: endTime,
                            date: useDate,
                            content: content,
                        }
                        console.log(request)

                        this.$axios.post("addevent/", request).then(res => {
                            if (res.data.error) {
                                swal({
                                    title: "错误",
                                    text: "请输入正确的场地编号",
                                    type: "error"
                                });
                                return;
                            }
                        });
                    }
                    swal({
                        title: "成功",
                        text: "场地预留成功",
                        type: "success"
                    });
                }
            }
        },
        manage(ground) {
            window.location.replace('/stadium_management/stadium_info/record?id=' + this.$route.query.id.toString())
        },
        setDate(date) {
            var durations;
            if (this.myDurations.length != this.foreDays) {
                let request = {
                    params: {
                        stadium_id: this.$route.query.id,
                        date: date
                    }
                };
                this.$axios.get("duration/", request).then(res => {
                    durations = res.data;
                    for (let i = 0; i < durations.length; i++) {
                        this.courts[this.map_id_to_court[durations[i].court]].reservedDuration = [];
                    }
                    for (let i = 0; i < durations.length; i++) {
                        this.courts[this.map_id_to_court[durations[i].court]].reservedDuration.push(durations[i]);
                    }
                    for (let i = 0; i < this.grounds.length; i++) {
                        for (let j = 0; j < this.grounds[i].courts.length; j++) {
                            if (this.grounds[i].courts[j].reservedDuration === undefined) {
                                this.grounds[i].courts[j].reservedDuration = [];
                            }
                            this.grounds[i].courts[j].reservedDuration = Common.fix_reserves(
                                this.grounds[i].courts[j].reservedDuration
                            );
                        }
                    }
                    this.$forceUpdate();
                });
            } else {
                durations = this.myDurations.filter(function (x) {
                    return x[0].date == date
                })[0]
                for (let i = 0; i < durations.length; i++) {
                    this.courts[this.map_id_to_court[durations[i].court]].reservedDuration = [];
                }
                for (let i = 0; i < durations.length; i++) {
                    this.courts[this.map_id_to_court[durations[i].court]].reservedDuration.push(durations[i]);
                }
                for (let i = 0; i < this.grounds.length; i++) {
                    for (let j = 0; j < this.grounds[i].courts.length; j++) {
                        if (this.grounds[i].courts[j].reservedDuration === undefined) {
                            this.grounds[i].courts[j].reservedDuration = [];
                        }
                        this.grounds[i].courts[j].reservedDuration = Common.fix_reserves(
                            this.grounds[i].courts[j].reservedDuration
                        );
                    }
                }
                this.$forceUpdate();
            }
        },
    },
    filters: {
        progress_type: function (type) {
            if (type === 0) {
                return "progress-bar progress-bar-default";
            } else if (type === 1) {
                return "progress-bar progress-bar-primary";
            } else if (type === 2) {
                return "progress-bar progress-bar-warning";
            } else if (type === -1) {
                return "progress-bar progress-bar-disabled";
            }
        },
        progress_length: function (flag, reserve, durations) {
            var sh, sm;
            sh = parseInt(durations[0].startTime.split(":")[0]);
            sm = parseInt(durations[0].startTime.split(":")[1]);
            var eh, em;
            eh = parseInt(durations[durations.length - 1].endTime.split(":")[0]);
            em = parseInt(durations[durations.length - 1].endTime.split(":")[1]);
            var h, m;
            h = parseInt(reserve.startTime.split(":")[0]);
            m = parseInt(reserve.startTime.split(":")[1]);
            var start_time = h * 60 + m;
            h = parseInt(reserve.endTime.split(":")[0]);
            m = parseInt(reserve.endTime.split(":")[1]);
            var end_time = h * 60 + m;
            var delta = (end_time - start_time) * 100 / (eh * 60 + em - sh * 60 - sm);
            if (flag == 0) {
                return "width: " + delta.toString() + "%";
            } else {
                return "display: inline-block;" + " width: " + delta.toString() + "%";
            }
        },
        progress_title: function (reserve) {
            let type = reserve.type;
            let title = "";
            if (type === 0) {
                title += "空闲时段（";
            } else if (type === 1) {
                title += "已预订时段（";
            } else if (type === 2) {
                title += "预留时段（";
            } else if (type === -1) {
                title += "不可用时段（";
            }
            title += reserve.startTime + "-" + reserve.endTime + "）";
            return title;
        }
    },
    updated() {
        $(".chosen-select").chosen({
            width: "100%"
        });
        var clocks = document.getElementsByClassName("clockpicker");
        let _this = this,
            i = 0;
        while (i < clocks.length) {
            $(clocks[i]).clockpicker().find('input').change(function () {
                _this.form_start = this.value;
            })
            i++;
            $(clocks[i]).clockpicker().find('input').change(function () {
                _this.form_end = this.value;
            });
            i++;
        }

        $("#data_1 .input-group.date").datepicker({
            todayBtn: "linked",
            keyboardNavigation: false,
            autoclose: true,
            format: "yyyy-mm-dd"
        });
        $(".tagsinput").tagsinput({
            tagClass: "label label-primary"
        });
        let spins = $(".touchspin");
        for (let i = 0; i < spins.length; i++) {
            $(spins[i]).TouchSpin({
                min: 1,
                max: this.grounds[i].courts.length,
                buttondown_class: "btn btn-white",
                buttonup_class: "btn btn-white"
            });
        }
        let number = this.$refs.number[this.current_court].value
        let useDate = this.$refs.useDate[this.current_court].value
        let startTime = this.$refs.startTime[this.current_court].value
        let endTime = this.$refs.endTime[this.current_court].value
        let flag = 0;
        if (startTime != this.old_startTime) {
            flag = 1;
        }
        if (startTime != '' && endTime != '') {
            let sh = parseInt(startTime.split(":")[0]);
            let sm = parseInt(startTime.split(":")[1]);
            let eh = parseInt(endTime.split(":")[0]);
            let em = parseInt(endTime.split(":")[1]);
            if (eh < sh || (eh == sh && em <= sm)) {
                swal({
                    title: "错误",
                    text: "请输入正确的起始和终止时间",
                    type: "error"
                });
                if (flag == 0) {
                    this.$refs.startTime[this.current_court].value = "";
                } else {
                    this.$refs.endTime[this.current_court].value = "";
                }
            }
        }
    },
    mounted() {
        $(".chosen-select").chosen({
            width: "100%"
        });
        var clocks = document.getElementsByClassName("clockpicker");
        for (var i = 0; i < clocks.length; i++) {
            $(clocks[i]).clockpicker();
        }
        $(document).ready(function () {
            $("#setEventDate").change(function () {})
            //$("#demo").val("this is lily").change()   此种方法可以，下面的方法也可以
            $("#setEventDate").val("this is lily111")
            $("#setEventDate").trigger("change")
        })
        $("#data_1 .input-group.date").datepicker({
            todayBtn: "linked",
            keyboardNavigation: false,
            autoclose: true,
            format: "yyyy-mm-dd"
        });
        $(".tagsinput").tagsinput({
            tagClass: "label label-primary"
        });
        $(".touchspin").TouchSpin({
            min: 1,
            buttondown_class: "btn btn-white",
            buttonup_class: "btn btn-white"
        });
        let request1 = {
            params: {
                id: this.$route.query.id
            }
        };
        let request2 = {
            params: {
                stadium_id: this.$route.query.id
            }
        };
        let p = Promise.all([
            this.$axios.get("stadium/", request1),
            this.$axios.get("court/", request2)
        ]);
        p.then(res => {
            var myDate = new Date();
            this.dates = [];
            for (let i = 0; i < res[0].data[0].foreDays; i++) {
                var date = new Date();
                date.setDate(date.getDate() + i);
                var dateString = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
                this.dates.push({
                    value: i,
                    label: dateString
                });
            }
            this.stadiumName = res[0].data[0].name;
            let courttypes = res[0].data[0].courtTypes;
            this.map_id_to_court = {};
            this.courts = res[1].data;
            for (let i = 0; i < this.courts.length; i++) {
                this.map_id_to_court[this.courts[i].id] = i;
            }
            let map_id_to_time = {};
            for (let i = 0; i < courttypes.length; i++) {
                map_id_to_time[courttypes[i].id] = courttypes[i].openingHours;
            }
            let map_type_to_index = {};
            for (let i = 0; i < this.courts.length; i++) {
                if (map_type_to_index[this.courts[i].type] === undefined) {
                    this.grounds.push({
                        type: this.courts[i].type,
                        courts: [],
                        openingHours: map_id_to_time[this.courts[i].courtType]
                    });
                    map_type_to_index[this.courts[i].type] = this.grounds.length - 1;
                }
                this.grounds[map_type_to_index[this.courts[i].type]].courts.push(this.courts[i]);
            }
            this.foreDays = res[0].data[0].foreDays;
            var date = new Date();
            date.setDate(date.getDate());
            var dateString = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
            this.setDate(dateString);
            for (var w = 0; w < res[0].data[0].foreDays; w++) {
                var date = new Date();
                date.setDate(date.getDate() + w);
                var dateString = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
                let request = {
                    params: {
                        stadium_id: this.$route.query.id,
                        date: dateString
                    }
                };
                this.$axios.get("duration/", request).then(res => {
                    this.myDurations.push(res.data)
                })
            }
        });
    }
};
</script>
