<script setup lang="ts">
import { ElConfigProvider } from "element-plus";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import '@uai-team/uai-editor/dist/style.css'
</script>

<template>
  <el-config-provider :locale="zhCn">
    <router-view v-slot="{ Component }">
      <keep-alive :include="['layout']">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </el-config-provider>
</template>

<style scoped></style>
