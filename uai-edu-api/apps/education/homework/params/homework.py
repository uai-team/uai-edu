#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : homework.py
# @desc     : 作业管理

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class HomeworkParams(QueryParams):
    def __init__(
            self,
            category_id: int | None = Query(None, title="类目ID"),
            dept_id: str | None = Query(None, title="可见范围"),
            homework_name: str | None = Query(None, title="作业名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.category_id = category_id
        self.dept_id = dept_id
        self.homework_name = ("like", homework_name)
