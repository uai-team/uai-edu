<template>
  <div class="login_body">
    <div class="login_box">
      <div class="login_logo">
        <img src="@/assets/images/common_login.png" />
      </div>
      <div class="login_content">
        <div v-if="isPwdLogin" class="login_pc">
          <div class="login_form">
            <div class="login_title">账号登录</div>
            <el-form v-loading="loading" :model="loginForm" @keyup.enter="handleLogin()">
              <el-form-item class="form-group" prop="mobile">
                <el-input v-model="loginForm.telephone" placeholder="手机号" autofocus />
              </el-form-item>
              <el-form-item class="form-group" prop="password">
                <el-input v-model="loginForm.password" placeholder="密码" type="password" show-password />
              </el-form-item>
              <div class="login-info">
                <el-checkbox v-model="loginForm.isAgreement" size="default"> 登录即同意<span class="blue_text"
                    @click="loginForm.visible = true">《隐私政策》</span> </el-checkbox>
                <!-- <router-link :to="{ path: '/reset' }">
                    <div class="login-info-reset">忘记密码？</div>
                  </router-link> -->
              </div>
              <el-button class="login-button" type="primary" size="large" @click="handleLogin()"> 马上登录 </el-button>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { loginApi } from '@/api/login'
import { userApi } from '@/api/user'
import { getBrowserInfo, getOsInfo } from '@/utils/base'
import { setStorageUser } from '@/utils/storage'
import { login } from '@/utils/login'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const binding = ref(false)

// 是否为密码登录
const isPwdLogin = ref(true)
// 密码
const mobilePwd = ref('')

// 登录信息
const loginForm = reactive({
  method: '0',
  isAgreement: true
})
// 绑定信息
const bindingForm = reactive({
  isAgreement: true
})

const wxLoginUrl = ref('')

onMounted(async () => {
})

async function handleLogin() {
  if (!loginForm.telephone) {
    ElMessage.warning('请输入账号')
    return
  }
  if (!loginForm.password) {
    ElMessage.warning('请输入密码')
    return
  }
  if (!loginForm.isAgreement) {
    ElMessage.warning('请阅读并同意用户协议')
    return
  }
  loading.value = true
  try {
    // 密码加密
    loginForm.os = getOsInfo()
    loginForm.browser = getBrowserInfo().name
    const res = await loginApi.userLogin(loginForm)
    login(`${res.token_type} ${res.access_token}`)
    const user = await userApi.getUserInfo()
    setStorageUser(user)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
<style lang="scss" scoped>
.login_body {
  background-color: #2256f7;
  height: calc(100vh - 130px);

  .login_box {
    width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .login_logo {
    float: left;
    width: 40%;
    margin-right: 10%;
  }

  .login_content {
    float: right;
    width: 400px;
    height: 480px;
    background-color: #fff;
    border-radius: 10px;

    .login_pc {
      padding: 0 40px;
    }

    .login_app {
      height: 100%;
      padding: 0 40px;

      .login_iframe {
        border: none;
        width: 100%;
        height: 100%;
      }
    }
  }

  .login_ico {
    float: right;
  }

  .login_title {
    color: #2256f6;
    font-size: 24px;
    margin: 20px auto;
    text-align: center;
  }

  .login-info {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .login-info-reset {
      color: #2256f6;
    }
  }

  .login-button {
    margin-top: 100px;
  }

  .login_other {
    color: #2256f6;
    font-size: 14px;
    overflow: hidden;
    text-align: center;
    margin-bottom: 20px;
  }
}

.var-input {
  width: 220px;
}

.var-img {
  margin-left: 20px;
  width: 80px;
}

.el-input {
  height: 40px;
  line-height: 40px;
}

.el-button {
  width: 100%;
  margin: 20px 0;
}
</style>
