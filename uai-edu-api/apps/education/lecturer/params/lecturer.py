#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : lecturer.py
# @desc     : 教师信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class LecturerParams(QueryParams):
    def __init__(
            self,
            lecturer_name: str | None = Query(None, title="教师名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.lecturer_name = ("like", lecturer_name)
