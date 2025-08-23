<template>
  <client-only>
    <el-dropdown>
      <span class="el-dropdown-link">
        <img v-if="userInfo?.avatar" class="header-image" :src="userInfo.avatar" alt="头像" />
        <img v-else class="header-image" src="@/assets/images/common_head.jpg" alt="头像" />
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>
            <router-link :to="{ path: '/account/homework/list' }"> 我的作业 </router-link>
          </el-dropdown-item>
          <el-dropdown-item>
            <router-link :to="{ path: '/account/exam/list' }"> 我的考试 </router-link>
          </el-dropdown-item>
          <el-dropdown-item>
            <router-link :to="{ path: '/account/exam/records' }"> 考试记录 </router-link>
          </el-dropdown-item>
          <el-dropdown-item>
            <router-link :to="{ path: '/account/wrong/list' }"> 我的错题 </router-link>
          </el-dropdown-item>
          <el-dropdown-item>
            <router-link :to="{ path: '/account/wrong/ebbinghaus' }"> 错题复习 </router-link>
          </el-dropdown-item>
          <el-dropdown-item>
            <nuxt-link :to="{ name: 'account-user' }"> 个人信息 </nuxt-link>
          </el-dropdown-item>
          <el-dropdown-item @click="handleLogout"> 安全退出 </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </client-only>
</template>
<script setup>
import { logout } from '@/utils/login'
import { getStorageUser } from '@/utils/storage'

const userInfo = ref(null)
onMounted(async () => {
  userInfo.value = getStorageUser()
})


// 退出登录
function handleLogout() {
  ElMessageBox.confirm('确认退出', '退出登录', {
    confirmButtonText: '确认',
    showCancelButton: false,
    type: 'warning'
  }).then(() => {
    logout()
    location.reload()
  })
}
</script>
<style lang="scss" scoped>
.header-image {
  border-radius: 50%;
  height: 40px;
}
</style>
