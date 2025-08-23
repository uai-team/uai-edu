<!-- 轮播图上的分类 -->
<template>
  <div v-if="list.length" class="class_block" @mouseleave="hideWidth">
    <div :class="{ left_block: true, show_scroll: list.length > 10 }">
      <div v-for="(item, index) in list" :key="index" :class="{ active: item.id == categoryId }"
        :style="list.length >= 5 && list.length <= 10 && 'line-height:' + (height - 10) / list.length + 'px;'"
        @mouseenter="changeWidth(item)">
        <router-link :to="{ path: '/course/list', query: { categoryId: item.id } }">
          {{ item.category_name }}
        </router-link>
        <span class="arrow" />
      </div>
    </div>
    <div class="big_block clearfix" :style="'width:' + width + 'px;'">
      <div class="list_items fl clearfix">
        <div v-for="(item1, index1) in twoList" :key="index1" class="list_item clearfix">
          <router-link :to="{ path: '/course/list', query: { categoryId: item1.id } }">
            {{ item1.category_name }}
          </router-link>
          <div class="fl three_box">
            <router-link v-for="(item2, index2) in item1.children" :key="index2"
            :to="{ path: '/course/list', query: { categoryId: item2.id } }" class="three_link">
              {{ item2.category_name }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { indexApi } from '@/api/index'

// 分类
const list = ref([])
const twoList = ref([])
const categoryId = ref('')
const width = ref(0)
const height = ref(360)

onMounted(async () => {
  list.value = (await indexApi.categoryList({ category_type: "course" })).slice(0, 7)
})

function changeWidth(item) {
  width.value = 400
  categoryId.value = item.id
  twoList.value = item.children.slice(0, 6)
}
function hideWidth() {
  width.value = 0
  categoryId.value = ''
}
</script>
<style lang="scss" scoped>
.class_block {
  position: absolute;
  height: 100%;
  top: 0;
  left: 50%;
  z-index: 20;
  margin-left: -600px;
}

.left_block {
  padding: 5px 0;
  border-radius: 10px 0 0 10px;
  width: 200px;
  height: calc(100% - 10px);
  font-size: 14px;
  background: #39364d;

  &.show_scroll {
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 4px;
      background: rgba(245, 245, 245, 0.4);
    }
  }

  .arrow {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-top: 1px solid #ccc;
    border-right: 1px solid #ccc;
    transform: rotate(45deg);
    position: absolute;
    right: 20px;
    top: 50%;
    margin-top: -3px;
  }

  div {
    padding: 0 20px;
    position: relative;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;

    &.active {
      background: rgba(255, 255, 255, 0.9);
      border-radius: 10px 0 0 10px;
      margin: 0 8px;

      a {
        color: #d51423;
      }

      .arrow {
        border-color: #d51423;
      }
    }
  }

  a {
    color: #fff;
    display: block;

    &:hover {
      color: #d51423;
    }
  }
}

.big_block {
  position: absolute;
  top: 0;
  left: 50%;
  height: 100%;
  margin-left: 90px;
  background: #fff;
  transition: width 0.1s;
  overflow: hidden;
  box-shadow: 1px 0px 1px rgba(0, 0, 0, 0.1);
}

.list_items {
  height: 100%;
  width: 400px;
  padding: 0 30px;
  overflow-y: auto;
  overflow-x: hidden;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background: rgba(210, 210, 210, 0.4);
  }
}

.list_item {
  padding-top: 20px;
  position: relative;
  line-height: 20px;

  .class_header {
    padding-right: 20px;
    background: #fff;
    font-size: 14px;
    font-weight: 700;
    line-height: 30px;

    &.has_three {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      width: 60px;
    }
  }

  .three_box {
    width: 400px;
  }

  .three_link {
    font-size: 14px;
    color: #999;
    display: inline-block;
    margin-right: 20px;

    &:hover {
      color: #d51423;
    }
  }
}

.foot_courses {
  padding: 0px 30px;
  height: 100%;
  width: 400px;
  background: rgba(247, 245, 248, 1);
  overflow-y: auto;
  overflow-x: hidden;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.1);
  }

  .courses_top {
    font-size: 14px;
    font-weight: 700;
    padding: 20px 0px;
  }

  .foot_course {
    width: 220px;
    position: relative;
    margin-bottom: 20px;
  }

  .inline_box {
    display: inline-block;
    height: 43px;
  }

  .img_box {
    width: 110px;
    height: 63px;

    img {
      width: 100%;
      height: 100%;
      border-radius: 3px;
    }
  }

  .course_info {
    font-size: 14px;
    margin-left: 8px;
  }

  .course_name {
    position: absolute;
    width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #333;
    top: 0;

    &:hover {
      text-decoration: none;
      color: #d51423;
    }
  }

  .course_price {
    position: absolute;
    color: #999;
    bottom: 2px;
  }
}

a {
  &:hover {
    color: #d51423;
    text-decoration: none;
  }
}
</style>
