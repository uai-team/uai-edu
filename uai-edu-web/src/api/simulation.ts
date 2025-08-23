import { getRequest } from '@/utils/request'

export const simulationApi = {
  // 仿真列表(搜索)
  simulationList: (params = {}) => {
    return getRequest('/education/simulation/center', params)
  },

  // 仿真详情
  simulationDetail: (params = {}) => {
    return getRequest(`/education/simulation/detail/${params.id}`, params)
  },
}
