#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/26
# @File     : exam.py
# @desc     : 用户考试

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class ExamUserParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)


class ExamUserAnswerParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
