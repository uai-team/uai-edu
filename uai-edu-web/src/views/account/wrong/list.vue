<template>
  <div class="main wrong-list">
    <!-- 选择分类 -->
    <CategoryChoose v-for="(category, index) in categoryList" :key="index" :menu="category" :index="index"
      @change="handleChange" />

    <div :key="index" v-for="(questionItem, index) in page.list" class="exam-question-item">
      <span class="question_title">{{ questionItem.question_info.question_title }}</span>
      <el-button v-if="!questionItem.user_correct" type="danger" size="small" class="question_action"
        @click="removeWrongQuestionBook(questionItem)">移出错题本</el-button>
      <br /><br />
      <div v-if="questionItem.question_info.question_type == 'single'">
        <el-radio-group v-model="questionItem.user_answer" class="radio-group-vertical" disabled>
          <el-radio v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
            :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' + item.content }}</el-radio>
        </el-radio-group>
      </div>
      <div v-if="questionItem.question_info.question_type == 'multiple'">
        <el-checkbox-group v-model="questionItem.user_answer" class="radio-group-vertical" disabled>
          <el-checkbox v-for="item in JSON.parse(questionItem.question_info.question_items)" :key="item.prefix"
            :label="item.prefix" class="radio-item-block">{{ item.prefix + '. ' +
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
      <div class="preview-lesson">关联课程：{{ questionItem.lesson_name }}
        <el-button v-if="!questionItem.user_correct" type="success" size="small" class="question_action"
          @click="studyLesson(questionItem)">课程学习</el-button>
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
        <ElRate v-model="questionItem.question_info.difficult" disabled text-color="#ff9900" score-template="{value}">
        </ElRate>
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
import CategoryChoose from '@/components/Category/Choose.vue'
import CommonPagination from '@/components/Common/Pagination.vue'

import { categoryApi } from '@/api/category'
import { userApi } from '@/api/user'
import useTable from '@/utils/table'

const router = useRouter()
const route = useRoute()

// 分类查询
const categoryList = ref([])
let selectCategory = []

onMounted(async () => {
  // 分类列表
  await getCategoryList()
  // 初始化分类
  initCategory()
})

const initCategory = () => {
  if (route.query.categoryId) {
    const classifyIdObj = {}
    const key = []
    const init = (children, prefixId) => {
      children.forEach((e) => {
        if (e.id) {
          const id = prefixId ? prefixId + '_' + e.id : `${e.id}`
          key.push(id)
          classifyIdObj[e.id] = e
          if (e.children && e.children.length) {
            return init(e.children, id)
          }
        }
      })
    }
    init(categoryRes, '')
    const lists = key.filter((e) => e.indexOf(route.query.categoryId) > -1)
    if (lists && lists.length) {
      lists.sort((a, b) => {
        return a.length - b.length
      })
      const ids = lists[0].split('_')
      if (ids && ids.length) {
        categoryList.value.push({
          active: ids[0],
          children: [{ id: '', category_name: '全部' }].concat(categoryRes)
        })
        ids.forEach((id, index) => {
          const item = classifyIdObj[id]
          if (item) {
            selectCategory.push(id)
            if (item.children.length) {
              categoryList.value.push({
                active: ids[index + 1] || id,
                children: [{ id: id, category_name: '全部' }].concat(item.children)
              })
            }
          }
        })
      }
    }
  } else {
    categoryList.value.push({
      active: '',
      children: [{ id: '', category_name: '全部' }].concat(categoryRes)
    })
  }
}

// 分类处理
const handleChange = (index, row) => {
  if (selectCategory[index] !== `${row.id}`) {
    selectCategory[index] = `${row.id}`
    if (row.children && row.children.length) {
      if (categoryList.value.length > index + 1) {
        categoryList.value.length = index + 1
      }
      categoryList.value.push({
        active: `${row.id}`,
        children: [{ id: `${row.id}`, category_name: '全部' }].concat(row.children)
      })
    } else {
      categoryList.value.length = index + 1
      selectCategory.length = index + 1
    }
  }
  const queryObj = Object.assign({ ...(route.query || {}) }, { categoryId: selectCategory[index] || '' })
  if (!queryObj.categoryId) {
    delete queryObj.categoryId
  }
  router.push({ query: queryObj })
  query.categoryId = queryObj.categoryId
  handleQuery()
}

// 分类查询
let categoryRes = []
const getCategoryList = async () => {
  const res = await categoryApi.categoryList({ category_type: "course" })
  categoryRes = res
  selectCategory = []
}

// 分页查询
const { page, handlePage, query, handleQuery } = useTable(
  { page: userApi.wrongQuestionList },
  { categoryId: route.query.categoryId }
)

watch(page, async (page) => {
  page.list.forEach(questionItem => {
    if (questionItem.question_info.question_type === 'multiple') {
      if (!Array.isArray(questionItem.user_answer)) {
        questionItem.user_answer = questionItem.user_answer.split(",")
      }
    }
  })
});

async function removeWrongQuestionBook(questionItem) {
  const res = await userApi.removeWrongQuestionBook({ id: questionItem.id })

  ElMessageBox.alert(`成功从我的错题本移除`, '提示', {
    confirmButtonText: '确定',
    callback: () => {
      handleQuery()
    }
  })
}

function studyLesson(questionItem) {
  router.push({ path: '/course/study', query: { id: questionItem.course_id, lessonId: questionItem.lesson_id } })
}

</script>
<style lang="scss" scoped>
.wrong-list {
  padding: 10px 0;
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