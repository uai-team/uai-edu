<template>
  <div class="main competition-list">
    <!-- 选择分类 -->
    <CategoryChoose v-for="(category, index) in categoryList" :key="index" :menu="category" :index="index"
      @change="handleChange" />

    <!-- 结果列表 -->
    <!-- <CompetitionList v-loading="page.loading" :list="page.list" /> -->

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
  const res = await categoryApi.categoryList({ category_type: "competition" })
  categoryRes = res
  selectCategory = []
}

// 分页查询
const { page, handlePage, query, handleQuery } = useTable(
  // { page: competitionApi.competitionList },
  { page: () => { return { totalCount: 500, pageCurrent: 1, pageSize: 10, list: [] } } },
  { categoryId: route.query.categoryId }
)
</script>
<style lang="scss" scoped>
.competition-list {
  padding: 10px 0;
}
</style>