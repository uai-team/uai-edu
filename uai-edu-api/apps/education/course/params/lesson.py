#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/15
# @File     : lesson.py
# @desc     : 课时信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class LessonParams(QueryParams):
    def __init__(
            self,
            chapter_id: int | None = Query(None, title="章节ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.chapter_id = chapter_id
