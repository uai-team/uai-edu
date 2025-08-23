<template>
  <div class="affix">
    <el-affix class="affix-info">
      <el-popover placement="left">
        <template #reference>
          <div class="icon">
            <img src="@/assets/svg/gzh.svg" width="30" alt="" />
            <div>公众号</div>
          </div>
        </template>
        <template #default>
          <img style="width: 126px" src="@/assets/images/gzh.jpg" alt="" />
          <div style="font-size: 10px; text-align: center">扫码关注微信公众号</div>
        </template>
      </el-popover>
    </el-affix>
    <el-affix class="affix-info">
      <el-popover placement="left">
        <template #reference>
          <div class="icon" @click="openEdit">
            <img src="@/assets/svg/edit.svg" width="30" alt="" />
            <div>笔记本</div>
          </div>
        </template>
        <template #default>
          <div style="font-size: 10px; text-align: center">点击记录笔记</div>
        </template>
      </el-popover>
    </el-affix>
    <el-affix class="affix-info">
      <el-popover placement="left">
        <template #reference>
          <div class="icon" @click="openAvatar">
            <img src="@/assets/svg/avatar.svg" width="30" alt="" />
            <div>数字人{{ props.contentRetentionKey }}</div>
          </div>
        </template>
        <template #default>
          <div style="font-size: 10px; text-align: center">启动数字教师</div>
        </template>
      </el-popover>
    </el-affix>
  </div>
  <div>
    <t-drawer v-model:visible="editorVisible" placement="left" :show-overlay="false" :close-btn="true" :footer="false"
      size="50%" :size-draggable="true" header="有爱智能文档笔记">
      <div ref="affixEditorDiv" id="affixEditorDiv" style="height: 100%; background-color: aqua;"></div>
    </t-drawer>
    <t-drawer v-model:visible="avatarVisible" :show-overlay="false" :close-btn="true" :footer="false" size="50%"
      :size-draggable="true" destroy-on-close header="有爱智能数字教师">
      <iframe src="https://open-avatar.holoworld.com.cn:8282/" width="100%" height="99%" frameborder="0" scrolling="no"
        allow="microphone; camera" sandbox="allow-scripts allow-same-origin allow-forms">
      </iframe>
    </t-drawer>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, toRefs, watch } from 'vue';

import { UAIEditor } from "@uai-team/uai-editor"

// 动态导入 UAIEditor
// let UAIEditor = null

const props = defineProps({
  contentRetentionKey: {
    default: null,
  },
  showEditor: {
    type: Boolean,
    default: false
  },
  imageUrl: {
    type: String,
    default: null
  }
});
const { showEditor, imageUrl } = toRefs(props)

const avatarVisible = ref(false)
const openAvatar = () => {
  // 打开数字教师
  avatarVisible.value = true;
}

const editorVisible = ref(false)
const openEdit = () => {
  editorVisible.value = true
}
const affixEditorDiv = ref(null)

let editor

const insertImage = (url) => {
  // 插入图片
  const { state: { tr }, view } = editor.innerEditor;
  editor.innerEditor.commands.insertContentAt(tr.selection.to, {
    type: 'image',
    attrs: {
      src: url,
      name,
      'type': 'image',
      'previewType': 'image',
    },
  });
}

onMounted(async () => {
  // try {
  //   // 动态导入 UAIEditor
  //   const module = await import(/* @vite-ignore */ "@uai-team/uai-editor")
  //   UAIEditor = module.UAIEditor
  // } catch (error) {
  //   console.error('Failed to load UAIEditor:', error)
  // }
  editor = new UAIEditor({
    element: document.getElementById('affixEditorDiv'),
    contentRetentionKey: props.contentRetentionKey,
    header: "classic",
    lang: 'zh_CN',
    ai: {
      chat: {
        models: {
          "default": {
              modelType: 'openai',
              baseUrl: 'http://localhost:8000/api/v0',
              apiKey: 'Empty',
              model: 'Qwen-2.5-7B-Instruct-NPU',
              stream: true
          },
          'Ryzen-AI': {
              modelType: 'openai',
              baseUrl: 'http://localhost:8000/api/v0',
              apiKey: 'Empty',
              model: 'Qwen-2.5-7B-Instruct-NPU',
              stream: true
          },
          "GLM-4-32B": {
            modelType: 'openai',
            baseUrl: 'https://ai.gitee.com/v1',
            apiKey: process.env.GITEE_TRY_TOKEN,
            model: 'GLM-4-32B',
            headers: {
              "X-Failover-Enabled": "true",
              "X-Package": "1910",
            },
            stream: true
          },
          "InternLM3-8B-Instruct": {
            modelType: 'openai',
            baseUrl: 'https://ai.gitee.com/v1',
            apiKey: process.env.GITEE_TRY_TOKEN,
            model: 'InternLM3-8B-Instruct',
            headers: {
              "X-Failover-Enabled": "true",
              "X-Package": "1910",
            },
            stream: true
          },
        },
      },
      image: {
        models: {
          text2image: {
            "default": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1', // images/generations
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
            "Kolors": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1', // images/generations
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
          },
          image2image: {
            "default": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1',
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
            "Kolors": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1', // images/generations
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
          },
          inpainting: {
            "default": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1',
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
            "Kolors": {
              modelType: 'moark',
              baseUrl: 'https://ai.gitee.com/v1', // images/generations
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Kolors',
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
          },
        }
      },
      audio: {
        models: {
          speech: {
            "default": {
                modelType: "moark",
                baseUrl: "https://ai.gitee.com/v1/audio/speech", // audio/speech
                apiKey: process.env.GITEE_TRY_TOKEN,
                model: "MegaTTS3",
                voice: "alloy",
                headers: {
                    'Authorization': `Bearer ${process.env.GITEE_TRY_TOKEN}`,
                    'Content-Type': 'application/json',
                }
            },
            "Spark-TTS-0.5B": {
              modelType: "moark",
              baseUrl: "https://ai.gitee.com/v1/async/audio/speech", // audio/speech
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: "Spark-TTS-0.5B",
              voice: "alloy",
              headers: {
                'Authorization': `Bearer ${process.env.GITEE_TRY_TOKEN}`,
                'Content-Type': 'application/json',
                "X-Package": "1910",
              }
            },
          },
          translations: {
            "default": {
              modelType: "openai",
              baseUrl: "https://ai.gitee.com/v1", // audio/translations
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: "whisper-large-v3",
              headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
          }
        }
      },
      vision: {
        models: {
          image: {
            "default": {
              modelType: "moark",
              baseUrl: 'https://ai.gitee.com/v1',
              apiKey: process.env.GITEE_TRY_TOKEN,
              model: 'Qwen2.5-VL-32B-Instruct',
              headers: {
                "Content-Type": "application/json",
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
              }
            },
          },
        },
        commands: {
          image: [{
            name: "教学解答",
            prompt: "你是一名专业教师，请告诉我这幅图的学习方法，或者告诉我这幅图的解题方法、步骤以及答案内容。"
          }],
        }
      }
    },
  })
})

watch(
  showEditor,
  (newValue) => {
    editorVisible.value = newValue
  },
  {
    immediate: true
  }
)

watch(
  imageUrl,
  (newValue) => {
    if (!newValue) return
    insertImage(newValue)
  },
  {
    immediate: true
  }
)
</script>
<style lang="scss" scoped>
.affix {
  position: fixed;
  right: 5px;
  top: 50vh;
  z-index: 9999;

  .affix-info {
    background-color: #fff;
    padding: 10px;
  }
}

.icon {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
