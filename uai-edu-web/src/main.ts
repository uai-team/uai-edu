import { createApp } from "vue";
import App from "./App.vue";
import "./styles/main.scss";
import "virtual:svg-icons-register";
import { createPinia } from "pinia";
import router from "@/router/index.ts";
import TDesign from 'tdesign-vue-next';
import TDesignChat from '@tdesign-vue-next/chat';

createApp(App).use(router).use(createPinia()).use(TDesign).use(TDesignChat).mount("#app");
