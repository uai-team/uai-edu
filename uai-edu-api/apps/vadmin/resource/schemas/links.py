#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : links.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Links(BaseModel):
    link_type: str = Field(..., title="链接类型")
    image_url: str | None = Field(None, title="图片链接")
    name: str = Field(..., title="链接名称")
    url: str = Field(..., title="链接地址")
    target: str = Field(..., title="打开目标")
    create_user_id: int | None = Field(None, title="创建人")


class LinksSimpleOut(Links):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
