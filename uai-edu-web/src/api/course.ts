import { getRequest, postRequest } from '@/utils/request'

export const courseApi = {
  // 课程列表(搜索)
  courseList: (params = {}) => {
    return getRequest('/education/course/center', params)
  },

  // 课程详情
  courseDetail: (params = {}) => {
    return getRequest(`/education/course/detail/${params.id}`, params)
  },

  // 获取播放信息
  studyLesson: (params = {}) => {
    return postRequest('/education/lesson/auth/study', params)
  },

  // 同步学习进度
  studyProgress: (params = {}) => {
    return postRequest('/education/lesson/auth/study/progress', params)
  },

  // 课程评论列出
  courseCommentPage: (params = {}) => {
    return postRequest('/course/api/course/comment', params)
  },

  // 课程详情(登录后)
  userCourseDetail: (params = {}) => {
    return postRequest('/course/auth/course/view', params)
  },

  // 课程评论添加
  courseCommentAdd: (params = {}) => {
    return postRequest('/course/auth/user/course/comment/add', params)
  },

  // 课程收藏添加
  courseCollectAdd: (params = {}) => {
    return postRequest('/course/auth/user/course/collect/add', params)
  }
}
