<template>
  <div class="book-detail">
    <Affix />
    <div class="book-header">
      <div class="header-left">
        <span class="cursor" @click="handleBack">
          <img class="cursor-image" src="@/assets/svg/return.svg" alt="return" />
        </span>
        <router-link :to="{ path: '/book/detail', query: { id: bookInfo?.id } }" class="left_col">
          <span class="header-title">
            {{ bookInfo?.book_name }}
          </span>
        </router-link>
      </div>
      <div class="header-right">
        <User />
      </div>
    </div>
    <div class="book-body">
      <div class="book-content">
        <iframe :src="bookInfo.book_path" width="100%" height="100%" frameborder="0"></iframe>
      </div>
      <div class="book-chat">
        <t-chat ref="chatRef" layout="both" style="height: 100%;" :reverse="false"
          :clear-history="chatList.length > 0 && !isStreamLoad" @clear="clearConfirm">
          <template v-for="(item, index) in chatList" :key="index">
            <t-chat-item style="margin: 10px;" :avatar="item.avatar" :role="item.role"
              :variant="item.role === 'assistant' ? 'outline' : 'base'">
              <template #content>
                <t-image v-if="item.image" :src="item.image" shape="round" fit="scale-down" />
                <t-chat-content :content="item.content" />
              </template>
            </t-chat-item>
          </template>
          <template #footer>
            <div class="upload-box" style="width: fit-content; text-align: center; margin: 10px auto;">
              <t-upload ref="uploadRef" v-model="imagefile"
                action="https://service-bv448zsw-1257786608.gz.apigw.tencentcs.com/api/upload-demo" theme="image"
                accept="image/*" :multiple="false" :auto-upload="false" :show-image-file-name="false" :locale="{
          triggerUploadText: {
            image: '请选择图片',
          },
        }"></t-upload>
            </div>
            <t-chat-sender v-model="chatMessage" :stop-disabled="isStreamLoad" :textarea-props="{
          placeholder: '请输入消息...',
        }" @stop="onStop" @send="onSend" style="width: calc(100% - 20px); margin: 10px;">
              <template #prefix>
                <div class="model-select">
                  <t-tooltip v-model:visible="allowToolTip" content="切换模型" trigger="hover">
                    <t-select v-model="selectValue" :options="selectOptions" value-type="object"
                      @focus="allowToolTip = false"></t-select>
                  </t-tooltip>
                </div>
              </template>
              <template #suffix="{ renderPresets }">
                <component :is="renderPresets([])" />
              </template>
            </t-chat-sender>
          </template>
        </t-chat>
      </div>
    </div>
  </div>
</template>
<script setup>
import { OpenAI } from 'openai';

import { bookApi } from '@/api/book'

import { AIChat } from "@/utils/config";

import User from '@/components/Layout/User.vue'

const route = useRoute()

const bookInfo = ref({})

function handleBack() {
  window.history.go(-1)
}

const imagefile = ref([]);
const uploadRef = ref();

// 定义一个函数用于将文件转换为Base64
const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

const imageBase64 = ref(null);
watch(imagefile, async (image) => {
  if (image.length > 0) {
    try {
      if (image[0].raw) {
        imageBase64.value = await convertToBase64(image[0].raw);
      } else if (image[0].url) {
        imageBase64.value = image[0].url;
      }
    } catch (error) {
      console.error('文件转换为Base64时出错:', error);
    }
  } else {
    imageBase64.value = null;
  }
});

const chatRef = ref(null);
const allowToolTip = ref(false);
const isChecked = ref(true);
// 取消请求
const fetchCancel = ref(false);
// 思考中
const isThinking = ref(false);
// 流式数据加载中
const isStreamLoad = ref(false);

const selectOptions = Object.keys(AIChat.models).map((item) => {
  return { label: item, value: item };
});

const selectValue = ref({
  label: Object.keys(AIChat.models)[0],
  value: Object.keys(AIChat.models)[0],
});

const chatMessage = ref('');
const chatList = ref([]);

const clearConfirm = function () {
  chatList.value = [];
};

const onStop = function () {
  if (fetchCancel.value) {
    fetchCancel.value = false;
    isStreamLoad.value = false;
    isThinking.value = false;
  }
};

const onSend = async function (message) {
  if (isStreamLoad.value) {
    return;
  }
  if (!message) {
    return;
  }

  isStreamLoad.value = true;
  fetchCancel.value = true;

  const user = {
    avatar: 'https://tdesign.gtimg.com/site/avatar.jpg',
    name: '自己',
    datetime: new Date().toDateString(),
    image: imagefile.value.length > 0 ? imagefile.value[0].url : '',
    content: message,
    role: 'user',
  };

  chatList.value.push(user);
  imagefile.value = [];
  chatMessage.value = '';

  const chatConfig = AIChat.models[user.image ? "Qwen2.5-VL-32B-Instruct" : selectValue.value.value];
  const client = new OpenAI({
    baseURL: chatConfig.baseUrl,
    apiKey: chatConfig.apiKey,
    dangerouslyAllowBrowser: true,
  });
  await client.chat.completions.create({
    model: chatConfig.model ?? "o1",
    stream: chatConfig.stream,
    max_tokens: chatConfig.max_tokens,
    temperature: chatConfig.temperature,
    top_p: chatConfig.top_p,
    frequency_penalty: chatConfig.frequency_penalty,
    messages: user.image ? [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": message
          },
          {
            "type": "image_url",
            "image_url": {
              "url": user.image,
            }
          }
        ]
      }
    ] : [
      { "role": "system", "content": "你是一名资深的教育专家。" },
      { "role": "user", "content": `${message}` }
    ]
  }).then(async response => {
    chatList.value.push({
      avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png',
      name: '有爱智能教育',
      datetime: new Date().toDateString(),
      role: 'assistant',
      thinking: isChecked.value,
      reasoning: '',
      content: '',
    });

    const lastItem = chatList.value[chatList.value.length - 1];
    isThinking.value = true;

    // 记录开始时间
    let startTime;
    // 记录结束时间
    let endTime;

    for await (var chunk of response) {
      if (chunk.choices[0]?.delta?.reasoning_content) {
        if (!startTime) {
          startTime = new Date().getTime();
        }
        lastItem.reasoning += chunk.choices[0]?.delta?.reasoning_content;
      }
      if (chunk.choices[0]?.delta?.content) {
        if (!endTime) {
          endTime = new Date().getTime();
          isThinking.value = false;
          // 计算用时
          lastItem.duration = Math.floor((endTime - startTime) / 1000);
        }
        lastItem.content += chunk.choices[0]?.delta?.content;
      }
      chatRef.value?.scrollToBottom({ behavior: 'smooth' });
    }
  });

  isStreamLoad.value = false;
};

onMounted(async () => {
  bookInfo.value = await bookApi.bookDetail({ id: route.query.id })
})

onUnmounted(() => {
})

</script>
<style lang="scss">
.book-header {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  height: 66px;
  line-height: 66px;
  margin: 0 auto;
  font-size: 18px;
  border-bottom: solid 1px #ccc;

  .cursor-image {
    width: 20px;
  }

  .header-left {
    margin-left: 20px;

    .header-title {
      margin-left: 20px;
    }
  }

  .header-right {
    margin-top: 20px;
    margin-right: 20px;
    display: flex;
    align-items: center;
  }
}

.book-body {
  display: flex;
  height: calc(100vh - 66px);

  .book-content {
    flex: 1;
  }

  .book-chat {
    width: 500px;
    padding: 10px 3px;
  }
}
</style>
