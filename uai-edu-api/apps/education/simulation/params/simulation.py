#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/03
# @File     : simulation.py
# @desc     : 仿真信息

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class SimulationParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
