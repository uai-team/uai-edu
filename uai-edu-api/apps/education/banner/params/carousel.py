#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : carousel.py
# @desc     : 轮播图

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class CarouselParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
