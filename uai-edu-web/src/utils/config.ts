export const AIChat = {
    models: {
        // 'default': {
        //     modelType: 'openai',
        //     baseUrl: 'http://localhost:11434/v1',
        //     apiKey: 'Ollama',
        //     model: 'Qwen3:4B',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        'Ryzen-AI': {
            modelType: 'openai',
            baseUrl: 'http://localhost:3000/flm/v1',
            apiKey: 'flm',
            model: 'llama3.1:8b',
            stream: true
        },
        // 'Ryzen-AI-1': {
        //     modelType: 'openai',
        //     baseUrl: 'http://localhost:8000/api/v0',
        //     apiKey: 'Empty',
        //     model: 'Qwen-2.5-7B-Instruct-NPU',
        //     stream: true
        // },
        'InternLM3-8B-Instruct': {
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
        // 'QwQ-32B': {
        //     modelType: 'openai',
        //     baseUrl: 'https://ai.gitee.com/v1',
        //     apiKey: process.env.GITEE_TRY_TOKEN,
        //     model: 'QwQ-32B',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        // 'DeepSeek-R1-Distill-Qwen-32B': {
        //     modelType: 'openai',
        //     baseUrl: 'https://ai.gitee.com/v1',
        //     apiKey: process.env.GITEE_TRY_TOKEN,
        //     model: 'DeepSeek-R1-Distill-Qwen-32B',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        // 'DeepSeek-R1': {
        //     modelType: 'openai',
        //     baseUrl: 'https://ai.gitee.com/v1',
        //     apiKey: process.env.GITEE_TRY_TOKEN,
        //     model: 'DeepSeek-R1',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        // 'DeepSeek-V3': {
        //     modelType: 'openai',
        //     baseUrl: 'https://ai.gitee.com/v1',
        //     apiKey: process.env.GITEE_TRY_TOKEN,
        //     model: 'DeepSeek-V3',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        'GLM-4-32B': {
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
        'Qwen2.5-VL-32B-Instruct': {
            modelType: 'openai',
            baseUrl: 'https://ai.gitee.com/v1',
            apiKey: process.env.GITEE_TRY_TOKEN,
            model: 'Qwen2.5-VL-32B-Instruct',
            headers: {
                "X-Failover-Enabled": "true",
                "X-Package": "1910",
            },
            stream: true
        },
        // 'ProxyInternLM3': {
        //     modelType: 'openai',
        //     baseUrl: 'http://localhost:5050/proxy/internlm/v1',
        //     apiKey: 'EMPTY',
        //     model: 'internlm3-latest',
        //     headers: {
        //         "X-Failover-Enabled": "true",
        //         "X-Package": "1910",
        //     },
        //     stream: true
        // },
        // 'ProxyInternVL3': {
        //     modelType: 'openai',
        //     baseUrl: 'http://localhost:5050/proxy/internlm/v1',
        //     apiKey: 'EMPTY',
        //     model: 'internvl3-latest',// 4225835
        //     stream: true
        // }
    }
};

export const AIImage = {
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
    }
};

export const AIAudio = {
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
        "Step-Audio-TTS-3B": {
            modelType: "moark",
            baseUrl: "https://ai.gitee.com/v1/audio/speech", // audio/speech
            apiKey: process.env.GITEE_TRY_TOKEN,
            model: "Step-Audio-TTS-3B",
            voice: "alloy",
            headers: {
                'Authorization': `Bearer ${process.env.GITEE_TRY_TOKEN}`,
                'Content-Type': 'application/json',
                "X-Package": "1910",
            }
        },
        "CosyVoice2": {
            modelType: "moark",
            baseUrl: "https://ai.gitee.com/v1/audio/speech", // audio/speech
            apiKey: process.env.GITEE_TRY_TOKEN,
            model: "CosyVoice2",
            voice: "alloy",
            headers: {
                'Authorization': `Bearer ${process.env.GITEE_TRY_TOKEN}`,
                'Content-Type': 'application/json',
                "X-Package": "1910",
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
    }
};
