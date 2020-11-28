import Vue from 'vue'
import Router from 'vue-router'

// route views
import Login from '@/views/Login'
import Home from '@/views/Home'
import StadiumInfo from '@/views/StadiumManagement/StadiumInfo'
import UserFeedback from '@/views/StadiumManagement/UserFeedback'
import GroundReserve from '@/views/StadiumManagement/GroundReserve'
import ReserveRecord from '@/views/StadiumManagement/ReserveRecord'
import UserInfo from '@/views/UserManagement/UserInfo'
import BlackList from '@/views/UserManagement/BlackList'
import OperationRecord from '@/views/OperationRecord'
import Statistic from '@/views/Statistic'
import SystemLog from '@/views/SystemLog'
import NewStadium from '@/views/StadiumManagement/NewStadium'
import EditStadium from '@/views/StadiumManagement/EditStadium'
import EditGround from '@/views/StadiumManagement/EditGround'

Vue.use(Router)

export default new Router({
    routes: [{
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/home',
            name: 'Home',
            component: Home
        },
        {
            path: '/stadium_management/stadium_info',
            name: 'StadiumInfo',
            component: StadiumInfo
        },
        {
            path: '/stadium_management/user_feedback',
            name: 'UserFeedback',
            component: UserFeedback
        },
        {
            path: '/stadium_management/ground_reserve',
            name: 'GroundReserve',
            component: GroundReserve
        },
        {
            path: '/stadium_management/reserve_record',
            name: 'ReserveRecord',
            component: ReserveRecord
        },
        {
            path: '/user_management/user_info',
            name: 'UserInfo',
            component: UserInfo
        },
        {
            path: '/use_managemant/black_list',
            name: 'BlackList',
            component: BlackList
        },
        {
            path: '/operation_record',
            name: 'OperationRecord',
            component: OperationRecord
        },
        {
            path: '/statistic',
            name: 'Statistic',
            component: Statistic
        },
        {
            path: '/system_log',
            name: 'SystemLog',
            component: SystemLog
        },
        {
            path: '/stadium_management/:managerId/stadium_info/new_stadium',
            name: 'NewStadium',
            component: NewStadium
        },
        {
            path: '/stadium_management/:managerId/stadium_info/edit_stadium/:stadiumId/',
            name: 'EditStadium',
            component: EditStadium
        },
        {
            path: '/stadium_management/:managerId/stadium_info/edit_ground/:stadiumId/',
            name: 'EditGround',
            component: EditGround
        }
    ],
    mode: 'history',
    base: process.env.BASE_URL
})