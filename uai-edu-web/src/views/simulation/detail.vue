<template>
  <div class="detail_content">
    <div class="detail_body">
      <div class="detail_header clearfix">
        <div class="detail_title">
          <router-link :to="{ path: '/' }"> 首页 </router-link>
          <span>></span>
        </div>
        <div class="detail_title">
          <router-link :to="{ path: '/simulation/list' }"> 仿真中心 </router-link>
          <span>></span>
        </div>
        <div class="detail_title">
          {{ simulationInfo?.simulation_name }}
        </div>
      </div>
      <div class="clearfix">
        <div class="video_box">
          <img class="detail_view" :src="simulationInfo?.simulation_cover" :alt="simulationInfo?.simulation_name" />
          <div class="view_info">
            <!-- 仿真详情 -->
            <div class="view_info_simulation">
              {{ simulationInfo.simulation_name }}
            </div>
            <!-- <div v-if="simulationInfo.lecturerResp" class="view_info_item">
                <span class="text_b">讲师名称:</span>{{ simulationInfo.lecturerResp.lecturerName }}（{{ simulationInfo.lecturerResp.lecturerPosition }}）
              </div>
              <div class="view_info_item"><span class="text_b">学习人数:</span>{{ simulationInfo.countStudy }} 人</div>
               -->
            <div class="foot_box">
              <router-link :to="{ path: '/simulation/study', query: { id: route.query.id } }">
                <button class="buy_btn">开始学习</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="main">
    <!-- 仿真详情 -->
    <div class="simulation_info clearfix">
      <div class="layout_left">
        <el-tabs type="border-card" @tab-click="handleTabClick">
          <el-tab-pane label="仿真介绍">
            <div class="introduce" v-html="simulationInfo.simulation_desc" />
          </el-tab-pane>
          <el-tab-pane label="仿真评论" name="comment">
            <!-- <simulation-comment v-if="activeName === 'comment'" :simulation-id="simulationInfo.id" /> -->
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>
<script setup>
import { simulationApi } from '@/api/simulation'
const route = useRoute()

const simulationInfo = ref({})

onMounted(async () => {
  simulationInfo.value = await simulationApi.simulationDetail({ id: route.query.id })
})

const activeName = ref('')
function handleTabClick(tab) {
  activeName.value = tab.props.name
}
</script>
<style lang="scss" scoped>
.detail_content {
  background: #fff;
  color: #999;
  font-size: 14px;

  .detail_body {
    width: 1200px;
    margin: 0 auto;
    height: 373px;
  }

  .detail_header {
    .detail_title {
      float: left;
      line-height: 57px;
      margin: 0 5px;
      max-width: 600px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;

      span {
        margin-left: 10px;
      }
    }
  }

  .video_box {
    overflow: hidden;

    .detail_view {
      float: left;
      width: 504px;
      height: 280px;
      background-size: 100%;
      border-radius: 5px;

      &.float_win {
        position: fixed;
        right: 10px;
        bottom: 30px;
        z-index: 9999;
      }
    }

    .view_info {
      float: right;
      width: 650px;
      height: 270px;
      position: relative;

      .view_info_item {
        line-height: 30px;

        .text_b {
          margin-right: 20px;
        }
      }

      .view_price {
        background: #f5f5f5;
        color: rgb(102, 102, 102);
        padding: 15px 10px;
        margin: 10px 0;

        span {
          font-size: 20px;
          color: #d51423;
          font-weight: bold;
          margin-left: 20px;
        }
      }

      .view_info_simulation {
        font-size: 18px;
        margin: 5px 0;
        color: #333;
        height: 25px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .foot_box {
        position: absolute;
        bottom: 0px;
        width: 100%;
        height: 36px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .buy_btn {
        display: block;
        width: 136px;
        height: 36px;
        background: #2256f6;
        color: #fff;
        border: none;
        border-radius: 6px;
        line-height: 36px;
        text-align: center;
        font-size: 14px;

        &:hover {
          text-decoration: none;
          color: #fff;
          cursor: pointer;
        }
      }

      .handle_info_btn {
        display: flex;
        align-items: center;
        color: #999;
        font-size: 14px;
      }
    }
  }
}

.simulation_info {
  margin: 20px 0;
  overflow: hidden;

  .layout_left {
    width: 1200px;
    float: left;

    .introduce {
      font-size: 14px;
      line-height: 30px;
      color: #333;
      padding-left: 8px;
    }
  }
}
</style>
