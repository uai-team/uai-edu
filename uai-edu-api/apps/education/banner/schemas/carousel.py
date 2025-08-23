#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : carousel.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Carousel(BaseModel):
    carousel_img: str = Field(..., title="图片链接")
    carousel_title: str | None = Field(None, title="横幅名称")
    carousel_url: str | None = Field(None, title="链接地址")
    carousel_target: str | None = Field(None, title="打开目标")
    create_user_id: int = Field(None, title="创建人")


class CarouselSimpleOut(Carousel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
