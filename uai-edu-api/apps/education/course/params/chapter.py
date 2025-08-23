#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/14
# @File     : chapter.py
# @desc     : 章节信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class ChapterParams(QueryParams):
    def __init__(
            self,
            course_id: int | None = Query(None, title="课程ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.course_id = course_id
