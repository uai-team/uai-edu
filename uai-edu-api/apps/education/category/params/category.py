#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : category.py
# @desc     : 类目信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class CategoryParams(QueryParams):
    def __init__(
            self,
            category_name: str | None = Query(None, title="类目名称"),
            category_type: str | None = Query(None, title="类目类型"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.category_name = ("like", category_name)
        self.category_type = category_type
