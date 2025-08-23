<template>
  <div style="display: flex; flex-direction: row;">
    <div class="do-exam-title">
      <div :key="index" v-for="(titleItem, index) in form.title_items">
        <h3>{{ titleItem.title_name }}</h3>
        <span :key="'tag-' + titleItem.order + '-' + questionItem.order"
          v-for="questionItem in titleItem.question_items"
          @click="scrollToQuestion(titleItem.order, questionItem.order)">
          <el-tag :type="isAnswered(questionItem) ? 'success' : 'info'" class="do-exam-title-tag">{{ questionItem.order
            }}</el-tag>
        </span>
      </div>
      <hr />
      <span class="do-exam-time">
        <span style="font-size: 18px;">剩余时间</span>
        <br />
        <span style="font-size: 20px; font-weight: bold; color: red;">{{ formatTime(remainTime) }}</span>
      </span>
      <hr />
      <div class="do-align-center">
        <el-button type="primary" @click="submitForm">提交试卷</el-button>
      </div>
    </div>
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
                <br /><br />
                <div v-if="questionItem.question_info.question_type == 'single'">
                  <el-radio-group v-model="questionItem.user_answer" class="radio-group-vertical">
                    <el-radio v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
                      :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' + item.content }}</el-radio>
                  </el-radio-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'multiple'">
                  <el-checkbox-group v-model="questionItem.user_answer" class="radio-group-vertical">
                    <el-checkbox v-for="item in JSON.parse(questionItem.question_info.question_items)"
                      :key="item.prefix" :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' +
        item.content }}</el-checkbox>
                  </el-checkbox-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'judge'">
                  <el-radio-group v-model="questionItem.user_answer">
                    <el-radio v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
                      :label="item.prefix">{{ item.prefix + '. ' + item.content }}</el-radio>
                  </el-radio-group>
                </div>
                <div v-if="questionItem.question_info.question_type == 'answer'">
                  <el-input v-model="questionItem.user_answer" type="textarea" :rows="5" placeholder="请输入答案" />
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
const remainTime = ref(0)
let timer = null

onMounted(async () => {
  form.value = await userApi.examPaperDetail({ id: route.query.id })
  // 初始化多选题答案为空数组
  form.value.title_items?.forEach(titleItem => {
    titleItem.question_items?.forEach(questionItem => {
      if (questionItem.question_info.question_type === 'multiple') {
        if (!Array.isArray(questionItem.user_answer)) {
          questionItem.user_answer = []
        }
      } else {
        questionItem.user_answer = ""
      }
    })
  })

  remainTime.value = form.value.paper_time * 60
  startTimer()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})

function isAnswered(questionItem) {
  const answer = questionItem.user_answer
  if (Array.isArray(answer)) {
    return answer.length > 0
  }
  return answer !== undefined && answer !== null && answer !== ''
}

function scrollToQuestion(titleOrder, questionOrder) {
  const element = document.getElementById(`question-${titleOrder}-${questionOrder}`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function startTimer() {
  timer = setInterval(() => {
    if (remainTime.value > 0) {
      remainTime.value--
    } else {
      clearInterval(timer)
      submitForm()
    }
  }, 1000)
}

function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours.toString().padStart(2, '0')}时${minutes.toString().padStart(2, '0')}分${secs.toString().padStart(2, '0')}秒`
}

async function submitForm() {
  if (timer) {
    clearInterval(timer)
  }
  // 对多选题答案进行排序处理
  form.value.title_items?.forEach(titleItem => {
    titleItem.question_items?.forEach(questionItem => {
      if (questionItem.question_info.question_type === 'multiple' && Array.isArray(questionItem.user_answer)) {
        questionItem.user_answer = questionItem.user_answer.sort().join(',')
      }
    })
  })
  const res = await userApi.examDoSubmit(form.value)

  ElMessageBox.alert(`考试完成，考试成绩 ${res.score} 分`, '提示', {
    confirmButtonText: '确定',
    callback: () => { router.push('/account/exam/list') }
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
</style>
