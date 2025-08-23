<template>
  <div class="lesson-detail">
    <Affix />
    <div class="lesson-header">
      <div class="header-left">
        <span class="cursor" @click="handleBack">
          <img class="cursor-image" src="@/assets/svg/return.svg" alt="return" />
        </span>
        <router-link :to="{ path: '/course/detail', query: { id: courseInfo?.id } }" class="left_col">
          <span class="header-title">
            {{ courseInfo?.course_name }}
          </span>
        </router-link>
      </div>
      <div class="header-right">
        <User />
      </div>
    </div>
    <div class="lesson-body">
      <div class="lesson-content" :class="{ show_panel: cateType }">
        <div class="player-box">
          <div v-show="showing" id="player" v-loading="loading" class="player-video" />
          <div v-show="!showing" class="study-tip">
            <div v-if="nextLesson">
              下一节：{{ nextLesson?.lesson_name }}
              <el-button size="small" type="success" @click="handleStudy(nextLesson)"> 马上学习</el-button>
            </div>
          </div>
        </div>
        <div class="lesson-info">
          <div class="lesson-info-tab">
            <div :class="{ on: cateType === 'chapter' }" class="lesson-info-button cursor"
              @click="handleTab('chapter')"><img src="@/assets/svg/chapter.svg" class="img-icon" />目录</div>
            <div :class="{ on: cateType === 'resource' }" class="lesson-info-button cursor"
              @click="handleTab('resource')"><img src="@/assets/svg/chapter.svg" class="img-icon" />资源</div>
            <div :class="{ on: cateType === 'chat' }" class="lesson-info-button cursor" @click="handleTab('chat')"><img
                src="@/assets/svg/comment.svg" class="img-icon" />问答</div>
            <div :class="{ on: cateType === 'comment' }" class="lesson-info-button cursor"
              @click="handleTab('comment')"><img src="@/assets/svg/comment.svg" class="img-icon" />评论</div>
          </div>
          <div v-if="cateType != ''" class="lesson-info-content">
            <div v-if="cateType === 'chapter'" class="lesson-info-chapter">
              <div v-for="(one, index) in courseInfo?.chapterRespList" :key="index">
                <div class="catalog-chapter">{{ index + 1 }}. {{ one.chapter_name }}</div>
                <div v-for="(two, num) in one.lessonRespList" :key="num" class="catalog-chapter-lesson cursor"
                  :class="{ on: studyLesson.id == two?.id }" @click="handleStudy(two)">
                  <div class="lesson-name">
                    &nbsp;&nbsp;
                    <!-- <span v-if="two.lessonType === 10">{{ getResourceTypeName(two.resourceResp?.resourceType) }}：</span> -->
                    {{ index + 1 }}-{{ num + 1 }} {{ two.lesson_name }}
                    <!-- <span v-if="two.resourceResp && two.resourceResp.resourceType < 3 && two.resourceResp.videoStatus === 1">(未更新)</span>
                    <span v-if="two.isFree">(试看)</span>
                    <div v-if="two.lessonType === 10" class="lesson-progress">
                      <el-progress v-if="two" :percentage="two.lessonProgress ? two.lessonProgress : 0" :stroke-width="2" :status="two.lessonProgress > 99 ? 'success' : ''" />
                    </div> -->
                  </div>
                </div>
              </div>
            </div>
            <div v-if="cateType === 'resource'" class="lesson-info-chapter">
              <div v-if="studyLesson.lesson_courseware" class="catalog-chapter-lesson cursor"
                :class="{ on: studyLessonResource === '课件资源' }"
                @click="handleResource('课件资源', studyLesson.lesson_courseware)">课件资源</div>
              <div v-if="studyLesson.lesson_tasklist" class="catalog-chapter-lesson cursor"
                :class="{ on: studyLessonResource === '学习任务' }"
                @click="handleResource('学习任务', studyLesson.lesson_tasklist)">学习任务</div>
              <div v-if="studyLesson.lesson_exercise" class="catalog-chapter-lesson cursor"
                :class="{ on: studyLessonResource === '课后练习' }"
                @click="handleResource('课后练习', studyLesson.lesson_exercise)">课后练习</div>
            </div>
            <div v-if="cateType === 'chat'" class="lesson-info-chat">
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
            <div v-if="cateType === 'comment'" class="lesson-info-comment">
              课程评论
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { OpenAI } from 'openai';

