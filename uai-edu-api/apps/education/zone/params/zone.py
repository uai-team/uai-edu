#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : zone.py
# @desc     : 专区信息

from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class ZoneParams(QueryParams):
    def __init__(
            self,
            zone_name: str | None = Query(None, title="专区名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.zone_name = ("like", zone_name)
