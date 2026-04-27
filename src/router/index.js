import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Translate from '../views/Translate.vue'
import Shop from '../views/Shop.vue'
import Stories from '../views/Stories.vue'
import My from '../views/My.vue'
import Community from '../views/Community.vue'
import MyPosts from '../views/MyPosts.vue'
import MyOrders from '../views/MyOrders.vue'
import MyAddress from '../views/MyAddress.vue'
import MySettings from '../views/MySettings.vue'
import MyHelp from '../views/MyHelp.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/translate',
    name: 'Translate',
    component: Translate
  },
  {
    path: '/shop',
    name: 'Shop',
    component: Shop
  },
  {
    path: '/stories',
    name: 'Stories',
    component: Stories
  },
  {
    path: '/community',
    name: 'Community',
    component: Community
  },
  {
    path: '/my',
    name: 'My',
    component: My
  },
  {
    path: '/my/posts',
    name: 'MyPosts',
    component: MyPosts
  },
  {
    path: '/my/orders',
    name: 'MyOrders',
    component: MyOrders
  },
  {
    path: '/my/address',
    name: 'MyAddress',
    component: MyAddress
  },
  {
    path: '/my/settings',
    name: 'MySettings',
    component: MySettings
  },
  {
    path: '/my/help',
    name: 'MyHelp',
    component: MyHelp
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
