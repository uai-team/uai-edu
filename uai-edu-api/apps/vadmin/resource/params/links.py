#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : links.py
# @desc     : 链接信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class LinksParams(QueryParams):
    def __init__(self, 
            name: str | None = Query(None, title="链接名称"),
            link_type: str | None = Query(None, title="链接类型"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.link_type = link_type
