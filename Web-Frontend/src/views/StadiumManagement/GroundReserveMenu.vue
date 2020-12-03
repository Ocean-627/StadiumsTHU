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
                            <a href="/home">主页</a>
                        </li>
                        <li class="breadcrumb-item">
                            场馆管理
                        </li>
                        <li class="breadcrumb-item active">
                            <strong>场地预留</strong>
                        </li>
                    </ol>
                </div>
            </div>
            <div class="wrapper wrapper-content animated fadeInRight">
                <div class="grid" v-masonry transition-duration="0.3s" item-selector=".grid-item" horizontal-order="true" gutter="25">
                    <div class="grid-item" v-masonry-tile
                        v-for="stadium in stadiums" v-bind:key="stadium.name" v-on:click="enter(stadium)">
                        <div class="contact-box">
                            <!-- 主要部分 & 单个单元 -->
                            <div class="row i-row">
                                <div class="col-md-7">
                                    <img alt="image" class="rounded m-t-xs img-fluid" :src="stadium.images[0].image">
                                </div>
                                <div class="col-md-5 i-infobox">
                                    <h2 class="i-title"><strong>{{stadium.name}}</strong></h2>
                                    <i class="fa fa-comment-o i-icon"></i>{{stadium.comments}}条评论 <br>
                                    <i class="fa fa-clock-o i-icon"></i>开放时间：{{stadium.openTime}} - {{stadium.closeTime}}<br>
                                    <i class="fa fa-location-arrow i-icon"></i>{{stadium.location}}<br>
                                    <div class="i-score">
                                        <i v-for="num in 5" :key="num" style="margin-right: 3px" :class="(num<=stadium.score)?'fa fa-star i-star':((num-0.5<=stadium.score)?'fa fa-star-half-o i-star':'fa fa-star-o i-star')"></i> {{ stadium.score }}
                                    </div>
                                </div>
                            </div>
                            <div class="row i-row i-groundinfo">
                                <div class="col-md-12">
                                    开放场地：
                                    <a v-for="courtType in stadium.courtTypes" v-bind:key="courtType.name">
                                            {{courtType.type}}场 {{courtType.amount}} 个&emsp;
                                        </a>
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
.i-row [class^="col-"] {
    padding: 10px;
}

.i-row {
    margin: 0;
}

.contact-box {
    max-width: 500px;
    padding: 15px;
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
</style>

<script>
import Navbar from "@/components/Navbar"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import Toolbox from "@/components/Toolbox"
import 'jquery'

export default {
    data() {
        return {
            stadiums: []
        }
    },
    components: {
        Toolbox,
        Navbar,
        Header,
        Footer
    },
    mounted() {
        this.$axios.get('stadium/', {})
            .then(res => {
                if (res.data.error) {
                    swal({
                        title: "错误", 
                        text: "出现了未知错误，请刷新重试！", 
                        type: "error",
                    })
                } else {
                    //console.log(res.data)
                    this.stadiums = res.data
                }
            })
    },
    methods: {
        enter(stadium) {
            window.location.replace('/stadium_management/ground_reserve/detail?id='+stadium.id.toString())
        }
    }
}
</script>
