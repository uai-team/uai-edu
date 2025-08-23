<template>
  <div v-for="(item, index) in zoneData" :key="index" class="i_content">
    <div class="i_zone">
      <div class="zone_header">
        <div class="big_text">
          <span class="col_block" />
          {{ item.zone_name }}
          <span class="small_text">{{ item.zone_desc }}</span>
          <router-link to="course/list" class="fr small_text link_text"> 更多课程 > </router-link>
        </div>
      </div>
      <CourseList :list="item.courses" />
    </div>
  </div>
</template>
<script setup>
import CourseList from '@/components/Course/List.vue'
import { indexApi } from '@/api/index'

const zoneData = ref()
onMounted(async () => {
  zoneData.value = await indexApi.zoneList({})
})
</script>
<style lang="scss" scoped>
.i_content {
  width: 1200px;
  margin: 0 0 30px 0;
  background: #f6f8fb;

  .i_zone {
    margin-top: 30px;

    .zone_header {
      .col_block {
        display: inline-block;
        width: 4px;
        height: 24px;
        background: blue;
        position: relative;
        top: 4px;
      }

      .big_text {
        font-size: 24px;
      }

      .small_text {
        font-size: 14px;
        color: #999;
        margin-top: 10px;
      }

      .link_text:hover {
        text-decoration: none;
        color: #333;
      }
    }
  }
}
</style>
