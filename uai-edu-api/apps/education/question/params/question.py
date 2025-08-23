#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/22
# @File     : question.py
# @desc     : 题目信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class QuestionParams(QueryParams):
    def __init__(
            self,
            category_id: int | None = Query(None, title="类目ID"),
            question_type: str | None = Query(None, title="题目类型"),
            question_title: str | None = Query(None, title="题目内容"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.category_id = category_id
        self.question_type = question_type
        self.question_title = ("like", question_title)
