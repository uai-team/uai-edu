#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/10/19 15:41 
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 简要说明

from fastapi import APIRouter, Depends
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from utils.response import SuccessResponse
import datetime
from apps.vadmin.record.crud import LoginRecordDal

app = APIRouter()


###########################################################
#    工作区管理
###########################################################
@app.get("/project", summary="获取项目")
async def get_project():
    data = [
        {
            "name": 'Mysql',
            "icon": 'vscode-icons:file-type-mysql',
            "message": '最流行的关系型数据库管理系统',
            "link": "https://www.mysql.com/",
        },
        {
            "name": 'FastAPI',
            "icon": 'simple-icons:fastapi',
            "message": '一个现代、快速(高性能)的 web 框架',
            "link": "https://fastapi.tiangolo.com/zh/",
        },
        {
            "name": 'Vue',
            "icon": 'logos:vue',
            "message": '渐进式 JavaScript 框架',
            "link": "https://cn.vuejs.org/",
        },
        {
            "name": 'Element-plus',
            "icon": 'logos:element',
            "message": '面向设计师和开发者的组件库',
            "link": "https://element-plus.org/zh-CN/",
        },
        {
            "name": 'Typescript',
            "icon": 'vscode-icons:file-type-typescript-official',
            "message": 'TypeScript是JavaScript类型的超集',
            "link": "https://www.typescriptlang.org/",
        },
        {
            "name": 'Vite',
            "icon": 'vscode-icons:file-type-vite',
            "message": 'Vite 下一代的前端工具链',
            "link": "https://cn.vitejs.dev/",
        }
    ]
    return SuccessResponse(data)


@app.get("/shortcuts", summary="获取快捷操作")
async def get_shortcuts():
    data = [
        {
            "name": "Swagger UI 接口文档",
            "link": "http://127.0.0.1:9000/docs"
        },
        {
            "name": "Redoc 接口文档",
            "link": "http://127.0.0.1:9000/redoc"
        },
        {
            "name": "前端文档",
            "link": "https://element-plus-admin-doc.cn/"
        },
        {
            "name": "UnoCSS 中文文档",
            "link": "https://unocss.nodejs.cn/guide/"
        },
        {
            "name": "Iconify 文档",
            "link": "https://icon-sets.iconify.design/"
        },
        {
            "name": "echarts 文档",
            "link": "https://echarts.apache.org/zh/index.html"
        },
    ]
    return SuccessResponse(data)
