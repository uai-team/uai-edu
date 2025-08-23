import { getRequest, postRequest, putRequest } from '@/utils/request'

export const userApi = {
  // 用户信息
  getUserInfo: () => {
    return getRequest('/vadmin/auth/user/admin/current/info')
  },

  // 家庭作业列表
  homeworkList: (params = {}) => {
    return getRequest('/education/homework/auth/user/center', params)
  },

  // 家庭作业详情
  homeworkDetail: (params = {}) => {
    return getRequest(`/education/homework/${params.id}`, params)
  },

  // 考试试卷列表
  examPaperList: (params = {}) => {
    return getRequest('/education/paper/auth/user/center', params)
  },

  // 考试试卷详情
  examPaperDetail: (params = {}) => {
    return getRequest(`/education/paper/${params.id}`, params)
  },

  // 提交试卷
  examDoSubmit: (params = {}) => {
    return postRequest('/education/paper/auth/user/do/submit', params)
  },

  // 考试记录列表
  examRecordsList: (params = {}) => {
    return getRequest('/education/paper/auth/user/records', params)
  },

  // 考试记录详情
  examAnswerDetail: (params = {}) => {
    return getRequest(`/education/paper/auth/user/record/${params.id}`, params)
  },

  // 加入错题本
  addWrongQuestionBook: (params = {}) => {
    return postRequest(`/education/wrong/auth/user/notebook/add/${params.id}`, params)
  },

  // 我的错题本
  wrongQuestionList: (params = {}) => {
    return getRequest(`/education/wrong/auth/user/notebook/list`, params)
  },

  // 移除错题本
  removeWrongQuestionBook: (params = {}) => {
    return postRequest(`/education/wrong/auth/user/notebook/remove/${params.id}`, params)
  },

  // 艾宾浩斯遗忘曲线复习计划
  ebbinghausSchedule: (params = {}) => {
    return getRequest(`/education/wrong/auth/user/notebook/ebbinghaus/schedule`, params)
  },

  // 提交复习计划
  submitReview: (params = {}) => {
    return postRequest(`/education/wrong/auth/user/notebook/ebbinghaus/submit/${params.id}`, params)
  },
}
