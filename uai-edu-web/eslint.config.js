const globals = require("globals");
const pluginJs = require("@eslint/js");
const tseslint = require("typescript-eslint");
const pluginVue = require("eslint-plugin-vue");
const autoImportGlobals = require("./.eslintrc-auto-import.json"); // 使用 require 导入 JSON
const prettierPlugin = require("eslint-plugin-prettier");
const prettierConfig = require("eslint-config-prettier");
 
module.exports = [
  // 应用于所有文件的基础配置
  {
    files: ["**/*.{js,ts,html,vue}"],
 
    languageOptions: {
      globals: {
        ...globals.browser,
        ...autoImportGlobals.globals // 将自动导入的全局变量合并到 ESLint 配置中
      }
    }
  },
 
  // 使用 JavaScript 推荐配置
  pluginJs.configs.recommended,
 
  // 使用 TypeScript 推荐配置
  ...tseslint.configs.recommended,
 
  // 使用 Vue.js 推荐的基础配置
  ...pluginVue.configs["flat/essential"],
 
  // 使用 prettier 规范
  prettierConfig, // 这是 eslint-config-prettier, 禁用与 Prettier 冲突的 ESLint 规则
 
  // 针对 Vue 文件的特殊处理
  {
    files: ["**/*.vue"], // 只应用于 .vue 文件
    languageOptions: {
      parserOptions: {
        ecmaVersion: 2020, // 或更高版本
        sourceType: "module", // 允许使用 ES 模块
        parser: tseslint.parser // 使用 TypeScript 解析器解析 Vue 文件中的脚本部分
      }
    }
  },
 
  // 自定义 ESLint 规则
  {
    plugins: {
      prettier: prettierPlugin // 使用 Prettier 插件，直接作为对象引用
    },
    rules: {
      "no-debugger": "off",
      "prettier/prettier": "error", // 强制使用 Prettier 格式化，并将不符合 Prettier 规范的代码作为错误
      "prefer-const": "off", // 允许使用 let 声明变量，而不强制使用 const 声明常量
      "vue/no-setup-props-destructure": "off", // 允许在 setup 中对 props 进行解构
      "vue/script-setup-uses-vars": "error", // 强制检查 script setup 中使用的变量，防止未使用变量的警告
      "vue/no-reserved-component-names": "off", // 允许使用 Vue 保留的组件名称
      "@typescript-eslint/ban-ts-ignore": "off", // 允许使用 @ts-ignore 注释，忽略 TypeScript 错误
      "@typescript-eslint/explicit-function-return-type": "off", // 不强制要求函数返回类型的明确声明
      "@typescript-eslint/no-explicit-any": "off", // 允许使用 any 类型
      "@typescript-eslint/no-var-requires": "off", // 允许使用 require 来导入模块，支持 CommonJS
      "@typescript-eslint/no-empty-function": "off", // 允许空函数声明
      "vue/custom-event-name-casing": "off", // 允许自定义事件名称使用任意大小写
      "no-use-before-define": "off", // 允许在变量声明之前使用它们
      "@typescript-eslint/no-use-before-define": "off", // 允许在变量声明之前使用 TypeScript 的变量
      "@typescript-eslint/ban-ts-comment": "off", // 允许使用 @ts- 开头的注释
      "@typescript-eslint/ban-types": "off", // 允许使用基本类型，禁止使用特定的类型
      "@typescript-eslint/no-non-null-assertion": "off", // 允许使用非空断言操作符（!）
      "@typescript-eslint/explicit-module-boundary-types": "off", // 不强制要求模块边界类型的明确声明
      "@typescript-eslint/no-unused-vars": "off", // 允许未使用的变量
      "no-unused-vars": "off", // 允许未使用的变量（在 JavaScript 中）
      "space-before-function-paren": "off", // 不强制要求函数括号前的空格
      "vue/attributes-order": "off", // 不强制要求 Vue 组件属性的顺序
      "vue/one-component-per-file": "off", // 允许在一个文件中定义多个 Vue 组件
      "vue/html-closing-bracket-newline": "off", // 不强制要求 HTML 标签的闭合括号换行
      "vue/max-attributes-per-line": "off", // 不强制要求每行最大属性数量
      "vue/multiline-html-element-content-newline": "off", // 不强制要求多行 HTML 元素内容换行
      "vue/singleline-html-element-content-newline": "off", // 不强制要求单行 HTML 元素内容换行
      "vue/attribute-hyphenation": "off", // 允许属性命名不使用连字符
      "vue/require-default-prop": "off", // 允许不定义组件的默认属性
      "vue/require-explicit-emits": "off", // 允许不显式声明组件 emit 的事件
      "vue/html-self-closing": [
        "error", // 强制 HTML 自闭合标签格式
        {
          html: {
            void: "always", // 对于 void 标签（如 <br>），总是使用自闭合
            normal: "never", // 对于正常标签（如 <div>），不使用自闭合
            component: "always" // 对于组件标签（如 <MyComponent>），总是使用自闭合
          },
          svg: "always", // 对于 SVG 标签，总是使用自闭合
          math: "always" // 对于 MathML 标签，总是使用自闭合
        }
      ],
      "vue/multi-word-component-names": "off", // 允许组件名称不使用多词
      "vue/no-v-html": "off", // 允许使用 v-html 指令（不推荐用于安全性考虑）
      "vue/require-toggle-inside-transition": "off" // 允许不在过渡组件中使用 toggle
    }
  }
];