import { courseApi } from '@/api/course'
import { AIChat } from "@/utils/config";
import { getStorageUser } from '@/utils/storage'
import { getClient, getClientForPri } from '@/utils/polyv'

import User from '@/components/Layout/User.vue'

const route = useRoute()

const userInfo = getStorageUser()
const courseInfo = ref(null)
const loading = ref(false)
const showing = ref(true)

// 当前播放的课时id
const studyLesson = ref()
const studyLessonResource = ref()
// 下一个课时
const nextLesson = ref()
// 用户学习信息
const userStudy = {}
let progressInterval = null
let polyvPlayerClient = null

onMounted(async () => {
  // 课程信息
  await getCourseInfo()

  // 初始化学习
  await handleStudy({ id: route.query.lessonId })
})

onUnmounted(() => {
  // 清除
  handleClear()
})

// 学习
async function handleStudy(lesson) {
  loading.value = true
  showing.value = true
  studyLessonResource.value = null

  // 更新课程信息
  await getCourseInfo()
  try {
    studyLesson.value = await courseApi.studyLesson({ course_id: route.query.id, lesson_id: lesson.id })
    // {
    //   "chapter_id": 1,
    //   "lesson_name": "观潮",
    //   "lesson_type": "video",
    //   "order": 1,
    //   "lecturer": null,
    //   "instructor": null,
    //   "lesson_resource": "/media/lessons/小学/语文/统编版/四年级/上册/观潮.mp4",
    //   "lesson_courseware": null,
    //   "lesson_tasklist": null,
    //   "lesson_exercise": null,
    //   "lesson_desc": null,
    //   "id": 1,
    //   "create_datetime": "2025-07-15 14:32:57",
    //   "update_datetime": "2025-07-15 14:32:57"
    // }
  } catch (e) {
    loading.value = false
  }

  // 资源类型
  if (studyLesson.value.lesson_type === "video") {
    handleClear()
    // 视频播放
    handlePlay(studyLesson.value)
  } else if (studyLesson.value.lesson_type === "audio") {
    handleClear()
    // 音频播放
    handlePlay(studyLesson.value)
  } else if (studyLesson.value.lesson_type === "document") {
    // 文档播放
    handleDoc(studyLesson.value.lesson_resource)
  } else {
    ElMessage.warning('暂不支持该类型资源')
  }
  loading.value = false
}

/**
 *  获取课程信息
 */
async function getCourseInfo() {
  courseInfo.value = await courseApi.courseDetail({ id: route.query.id })
  return courseInfo.value
}

/**
 * 获取课程学习中的下一节
 * @param lessonId
 * @returns {*}
 */
function getNextPeriod(lessonId) {
  for (let i = 0; i < courseInfo.value.chapterRespList.length; i++) {
    for (let j = 0; j < courseInfo.value.chapterRespList[i].lessonRespList.length; j++) {
      if (courseInfo.value.chapterRespList[i].lessonRespList[j].id === lessonId) {
        if (courseInfo.value.chapterRespList[i].lessonRespList.length === j + 1) {
          if (courseInfo.value.chapterRespList[i + 1]) {
            return courseInfo.value.chapterRespList[i + 1].lessonRespList[0]
          }
        } else {
          return courseInfo.value.chapterRespList[i].lessonRespList[j + 1]
        }
      }
    }
  }
}

/**
 * 文档图片播放
 */
function handleResource(resource, srcPath) {
  studyLessonResource.value = resource
  const iframe = document.createElement('iframe')
  iframe.setAttribute('src', srcPath)
  iframe.style.width = '100%'
  iframe.style.height = '100%'
  const player = document.getElementById('player')
  player.innerHTML = ''
  player.appendChild(iframe)
}

/**
 * 文档图片播放
 */
function handleDoc(srcPath) {
  const iframe = document.createElement('iframe')
  iframe.setAttribute('src', srcPath)
  iframe.style.width = '100%'
  iframe.style.height = '100%'
  const player = document.getElementById('player')
  player.innerHTML = ''
  player.appendChild(iframe)

  // 记录进度
  // handleStudyRecord()
}

// 音视频播放
function handlePlay(studyLesson) {
  // 清除内容
  document.getElementById('player').innerHTML = ''
  polyvPlayerClient = getClientForPri(studyLesson, true, "on")
  polyvPlayerClient.on('s2j_onVideoPlay', function () {
    // 开始播放
    handleStart()
  })
  polyvPlayerClient.on('s2j_onVideoPause', function () {
    // 暂停播放
    handlePause()
  })
  polyvPlayerClient.on('s2j_onPlayOver', function () {
    // 完成播放
    handleComplete()
  })
}

