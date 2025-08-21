import { ConfigEnv, defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

import { fileURLToPath, URL } from "node:url";

import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers"; // Element Plus 组件解析器

import { createSvgIconsPlugin } from "vite-plugin-svg-icons";
import path from "path";

// https://vite.dev/config/
export default defineConfig(({ command, mode }: ConfigEnv) => {
  let env = {} as any;
  const isBuild = command === "build";
  if (!isBuild) {
    env = loadEnv(
      process.argv[3] === "--mode" ? process.argv[4] : process.argv[3],
      process.cwd()
    );
  } else {
    env = loadEnv(mode, process.cwd());
  }
  return {
    css: {
      preprocessorOptions: {
        scss: {
          // 按需导入自定义主题
          additionalData: `@use "@/styles/themeVar.scss" as *;`,
        },
      },
    },
    define: {
      'process.env': process.env
    },
    plugins: [
      vue(),

      createSvgIconsPlugin({
        // Specify the icon folder to be cached
        iconDirs: [path.resolve(process.cwd(), "src/assets/svg")],
        // Specify symbolId format
        symbolId: "icon-[dir]-[name]",
      }),

      AutoImport({
        imports: ["vue", "vue-router"], // 自动导入 Vue 和 Vue Router 的 API

        eslintrc: {
          enabled: true, // 启用 ESLint 配置生成
          filepath: "./.eslintrc-auto-import.json", // 生成的 ESLint 配置文件路径
        },
        resolvers: [ElementPlusResolver()],
      }),

      Components({
        resolvers: [ElementPlusResolver({ importStyle: "sass" })],
      }),
    ],
    resolve: {
      alias: {
        // 将 '@' 别名映射到 'src' 目录，简化导入路径
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      port: 3000,
      proxy: {
        // 选项写法
        '/api': {
          target: 'http://127.0.0.1:9000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        },
        // 选项写法
        '/media': {
          target: 'http://127.0.0.1:9000',
          changeOrigin: true,
          rewrite: (path) => path
        }
      },
      hmr: {
        overlay: false
      },
      host: '0.0.0.0'
    },
  };
});
