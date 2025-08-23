#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : course.py
# @desc     : 课程信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class CourseParams(QueryParams):
    def __init__(
            self,
            category_id: int | None = Query(None, title="类目ID"),
            course_name: str | None = Query(None, title="课程名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.category_id = category_id
        self.course_name = ("like", course_name)
