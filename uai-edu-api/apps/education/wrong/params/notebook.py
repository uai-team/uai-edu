#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/29
# @File     : notebook.py
# @desc     : 我的错题本

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class NotebookParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
