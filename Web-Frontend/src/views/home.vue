<template>
    <div>
        <Header></Header>
        <div class="dropdown-divider"></div>
        <Navbar></Navbar>
    </div>
</template>

<script>
import Navbar from "../components/Navbar"
import Header from "../components/Header"
export default {
    data(){
        return {}
    },
    components: {
        Navbar, Header
    }
}
</script>