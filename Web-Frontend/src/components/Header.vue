<template>
    <div class="row border-bottom">
        <nav class="navbar navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <a class="navbar-minimalize minimalize-styl-2 btn btn-primary " href="#"><i
                        class="fa fa-bars"></i> </a>
            </div>
            <ul class="nav navbar-top-links navbar-right">
                <li style="padding: 20px">
                    <span class="m-r-sm text-muted welcome-message">{{ time }}</span>
                </li>
                <li>
                    <a href="/login">
                        <i class="fa fa-sign-out"></i> 注销
                    </a>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    data() {
        return {
            time: "",
            messages: [
                {
                    user: "cbx",
                    time: new Date(),
                    image: "/static/img/dog.jpg"
                },
                {
                    user: "cnx",
                    time: new Date() - 200000,
                    image: "/static/img/a1.jpg"
                },
                {
                    user: "hhy",
                    time: new Date() - 3890000,
                    image: "/static/img/a3.jpg"
                }
            ]
        }
    },
    created() {
        this.time += new Date().getFullYear() + "-" + (new Date().getMonth() + 1) + "-" + new Date().getDate()
    },
    mounted(){}
}
</script>