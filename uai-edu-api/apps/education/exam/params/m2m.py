#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : m2m.py
# @desc     : 考试试卷题目

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class TitleQuestionParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
