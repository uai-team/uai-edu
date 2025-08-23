#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : homeworkitem.py
# @desc     : 作业管理

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class HomeworkItemParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
