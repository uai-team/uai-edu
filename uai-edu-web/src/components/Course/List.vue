<template>
  <!-- 暂没数据 -->
  <div v-if="props.list.length === 0" class="no-data">暂无数据</div>
  <el-row v-else class="zone_body" :gutter="20">
    <el-col v-for="(course, int) in props.list" :key="int" :span="6" class="zone_body_course">
      <router-link :to="{ path: '/course/detail', query: { id: course.id }  }">
        <img :src="course.course_cover" alt="" />
        <div class="course_name" v-html="course.course_name" />
        <div class="course_desc">
          <div class="collect">
            <Collect :course-id="course.id" />
          </div>
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
.zone_body {
  .zone_body_course {
    height: 255px;
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

      .course_name {
        font-size: 16px;
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

      .course_desc {
        display: flex;
        justify-content: end;
        align-items: center;

        .price_box {
          font-size: 16px;
          margin-top: 5px;
          margin-left: 10px;
          color: red;
        }

        .collect {
          margin-right: 8px;
          font-size: 12px;
        }
      }
    }
  }

  img {
    width: 285px;
    height: 158px;
    border-radius: 6px 6px 0 0;
  }
}
</style>
