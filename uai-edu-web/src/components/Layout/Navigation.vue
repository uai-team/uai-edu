<template>
  <el-header>
    <div class="top">
      <div class="top-nav">
        <a href="/"><img v-if="info" :src="info.web_logo" alt="" /></a>
        <div v-for="(item, index) in nav" :key="index" class="top-nav-title">
          <router-link v-if="!isExternalUrl(item.navUrl)" :to="{ path: item.navUrl }"
            :class="{ active: route.path.startsWith(item.navUrl) }">
            {{ item.navTitle }}
          </router-link>
          <a v-else :href="item.navUrl" :target="item.target">{{ item.navTitle }}</a>
        </div>
        <div class="top-nav-title">
          <router-link :to="{ path: '/labs/list' }" :class="{ active: route.path.startsWith('/labs/list') }">
            <div style="display: flex; align-items: center;">
              <img
                src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjIxLjciIGhlaWdodD0iNSIgcng9IjIuNSIgdHJhbnNmb3JtPSJzY2FsZSgtMSAxKSByb3RhdGUoLTU5LjM4OCA4Ljc2IDMzLjI5MykiIGZpbGw9InVybCgjYSkiLz48bWFzayBpZD0iYiIgc3R5bGU9Im1hc2stdHlwZTphbHBoYSIgbWFza1VuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeD0iOSIgeT0iNSIgd2lkdGg9IjkiIGhlaWdodD0iMTEiPjxwYXRoIHRyYW5zZm9ybT0ic2NhbGUoLTEgMSkgcm90YXRlKC01OS4zODggMi41MDYgMjIuMzIzKSIgZmlsbD0iI2ZmZiIgZD0iTTAgMGg5LjE4OXY1SDB6Ii8+PC9tYXNrPjxnIG1hc2s9InVybCgjYikiPjxyZWN0IHdpZHRoPSIyMS43IiBoZWlnaHQ9IjUiIHJ4PSIyLjUiIHRyYW5zZm9ybT0ic2NhbGUoLTEgMSkgcm90YXRlKC01OS4zODggOC43NiAzMy4yOTMpIiBmaWxsPSJ1cmwoI2MpIi8+PC9nPjxyZWN0IHk9IjIzLjg3OSIgd2lkdGg9IjIxLjciIGhlaWdodD0iNSIgcng9IjIuNSIgdHJhbnNmb3JtPSJyb3RhdGUoLTU5LjM4OCAwIDIzLjg4KSIgZmlsbD0idXJsKCNkKSIvPjxyZWN0IHdpZHRoPSIxMS44NTkiIGhlaWdodD0iNSIgcng9IjIuNSIgdHJhbnNmb3JtPSJzY2FsZSgtMSAxKSByb3RhdGUoLTg5LjcgLTIuMDg3IDI4KSIgZmlsbD0idXJsKCNlKSIvPjxwYXRoIGQ9Im0zMiA4Ljg2NC0zLjIxNC0xLjI4NkwyNy41IDQuMzY0bC0xLjI4NiAzLjIxNEwyMyA4Ljg2NGwzLjIxNCAxLjI4NSAxLjI4NiAzLjIxNSAxLjI4Ni0zLjIxNUwzMiA4Ljg2NFoiIGZpbGw9InVybCgjZikiLz48cmVjdCB3aWR0aD0iMTQuMDcxIiBoZWlnaHQ9IjUiIHJ4PSIyLjUiIHRyYW5zZm9ybT0ic2NhbGUoLTEgMSkgcm90YXRlKC0uNDcgMjUxNC4zNCAxODM1LjQzNykiIGZpbGw9InVybCgjZykiLz48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImEiIHgxPSIwIiB5MT0iMi41IiB4Mj0iMjEuNyIgeTI9IjIuNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMxRTYyRUMiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyOEQzRkQiLz48L2xpbmVhckdyYWRpZW50PjxsaW5lYXJHcmFkaWVudCBpZD0iYyIgeDE9IjE0Ljc1MyIgeTE9IjMuMzAxIiB4Mj0iMTkuMDk5IiB5Mj0iNy43MDEiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBzdG9wLWNvbG9yPSIjNTg2RkZGIiBzdG9wLW9wYWNpdHk9IjAiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM1ODZGRkYiLz48L2xpbmVhckdyYWRpZW50PjxsaW5lYXJHcmFkaWVudCBpZD0iZCIgeDE9IjAiIHkxPSIyNi4zNzkiIHgyPSIyMS43IiB5Mj0iMjYuMzc5IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agc3RvcC1jb2xvcj0iIzNBNzhGNiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzI4RDNGRCIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJlIiB4MT0iMCIgeTE9IjIuNSIgeDI9IjExLjg1OSIgeTI9IjIuNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMzQTc4RjYiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyOEQzRkQiLz48L2xpbmVhckdyYWRpZW50PjxsaW5lYXJHcmFkaWVudCBpZD0iZiIgeDE9IjIzIiB5MT0iOC44NjQiIHgyPSIzMiIgeTI9IjguODY0IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHN0b3Agc3RvcC1jb2xvcj0iIzNBNzhGNiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzI4RDNGRCIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJnIiB4MT0iMCIgeTE9IjIuNSIgeDI9IjE0LjA3MSIgeTI9IjIuNSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMzQTc4RjYiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyOEQzRkQiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48L3N2Zz4=" />
              实验室
            </div>
          </router-link>
        </div>
      </div>
      <div v-if="route.path != '/search'" class="top-search">
        <el-input v-model="search" autofocus placeholder="请输入搜索内容" @keyup.enter="handleSearch">
          <template #prefix>
            <img src="@/assets/svg/search.svg" />
          </template>
        </el-input>
      </div>
      <div class="top-user">
        <div v-if="loginStatus">
          <User />
        </div>
        <div v-else>
          <router-link :to="{ path: '/login' }"> 登录 </router-link>
        </div>
      </div>
    </div>
  </el-header>
