<template>
  <div class="main">
    <div class="ebbinghaus_schedule">
      <h2>艾宾浩斯遗忘曲线复习计划</h2>
      <div style="text-align: left; width:fit-content; margin:0 auto; font-size: 16px;">
        <span>全部题目总数：{{ res.total_problems }}</span><br />
        <span>待复习题目数：{{ res.problems_to_review }}</span><br />
        <span>复习完成比例：{{ res.review_rate }}</span><br />
        <span>近期复习计划：</span><br />
        <ul>
          <li v-for="(item, index) in res.review_stages" :key="index">
            {{ index }}日前需要复习：{{ item }} 题
          </li>
        </ul>
      </div>
    </div>
    <h1>今日复习题目</h1>
    <div class="exam-question-item" v-for="(item, index) in res.today_to_review" :key="index">
      <span class="question_title">{{ item.question_info.question_title }}</span>
      <el-button v-if="reviewCorrect(item)" type="success" size="small" class="question_action"
        @click="submitReview(item)">提交复习</el-button>
      <el-button type="primary" size="small" class="question_action" @click="showAnalyze(item)">题目解析</el-button>
      <br /><br />
      <div v-if="item.question_info.question_type == 'single'">
        <el-radio-group v-model="item.user_review_answer" class="radio-group-vertical">
          <el-radio v-for="item in JSON.parse(item.question_info.question_items)" :key="item.prefix"
            :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' + item.content }}</el-radio>
        </el-radio-group>
      </div>
      <div v-if="item.question_info.question_type == 'multiple'">
        <el-checkbox-group v-model="item.user_review_answer" class="radio-group-vertical">
          <el-checkbox v-for="item in JSON.parse(item.question_info.question_items)" :key="item.prefix"
            :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' +
          item.content }}</el-checkbox>
        </el-checkbox-group>
      </div>
      <div v-if="item.question_info.question_type == 'judge'">
        <el-radio-group v-model="item.user_review_answer">
          <el-radio v-for="item in JSON.parse(item.question_info.question_items)" :key="item.prefix"
            :label="item.prefix">{{ item.prefix + '. ' + item.content }}</el-radio>
        </el-radio-group>
      </div>
      <div v-if="item.question_info.question_type == 'answer'">
        <el-input v-model="item.user_review_answer" type="textarea" :rows="5" placeholder="请输入答案" />
      </div>
      <div v-if="item.question_info.show_analyze">
        <div class="preview-analysis" v-if="item.question_info.analyze">
          <div class="analysis-title">题目解析：</div>
          <div>{{ item.question_info.analyze }}</div>
        </div>
        <div class="preview-correct" v-if="item.question_info.analyze">
          <div class="correct-title">正确答案：</div>
          <div>{{ item.question_info.correct }}</div>
        </div>
        <div class="preview-difficulty" v-if="item.question_info.difficult > 0">
          <div class="difficulty-title">题目难度：</div>
          <ElRate v-model="item.question_info.difficult" disabled text-color="#ff9900" score-template="{value}">
          </ElRate>
        </div>
      </div>
    </div>
    <!-- 分页功能 -->
    <div v-if="page.totalCount >= 1" class="pagination clearfix">
      <CommonPagination v-model:current-page="page.pageCurrent" v-model:page-size="page.pageSize"
        :total="page.totalCount" @pagination="handlePage" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import CommonPagination from '@/components/Common/Pagination.vue'

import { userApi } from '@/api/user'
import useTable from '@/utils/table'

const res = ref({})

onMounted(async () => {
})

function showAnalyze(item) {
  item.question_info.show_analyze = !item.question_info.show_analyze
}

function reviewCorrect(item) {
  let user_review_answer = item.user_review_answer
  if (item.question_info.question_type === 'multiple' && Array.isArray(user_review_answer)) {
    user_review_answer = user_review_answer.sort().join(',')
  }
  return user_review_answer == item.question_info.correct
}

async function submitReview(item) {
  await userApi.submitReview({ id: item.id })
  handleQuery()
}

// 分页查询
const { page, handlePage, query, handleQuery } = useTable(
  { page: userApi.ebbinghausSchedule },
  {}
)

watch(page, async (page) => {
  res.value = page.list[0]
});

</script>

<style lang="scss" scoped>
.ebbinghaus_schedule {
  text-align: center;
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
}


.exam-question-item {
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;

  .question_title {
    font-size: 16px;
    font-weight: bold;
  }

  .question_answer_right {
    color: green;
    font-size: 16;
    font-weight: bold;
    margin-left: 20px;
  }

  .question_answer_wrong {
    color: red;
    font-size: 16;
    font-weight: bold;
    margin-left: 20px;
  }

  .el-form-item__label {
    font-size: 15px !important;
  }
}

.question-title-padding {
  padding-left: 25px;
  padding-right: 25px;
}

.radio-group-vertical {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.radio-item-block {
  display: block;
}

.question_action {
  float: right;
  margin-right: 10px;
}

.preview-lesson {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px dashed #dcdfe6;
  font-size: 16px;
  font-weight: bold;
  color: green;
}

.preview-analysis {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px dashed #dcdfe6;
  color: #409eff;
}

.analysis-title {
  font-weight: bold;
  margin-bottom: 5px;
  color: #409eff;
}

.preview-correct {
  margin-top: 15px;
  display: flex;
  align-items: center;
  color: green;
}

.correct-title {
  font-weight: bold;
  margin-right: 10px;
  color: green;
}

.preview-difficulty {
  margin-top: 15px;
  display: flex;
  align-items: center;
}

.difficulty-title {
  font-weight: bold;
  margin-right: 10px;
}
</style>