<template>
  <div class="main" style="display: flex; flex-direction: row;">
    <div style="display: flex; flex:1; flex-direction: column;">
      <el-container class="app-item-contain">
        <el-header class="align-center">
          <h1>{{ form.paper_name }}</h1>
          <div>
            <span class="question-title-padding">试卷总分：{{ form.paper_score }} 分</span>
            <span class="question-title-padding">考试时间：{{ form.paper_time }} 分钟</span>
          </div>
        </el-header>
        <el-main>
          <el-form :model="form" label-width="100px">
            <div :key="index" v-for="(titleItem, index) in form.title_items">
              <h2>{{ titleItem.title_name }}</h2>
              <div v-for="questionItem in titleItem.question_items" class="exam-question-item"
                :id="'question-' + titleItem.order + '-' + questionItem.order">
                <span class="question_title">{{ questionItem.order }}. {{ questionItem.question_info.question_title
                  }} （{{ questionItem.score }}分）</span>
                <el-tag v-if="questionItem.user_correct" :type="success" class="question_answer_right">正确</el-tag>
                <el-tag v-else :type="danger" class="question_answer_wrong">错误</el-tag>
                <el-button v-if="!questionItem.user_correct" type="danger" size="small" class="question_action"
                  @click="addWrongQuestionBook(questionItem)">加入错题本</el-button>
                <br /><br />
                <div v-if="questionItem.question_info.question_type == 'single'">
                  <el-radio-group v-model="questionItem.user_answer" class="radio-group-vertical" disabled>
                    <el-radio v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
                      :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' + item.content }}</el-radio>
                  </el-radio-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'multiple'">
                  <el-checkbox-group v-model="questionItem.user_answer" class="radio-group-vertical" disabled>
                    <el-checkbox v-for="item in JSON.parse(questionItem.question_info.question_items)"
                      :key="item.prefix" :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' +
            item.content }}</el-checkbox>
                  </el-checkbox-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'judge'">
                  <el-radio-group v-model="questionItem.user_answer" disabled>
                    <el-radio v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
                      :label="item.prefix">{{ item.prefix + '. ' + item.content }}</el-radio>
                  </el-radio-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'answer'">
                  <el-input v-model="questionItem.user_answer" type="textarea" :rows="5" disabled />
                </div>
                <div class="preview-analysis" v-if="questionItem.question_info.analyze">
                  <div class="analysis-title">题目解析：</div>
                  <div>{{ questionItem.question_info.analyze }}</div>
                </div>
                <div class="preview-correct" v-if="questionItem.question_info.correct">
                  <div class="correct-title">正确答案：</div>
                  <div>{{ questionItem.question_info.correct }}</div>
                </div>
                <div class="preview-difficulty" v-if="questionItem.question_info.difficult > 0">
                  <div class="difficulty-title">题目难度：</div>
                  <ElRate v-model="questionItem.question_info.difficult" disabled text-color="#ff9900"
                    score-template="{value}"></ElRate>
                </div>
              </div>
            </div>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { userApi } from '@/api/user'

const route = useRoute()
const router = useRouter()

const form = ref({})

onMounted(async () => {
  form.value = await userApi.examAnswerDetail({ id: route.query.id })
  // 初始化多选题答案为空数组
  form.value.title_items?.forEach(titleItem => {
    titleItem.question_items?.forEach(questionItem => {
      if (questionItem.question_info.question_type === 'multiple') {
        if (!Array.isArray(questionItem.user_answer)) {
          questionItem.user_answer = questionItem.user_answer.split(",")
        }
      }
    })
  })
})

onUnmounted(() => {
})

async function addWrongQuestionBook(questionItem) {
  const res = await userApi.addWrongQuestionBook({ id: questionItem.user_answer_id })

  ElMessageBox.alert(`成功添加到我的错题本`, '提示', {
    confirmButtonText: '确定'
  })
}
</script>

<style lang="scss" scoped>
.align-center {
  height: 90px;
  text-align: center;
}

.do-exam-title {
  width: 300px;
  height: calc(100vh - 40px);
  padding: 10px;
  margin: 10px;
  border-radius: 10px;
  background-color: #fff;
}

.do-exam-title-tag {
  margin-left: 5px;
  cursor: pointer;
}

.do-exam-time {
  display: block;
  text-align: center;
  line-height: 2;
}

.do-align-center {
  text-align: center;
  margin-top: 20px;

  .el-form-item__content {
    margin-left: 0px !important;
  }
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

.el-main {
  overflow-y: auto;
  max-height: calc(100vh - 90px);
}

.question_action {
  float: right;
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
