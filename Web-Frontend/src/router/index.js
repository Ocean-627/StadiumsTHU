import Vue from 'vue'
import Router from 'vue-router'

// route views
import Login from '@/views/Login'
import Home from '@/views/Home'
import Profile from "@/views/Profile"
import Messages from "@/views/Messages";
import MessagesDetail from "@/views/MessagesDetail";
import StadiumInfo from '@/views/StadiumManagement/StadiumInfo'
import UserFeedback from '@/views/StadiumManagement/UserFeedback'
import GroundReserve from '@/views/StadiumManagement/GroundReserve'
import ReserveRecord from '@/views/StadiumManagement/ReserveRecord'
import UserInfo from '@/views/UserManagement/UserInfo'
import UserInfoDetail from '@/views/UserManagement/UserInfoDetail'
import OperationRecord from '@/views/OperationRecord'
import Statistic from '@/views/Statistic'
import SystemLog from '@/views/SystemLog'
import NewStadium from '@/views/StadiumManagement/NewStadium'
import EditStadium from '@/views/StadiumManagement/EditStadium'
import EditGround from '@/views/StadiumManagement/EditGround'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/home",
      name: "Home",
      component: Home
    },
    {
      path: "/profile",
      name: "Profile",
      component: Profile
    },
    {
      path: "/messages",
      name: "Messages",
      component: Messages
    },
    {
      path: "/messages/detail",
      name: "MessagesDetail",
      component: MessagesDetail
    },
    {
      path: "/stadium_management/stadium_info",
      name: "StadiumInfo",
      component: StadiumInfo
    },
    {
      path: "/stadium_management/user_feedback",
      name: "UserFeedback",
      component: UserFeedback
    },
    {
      path: "/stadium_management/stadium_info/detail",
      name: "GroundReserve",
      component: GroundReserve
    },
    {
      path: "/stadium_management/stadium_info/record",
      name: "ReserveRecord",
      component: ReserveRecord
    },
    {
      path: "/user_management",
      name: "UserInfo",
      component: UserInfo
    },
    {
      path: "/user_management/detail/:userId",
      name: "UserInfoDetail",
      component: UserInfoDetail
    },
    {
      path: "/operation_record",
      name: "OperationRecord",
      component: OperationRecord
    },
    {
      path: "/statistic",
      name: "Statistic",
      component: Statistic
    },
    {
      path: "/system_log",
      name: "SystemLog",
      component: SystemLog
    },
    {
      path: "/stadium_management/stadium_info/new_stadium",
      name: "NewStadium",
      component: NewStadium
    },
    {
      path: "/stadium_management/stadium_info/edit_stadium",
      name: "EditStadium",
      component: EditStadium
    },
    {
      path: "/stadium_management/stadium_info/edit_ground",
      name: "EditGround",
      component: EditGround
    }
  ],
  mode: "history",
  base: process.env.BASE_URL
});