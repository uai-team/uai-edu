#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : paper.py
# @desc     : 考试试卷

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class ExamPaperParams(QueryParams):
    def __init__(
            self,
            category_id: int | None = Query(None, title="类目ID"),
            dept_id: str | None = Query(None, title="可见范围"),
            paper_name: str | None = Query(None, title="试卷名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.category_id = category_id
        self.dept_id = dept_id
        self.paper_name = ("like", paper_name)
