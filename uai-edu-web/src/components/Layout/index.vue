<template>
  <div class="flex flex-col h-full">
    <div class="flex flex-col">
      <Navigation />
    </div>
    <!-- <div class="flex-1">
      <router-view></router-view>
    </div> -->
    <el-main>
      <router-view></router-view>
      <Footer />
    </el-main>
    <Affix />
  </div>

</template>
<script setup lang="ts">
// import { ref, watch, onMounted } from "vue";
// import { GuideProps, ButtonProps } from 'tdesign-vue-next';

// import { settingsStore } from '@/store/settings';

// const settings = settingsStore();

// const visible = ref(false);
// const current = ref(-1);
// const guide_steps = [
//   {
//     element: '.guide_step1',
//     title: '查看系统功能演示',
//     body: '请先通过这里查看系统功能演示，了解系统的使用方法，这里有比较详细的功能演示视频。',
//     placement: 'bottom-right',
//   },
//   {
//     element: '.guide_step2',
//     title: '新标签页打开系统',
//     body: '尽管我设置了我的应用是全屏，但我发现右侧的滚动条并未出现，并且超出屏幕的部分被隐藏了。可以在新标签页打开系统，这样就可以看到右侧的滚动条和页面的全部内容了。',
//     placement: 'bottom',
//   },
//   {
//     element: '.guide_step3',
//     title: '在线课程分类',
//     body: '这里是在线课程分类列表，可以选择课程分类，下面会列出当前分类下的部分课程。',
//     placement: 'right',
//   },
//   {
//     element: '.guide_step4',
//     title: '在线课程列表',
//     body: '点击课程可以进入课程学习页面，进行课程学习。',
//     placement: 'right',
//   },
//   {
//     element: '.guide_step5',
//     title: '热门工具分类',
//     body: '这里是热门工具分类列表，可以选择工具分类，下面会列出当前分类下的部分工具。',
//     placement: 'right',
//   },
//   {
//     element: '.guide_step6',
//     title: '热门工具列表',
//     body: '点击工具可以进入工具使用页面，进行工具使用。',
//     placement: 'right',
//   },
// ];

// const handleChange: GuideProps['onChange'] = () => {
// };
// const handlePrevStepClick: GuideProps['onPrevStepClick'] = () => {
// };
// const handleNextStepClick: GuideProps['onNextStepClick'] = () => {
// };
// const handleFinish: GuideProps['onFinish'] = () => {
//   visible.value = false;
//   settings.showGuide = false;
// };
// const handleSkip: GuideProps['onSkip'] = () => {
//   visible.value = false;
//   settings.showGuide = false;
// };
// onMounted(() => {
//   if (settings.showGuide) {
//     visible.value = true;
//     setTimeout(() => {
//       current.value = 0;
//     }, 800);
//   }
// });

</script>

<style lang="scss" scoped>
.el-main {
  padding: 0;
  overflow: auto;
  margin: 70px auto 0;
  height: calc(100vh - 70px);
}
</style>
