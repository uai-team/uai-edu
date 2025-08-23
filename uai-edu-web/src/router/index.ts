import { createRouter, createWebHistory } from "vue-router";

const routes: any = [
  {
    path: "/",
    component: () => import("@/components/Layout/index.vue"),
    redirect: () => {
      return { path: "/home" };
    },
    children: [
      {
        path: "home",
        name: "Home",
        component: () => import("@/views/home/index.vue"),
      },
      {
        path: "login",
        name: "Login",
        component: () => import("@/views/home/login.vue"),
      },
      {
        path: "course/list",
        name: "CourseList",
        component: () => import("@/views/course/list.vue"),
      },
      {
        path: "course/detail",
        name: "CourseDetail",
        component: () => import("@/views/course/detail.vue"),
      },
      {
        path: "book/list",
        name: "BookList",
        component: () => import("@/views/book/list.vue"),
      },
      {
        path: "book/detail",
        name: "BookDetail",
        component: () => import("@/views/book/detail.vue"),
      },
      {
        path: "simulation/list",
        name: "SimulationList",
        component: () => import("@/views/simulation/list.vue"),
      },
      {
        path: "simulation/detail",
        name: "SimulationDetail",
        component: () => import("@/views/simulation/detail.vue"),
      },
      {
        path: "competition/list",
        name: "CompetitionList",
        component: () => import("@/views/competition/list.vue"),
      },
      {
        path: "labs/list",
        name: "LabsList",
        component: () => import("@/views/labs/list.vue"),
      },
      {
        path: "account/homework/list",
        name: "AccountHomeworkList",
        component: () => import("@/views/account/homework/list.vue"),
      },
      {
        path: "account/homework/do",
        name: "AccountHomeworkDo",
        component: () => import("@/views/account/homework/do.vue"),
      },
      {
        path: "account/exam/list",
        name: "AccountExamList",
        component: () => import("@/views/account/exam/list.vue"),
      },
      {
        path: "account/exam/records",
        name: "AccountExamRecordsList",
        component: () => import("@/views/account/exam/records.vue"),
      },
      {
        path: "account/exam/view",
        name: "AccountExamRecordView",
        component: () => import("@/views/account/exam/view.vue"),
      },
      {
        path: "account/wrong/list",
        name: "AccountWrongList",
        component: () => import("@/views/account/wrong/list.vue"),
      },
      {
        path: "account/wrong/ebbinghaus",
        name: "AccountWrongEbbinghaus",
        component: () => import("@/views/account/wrong/ebbinghaus.vue"),
      },
    ],
  },
  {
    path: "/course/study",
    name: "CourseStudy",
    component: () => import("@/views/course/study.vue"),
  },
  {
    path: "/book/study",
    name: "BookStudy",
    component: () => import("@/views/book/study.vue"),
  },
  {
    path: "/simulation/study",
    name: "SimulationStudy",
    component: () => import("@/views/simulation/study.vue"),
  },
  {
    path: "/labs/story",
    name: "LabsStory",
    component: () => import("@/views/labs/story.vue"),
  },
  {
    path: "/labs/accompany",
    name: "LabsAccompany",
    component: () => import("@/views/labs/accompany.vue"),
  },
  {
    path: "/labs/writing",
    name: "LabsWriting",
    component: () => import("@/views/labs/writing.vue"),
  },
  {
    path: "/labs/music",
    name: "LabsMusic",
    component: () => import("@/views/labs/music.vue"),
  },
  {
    path: "/labs/solving",
    name: "LabsSolving",
    component: () => import("@/views/labs/solving.vue"),
  },
  {
    path: "/labs/photoshop",
    name: "LabsPhotoshop",
    component: () => import("@/views/labs/photoshop.vue"),
  },
  {
    path: "/labs/tryon",
    name: "LabsTryon",
    component: () => import("@/views/labs/tryon.vue"),
  },
  {
    path: "/labs/composing",
    name: "LabsComposing",
    component: () => import("@/views/labs/composing.vue"),
  },
  {
    path: "/labs/arxiv",
    name: "LabsArxiv",
    component: () => import("@/views/labs/arxiv.vue"),
  },
  {
    path: "/account/exam/do",
    name: "AccountExamDo",
    component: () => import("@/views/account/exam/do.vue"),
  },
  // {
  //   path: "/home",
  //   name: "Home",
  //   component: () => import("@/views/home/index.vue"),
  // },
  // {
  //   path: "/",
  //   component: () => import("@/components/layout/index.vue"),
  //   children: [
  //     {
  //       path: "home",
  //       name: "Home",
  //       component: () => import("@/views/home/index.vue"),
  //     },
  //   ],
  // },
  // {
  //   path: "/",
  //   component: () => import("@/components/layout/index.vue"),
  //   children: [
  //     {
  //       path: "home",
  //       name: "Home",
  //       component: () => import("@/views/home/index.vue"),
  //     },
  //     {
  //       path: "course",
  //       name: "Course",
  //       component: () => import("@/views/course/index.vue"),
  //     },
  //     {
  //       path: "tool",
  //       name: "Tool",
  //       component: () => import("@/views/tool/index.vue"),
  //     },
  //   ],
  // },
  // {
  //   path: "/study",
  //   name: "Study",
  //   component: () => import("@/views/course/study.vue"),
  // },
  // {
  //   path: "/story",
  //   name: "Story",
  //   component: () => import("@/views/course/story.vue"),
  // },
  // {
  //   path: "/arxiv",
  //   name: "Arxiv",
  //   component: () => import("@/views/tool/arxiv.vue"),
  // },
  // {
  //   path: "/exam",
  //   name: "Exam",
  //   component: () => import("@/views/tool/exam.vue"),
  // },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 始终滚动到顶部
    return { top: 0 };
  },
});

export default router;
