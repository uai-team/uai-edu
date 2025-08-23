<template>
  <div class="main homework_list">
    <div style="text-align: center;">
      <h1>{{ homework.homework_name }}</h1>
    </div>
    <div :key="index" v-for="(item, index) in homework.items" class="homework_item">
      <el-tag type="success">{{ item.item_type }}</el-tag> &nbsp;
      <span class="homework_title">{{ item.resource_name }}</span>
      <el-button type="success" size="small" class="homework_action" @click="doHomework(item)">去完成</el-button>
    </div>
  </div>
</template>
<script setup>
import { userApi } from '@/api/user'

const router = useRouter()
const route = useRoute()

const homework = ref({})

onMounted(async () => {
  homework.value = await userApi.homeworkDetail({ id: route.query.id })
  console.log(homework.value)
})

function doHomework(item) {
  if (item.item_type === 'course') {
    router.push({ path: '/course/study', query: { id: item.course_id, lessonId: item.resource_id } })
  }
  if (item.item_type === 'book') {
    router.push({ path: '/book/study', query: { id: item.resource_id } })
  }
  if (item.item_type === 'exam') {
    router.push({ path: '/account/exam/do', query: { id: item.resource_id } })
  }
}

</script>
<style lang="scss" scoped>
.homework_list {
  padding: 10px 0;
}

.homework_item {
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;

  .homework_title {
    font-size: 16px;
    font-weight: bold;
  }

  .el-form-item__label {
    font-size: 15px !important;
  }
}

.homework_action {
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
</style>