// 记录进度
function handleStudyRecordForVod(studyStatus) {
  userStudy.course_id = courseInfo.value.id
  userStudy.chapter_id = studyLesson.value.chapter_id
  userStudy.lesson_id = studyLesson.value.id
  userStudy.user_id = userInfo.id
  // studyStatus 1学习中 2暂停
  userStudy.study_status = studyStatus
  userStudy.current_duration = polyvPlayerClient.j2s_getCurrentTime()
  courseApi
    .studyProgress(userStudy)
    .then((res) => {
      if (res === 'OK') {
        // 完成，暂停同步
        if (progressInterval) {
          clearInterval(progressInterval)
        }
      }
    })
    .catch((error) => {
      clearInterval(progressInterval)
      polyvPlayerClient.j2s_pauseVideo()
      ElMessageBox.confirm('系统异常将暂停观看，请联系管理员', '提示', {
        confirmButtonText: '返回',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        handleBack()
      })
    })
}

// 记录进度
function handleStudyRecord() {
  userStudy.currentPage = 1
  courseApi
    .studyProgress(userStudy)
    .then((res) => {
      if (res === 'OK') {
        // 完成，暂停同步
        if (progressInterval) {
          clearInterval(progressInterval)
        }
      }
    })
    .catch((error) => {
      ElMessageBox.confirm('系统异常将暂停观看，请联系管理员', '提示', {
        confirmButtonText: '返回',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        handleBack()
      })
    })
}

// tab切换
const cateType = ref('chapter')

function handleTab(item) {
  if (item === cateType.value) {
    cateType.value = ''
  } else {
    cateType.value = item
  }
}

// 开始
function handleStart() {
  // 播放
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  progressInterval = setInterval(() => {
    handleStudyRecordForVod(1)
  }, 3000)
}

// 暂停
function handlePause() {
  // 更新进度
  handleStudyRecordForVod(2)
  if (progressInterval) {
    clearInterval(progressInterval)
  }
}

// 完成播放
function handleComplete() {
  // 更新进度
  handleStudyRecordForVod(1)
  // 播放完成
  if (progressInterval) {
    clearInterval(progressInterval)
  }

  // 显示下一节
  showing.value = false
  nextLesson.value = getNextPeriod(studyLesson.value.id)
}

// 清除
function handleClear() {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  if (polyvPlayerClient) {
    // 暂停学习
    handleStudyRecordForVod(2)
    polyvPlayerClient.destroy()
  }
}

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

</script>
<style lang="scss">
.lesson-header {
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

.lesson-body {
  background: #000;

  .lesson-content {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-between;

    .player-box {
      width: calc(100% - 66px);
      padding: 10px 20px;

      .player-video {
        height: calc(100vh - 86px);
      }

      .study-tip {
        height: calc(100vh - 86px);
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        color: #fff;
        font-size: 16px;
      }
    }

    .lesson-info {
      background: #1c1f21;
      display: flex;
      flex-direction: row-reverse;

      .lesson-info-tab {
        width: 80px;
        font-size: 16px;

        .lesson-info-button {
          color: #fff;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 20px 0;

          .img-icon {
            width: 25px;
          }

          &:hover {
            background-color: #333;
          }
        }

        .on {
          background-color: #333;
        }
      }

      .content {
        display: block;
      }

      .lesson-info-content {
        background-color: #fff;
        // color: #fff;
        width: 400px;
        // padding: 10px;
        height: calc(100vh - 66px);
        overflow: auto;

        .lesson-info-chapter {
          padding: 20px;
        }

        .lesson-info-comment {
          padding: 20px;
        }

        .catalog-chapter {
          font-size: 16px;
          margin: 15px 0;
        }

        .catalog-chapter-lesson {
          font-size: 14px;
          margin: 10px;

          &:hover {
            color: red;
          }

          .lesson-name {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 350px;
          }

          .lesson-progress {
            height: 20px;
            width: 300px;
            margin-left: 50px;
          }

          .lesson-live {
            font-size: 12px;
            text-align: right;
          }
        }

        .lesson-info-chat {
          height: 100%;
          // background-color: #fff;
          // padding: 10px 3px;
        }

        .on {
          color: #2256f6;
        }
      }
    }
  }
}
</style>
