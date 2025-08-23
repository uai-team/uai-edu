import { getRequest, postRequest } from '@/utils/request'

export const categoryApi = {
  // 类目列表
  categoryList: (params = {}) => {
    return getRequest('/education/category', params)
  },
}
