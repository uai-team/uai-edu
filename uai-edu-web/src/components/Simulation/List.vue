<template>
  <!-- 暂没数据 -->
  <div v-if="props.list.length === 0" class="no-data">暂无数据</div>
  <el-row v-else class="simulation_body" :gutter="20">
    <el-col v-for="(simulation, int) in props.list" :key="int" :span="6" class="simulation_body_item">
      <router-link :to="{ path: '/simulation/detail', query: { id: simulation.id } }">
        <img :src="simulation.simulation_cover" alt="" />
        <div class="simulation_name" v-html="simulation.simulation_name" />
        <div class="simulation_desc">{{ simulation.simulation_desc }}</div>
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
.simulation_body {
  .simulation_body_item {
    height: 290px;
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

      .simulation_name {
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

      .simulation_desc {
        display: flex;
        padding: 5px;
        justify-content: end;
        align-items: center;
        font-size: 14px;
        color: #999;
        overflow: hidden;
        text-overflow: ellipsis;
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
