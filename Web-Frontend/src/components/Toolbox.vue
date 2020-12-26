<template>
    <div class="theme-config">
        <div class="theme-config-box">
            <div class="spin-icon" v-on:click="toggle()">
                <i class="fa fa-cogs fa-spin"></i>
            </div>
            <div class="skin-settings">
                <div class="title">
                    页面设置 <br>
                </div>
                <div class="setings-item">
                    <span>
                        顶级导航栏
                    </span>

                    <div class="switch">
                        <div class="onoffswitch">
                            <input type="checkbox" name="fixednavbar" class="onoffswitch-checkbox" id="fixednavbar" v-on:click="fixednavbar()">
                            <label class="onoffswitch-label" for="fixednavbar">
                                <span class="onoffswitch-inner"></span>
                                <span class="onoffswitch-switch"></span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="setings-item">
                    <span>
                        顶部导航栏V.2
                        <br>
                        <small>*主要布局</small>
                    </span>

                    <div class="switch">
                        <div class="onoffswitch">
                            <input type="checkbox" name="fixednavbar2" class="onoffswitch-checkbox" id="fixednavbar2" v-on:click="fixednavbar2()">
                            <label class="onoffswitch-label" for="fixednavbar2">
                                <span class="onoffswitch-inner"></span>
                                <span class="onoffswitch-switch"></span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="setings-item">
                    <span>
                        盒子布局
                    </span>

                    <div class="switch">
                        <div class="onoffswitch">
                            <input type="checkbox" name="boxedlayout" class="onoffswitch-checkbox" id="boxedlayout" v-on:click="boxedlayout()">
                            <label class="onoffswitch-label" for="boxedlayout">
                                <span class="onoffswitch-inner"></span>
                                <span class="onoffswitch-switch"></span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="setings-item">
                    <span>
                        固定页脚
                    </span>

                    <div class="switch">
                        <div class="onoffswitch">
                            <input type="checkbox" name="fixedfooter" class="onoffswitch-checkbox" id="fixedfooter" v-on:click="fixedfooter()">
                            <label class="onoffswitch-label" for="fixedfooter">
                                <span class="onoffswitch-inner"></span>
                                <span class="onoffswitch-switch"></span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="title">换肤</div>
                <div class="setings-item default-skin">
                    <span class="skin-name ">
                        <a href="#" class="s-skin-0" v-on:click="skin('0')">
                            默认
                        </a>
                    </span>
                </div>
                <div class="setings-item blue-skin">
                    <span class="skin-name ">
                        <a href="#" class="s-skin-1" v-on:click="skin('1')">
                            蓝色
                        </a>
                    </span>
                </div>
                <div class="setings-item yellow-skin">
                    <span class="skin-name ">
                        <a href="#" class="s-skin-3" v-on:click="skin('3')">
                            黄色
                        </a>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<style>

</style>

<script>
import Common from "@/Common"
import "@/assets/js/jquery-3.1.1.min.js";
export default {
    data() {
        return {}
    },
    methods: {
        toggle() {
            $(".theme-config-box").toggleClass("show");
        },
        skin(n) {
            if(n === '1'){
                $("body").removeClass("skin-3")
                $("body").removeClass("skin-2")
                $("body").addClass("skin-1")
            }
            else if(n === '2'){
                $("body").removeClass("skin-1")
                $("body").removeClass("skin-3")
                $("body").addClass("skin-2")
            }
            else if(n === '3'){
                $("body").removeClass("skin-1")
                $("body").removeClass("skin-2")
                $("body").addClass("skin-3")
            }
            else{
                $("body").removeClass("skin-1")
                $("body").removeClass("skin-2")
                $("body").removeClass("skin-3")
            }
            localStorage.setItem("colortype", n);
        },
        fixednavbar() {
            if ($('#fixednavbar').is(':checked')) {
                $(".navbar-static-top").removeClass('navbar-static-top').addClass('navbar-fixed-top');
                $("body").removeClass('boxed-layout');
                $("body").addClass('fixed-nav');
                $('#boxedlayout').prop('checked', false);
                localStorage.setItem("boxedlayout", 'off');
                localStorage.setItem("fixednavbar", 'on');
            } 
            else {
                $(".navbar-fixed-top").removeClass('navbar-fixed-top').addClass('navbar-static-top');
                $("body").removeClass('fixed-nav');
                $("body").removeClass('fixed-nav-basic');
                $('#fixednavbar2').prop('checked', false);
                localStorage.setItem("fixednavbar", 'off');
                localStorage.setItem("fixednavbar2", 'off');
            }
        },
        fixednavbar2() {
            if ($('#fixednavbar2').is(':checked')) {
                $(".navbar-static-top").removeClass('navbar-static-top').addClass('navbar-fixed-top');
                $("body").removeClass('boxed-layout');
                $("body").addClass('fixed-nav').addClass('fixed-nav-basic');
                $('#boxedlayout').prop('checked', false);
                localStorage.setItem("boxedlayout", 'off');
                localStorage.setItem("fixednavbar2", 'on');
            } 
            else {
                $(".navbar-fixed-top").removeClass('navbar-fixed-top').addClass('navbar-static-top');
                $("body").removeClass('fixed-nav').removeClass('fixed-nav-basic');
                $('#fixednavbar').prop('checked', false);
                localStorage.setItem("fixednavbar2", 'off');
                localStorage.setItem("fixednavbar", 'off');
            }
        },
        boxedlayout() {
            if ($('#boxedlayout').is(':checked')) {
                $("body").addClass('boxed-layout');
                $('#fixednavbar').prop('checked', false);
                $('#fixednavbar2').prop('checked', false);
                $(".navbar-fixed-top").removeClass('navbar-fixed-top').addClass('navbar-static-top');
                $("body").removeClass('fixed-nav');
                $("body").removeClass('fixed-nav-basic');
                $(".footer").removeClass('fixed');
                $('#fixedfooter').prop('checked', false);
                localStorage.setItem("fixednavbar", 'off');
                localStorage.setItem("fixednavbar2", 'off');
                localStorage.setItem("fixedfooter", 'off');
                localStorage.setItem("boxedlayout", 'on');
            } 
            else {
                $("body").removeClass('boxed-layout');
                localStorage.setItem("boxedlayout", 'off');
            }
        },
        fixedfooter() {
            if ($('#fixedfooter').is(':checked')) {
                $('#boxedlayout').prop('checked', false);
                $("body").removeClass('boxed-layout');
                $(".footer").addClass('fixed');
                localStorage.setItem("boxedlayout", 'off');
                localStorage.setItem("fixedfooter", 'on');
            } 
            else {
                $(".footer").removeClass('fixed');
                localStorage.setItem("fixedfooter", 'off');
            }
        }
    },
    mounted() {
        var fixednavbar = localStorage.getItem("fixednavbar")
        var fixednavbar2 = localStorage.getItem("fixednavbar2")
        var boxedlayout = localStorage.getItem("boxedlayout")
        var fixedfooter = localStorage.getItem("fixedfooter")
        var colortype = localStorage.getItem("colortype")
        if (fixednavbar == 'on') {
            $('#fixednavbar').prop('checked', 'checked')
        }
        if (fixednavbar2 == 'on') {
            $('#fixednavbar2').prop('checked', 'checked')
        }
        if (boxedlayout == 'on') {
            $('#boxedlayout').prop('checked', 'checked')
        }
        if (fixedfooter == 'on') {
            $('#fixedfooter').prop('checked', 'checked')
        }
        if(!colortype) colortype = '0'
        this.skin(colortype)
        
    }
}
</script>