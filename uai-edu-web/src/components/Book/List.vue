<template>
  <!-- 暂没数据 -->
  <div v-if="props.list.length === 0" class="no-data">暂无数据</div>
  <el-row v-else class="book_body" :gutter="20">
    <el-col v-for="(book, int) in props.list" :key="int" :span="12" class="book_body_item">
      <router-link :to="{ path: '/book/detail', query: { id: book.id } }" style="display: flex;">
        <img :src="book.book_cover" alt="" />
        <div style="display: flex; flex-direction: column;">
        <div class="book_name" v-html="book.book_name" />
        <div class="book_desc">{{ book.book_desc }}</div>
        </div>
      </router-link>
    </el-col>
  </el-row>
</template>
<script setup>
const props = defineProps({
  list: {
    type: Array,
    default: () => []
  }
})
</script>
<style lang="scss" scoped>
.book_body {
  .book_body_item {
    height: 196px;
    border-radius: 6px;
    margin: 10px 0;

    &:hover {
      box-shadow: 0px 0px 0px rgba(0, 0, 0, 0.2);
      transform: translateY(-2px);
      transition: all 0.3s;
    }

    a {
      display: block;
      width: 100%;
      height: 100%;
      position: relative;
      background: #fff;
      border-radius: 6px;

      &:hover {
        color: #000;
        text-decoration: none;
      }

      .book_name {
        font-size: 18px;
        margin-top: 5px;
        padding-left: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-height: 25px;
        height: 30px;
      }

      .book_desc {
        // display: flex;
        padding: 10px;
        justify-content: end;
        // align-items: center;
        text-align: left;
        font-size: 14px;
        color: #999;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
  }

  img {
    width: 139px;
    height: 196px;
    border-radius: 6px 0 0 6px;
  }
}
</style>