</template>
<script setup>
import { indexApi } from '@/api/index'
import { isExternalUrl } from '@/utils/base'
import { getToken } from '@/utils/cookie'
import { getStorage, setStorage } from '@/utils/storage'

const route = useRoute()

// 网站信息
const info = ref({})
// 导航信息
const nav = ref([{
  navUrl: "/home",
  navTitle: "首页",
  target: "_self"
}, {
  navUrl: "/course/list",
  navTitle: "课程中心",
  target: "_self"
}, {
  navUrl: "/book/list",
  navTitle: "教材中心",
  target: "_self"
}, {
  navUrl: "/simulation/list",
  navTitle: "仿真中心",
  target: "_self"
}, {
  navUrl: "/competition/list",
  navTitle: "竞赛中心",
  target: "_self"
}])
//
const loginStatus = ref(false)

const search = ref('')

onMounted(() => {
  // 站点信息
  info.value = getStorage('WebsiteInfo')
  if (!info.value) {
    indexApi.websiteInfo().then((res) => {
      setStorage('WebsiteInfo', res, 60)
      info.value = res
    })
  }

  const token = getToken()
  if (token) {
    loginStatus.value = true
  }
})

// 搜索
function handleSearch() {
  useRouter().push({ name: 'search', query: { kw: search.value } })
}
</script>
<style lang="scss" scoped>
.el-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #fff;
  z-index: 999;
  height: 70px;
  display: flex;
  justify-content: center;
  border: 1px solid #ebeef5;
}

.active {
  color: #46c37b;
}

.top {
  width: 1200px;
  min-width: 1200px;
  height: 70px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  .top-nav {
    display: flex;
    align-items: center;

    .top-nav-title {
      margin-left: 30px;
      font-size: 18px;
    }

    // .top-nav-title:last-child {
    //   border-radius: 10px;
    //   color: #fff;
    //   border-color: #46c37b;
    //   background-color: #46c37b;
    //   padding: 8px 10px;
    // }
  }

  .top-search {
    .el-input {
      height: 35px;
      line-height: 35px;
    }

    img {
      width: 20px;
    }
  }

  .top-user {
    img {
      border-radius: 50%;
    }

    a {
      font-size: 16px;
      margin-left: 10px;
    }
  }

  img {
    height: 35px;
    width: auto;
  }
}
</style>
