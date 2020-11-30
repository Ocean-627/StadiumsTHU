<template>
    <div id="wrapper">
        <Navbar></Navbar>
        <div id="page-wrapper" class="gray-bg dashbard-1">
            <Header></Header>
            <div class="row border-bottom white-bg dashboard-header">
                <div class="col-md-3">
                    <h2>欢迎您，马保国</h2>
                    <small>您有42条消息和6条通知。</small>
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
export default {
    data() {
        return {}
    },
    components: {
        Toolbox, Navbar, Header, Footer
    },
    mounted() {
        setTimeout(function () {
            toastr.options = {
                closeButton: true,
                progressBar: true,
                showMethod: 'slideDown',
                timeOut: 4000
            };
            toastr.success('清动家园管理者', '欢迎您 马保国');
        }, 1300);
    }
}

</script>
