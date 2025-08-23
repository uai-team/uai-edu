import { postRequest } from '@/utils/request'

export const loginApi = {
  // 密码登录
  userLogin: (params = {}) => {
    return postRequest('/user/login', params)
  },
  // 修改密码
  updatePassword: (params = {}) => {
    return postRequest('/user/password', params)
  }
}
