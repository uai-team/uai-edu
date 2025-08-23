import { getRequest, postRequest } from '@/utils/request'

export const bookApi = {
  // 教材列表(搜索)
  bookList: (params = {}) => {
    return getRequest('/education/book/center', params)
  },

  // 教材详情
  bookDetail: (params = {}) => {
    return getRequest(`/education/book/detail/${params.id}`, params)
  },
}
