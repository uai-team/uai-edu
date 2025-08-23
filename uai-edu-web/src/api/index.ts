import { getRequest, postRequest } from '@/utils/request'

export const indexApi = {
  // 首页轮播图
  carouselList: () => {
    return getRequest('/education/carousel')
  },
  // 类目列表
  categoryList: (params = {}) => {
    return getRequest('/education/category', params)
  },
  // 专区课程
  zoneList: (params = {}) => {
    return getRequest('/education/zone/course', params)
  },
  // 站点信息
  websiteInfo: () => {
    return getRequest('/vadmin/system/settings/tabs/values', { tab_id: 1 })
  },
  // 友情链接
  websiteLink: () => {
    return getRequest('/vadmin/resource/links?page=1&limit=10&link_type=1')
  },
}
