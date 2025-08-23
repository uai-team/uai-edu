<template>
  <div class="main exam-list">
    <!-- 暂没数据 -->
    <div v-if="page.list.length === 0" class="no-data">暂无数据</div>
    <el-row v-else class="exam_body" :gutter="20">
      <el-col v-for="(exam, int) in page.list" :key="int" :span="6" class="exam_body_item">
        <div class="exam_info">
          <div class="exam_name" v-html="exam.paper_name"></div>
          <div class="exam_desc">学科科目：{{ exam.category_name }}</div>
          <div class="exam_desc">考试时长：{{ exam.paper_time }} 分钟</div>
          <div class="exam_desc">试卷总分：{{ exam.paper_score }} 分</div>
          <router-link :to="{ path: '/account/exam/do', query: { id: exam.id } }">开始答题
          </router-link>
        </div>
      </el-col>
    </el-row>
    <!-- 分页功能 -->
    <div v-if="page.totalCount >= 1" class="pagination clearfix">
      <CommonPagination v-model:current-page="page.pageCurrent" v-model:page-size="page.pageSize"
        :total="page.totalCount" @pagination="handlePage" />
    </div>
  </div>
</template>
<script setup>
import CommonPagination from '@/components/Common/Pagination.vue'
import { userApi } from '@/api/user'
import useTable from '@/utils/table'

const router = useRouter()
const route = useRoute()

// 分页查询
const { page, handlePage, query, handleQuery } = useTable(
  { page: userApi.examPaperList },
  {}
)
</script>
<style lang="scss" scoped>
.exam-list {
  padding: 10px 0;
}

.exam_body {
  .exam_body_item {
    height: 215px;
    border-radius: 6px;
    margin: 10px 0;

    .exam_info {
      height: 190px;
      border-radius: 6px;
      padding: 10px;
      background-color: #fff;

      .exam_name {
        font-size: 18px;
        margin-top: 5px;
        padding-left: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-height: 25px;
        height: 50px;
      }

      .exam_desc {
        font-size: 16px;
        margin-top: 5px;
        padding-left: 10px;
        color: #999;
      }

      &:hover {
        box-shadow: 0px 0px 0px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
        transition: all 0.3s;
      }

      a {
        display: block;
        font-size: 16px;
        text-align: center;
        float: right;
        color: rgb(0, 191, 255);
        width: 70px;
        margin-top: 10px;
        padding: 8px;
        border-radius: 6px;

        &:hover {
          background-color: #eee;
          text-decoration: none;
        }
      }
    }
  }
}
</style>