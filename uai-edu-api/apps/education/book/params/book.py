#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/07
# @File     : book.py
# @desc     : 教材信息

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class BookParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
