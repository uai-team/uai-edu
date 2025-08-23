#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : views.py
# @desc     : 视图层

from fastapi import UploadFile, Depends, APIRouter
from . import schemas, crud, params, models
from apps.vadmin.auth.utils.validation.auth import Auth
from application.settings import ALIYUN_OSS
from utils.response import SuccessResponse
from core.database import db_getter
from sqlalchemy.ext.asyncio import AsyncSession
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from apps.vadmin.auth.utils.current import FullAdminAuth, AllUserAuth, OpenAuth
from core.dependencies import IdList
from sqlalchemy.orm import joinedload


app = APIRouter()

###########################################################
#    图片资源管理
###########################################################
@app.get("/images", summary="获取图片列表")
async def get_images_list(p: params.ImagesParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.VadminImages
    v_options = [joinedload(model.create_user)]
    v_schema = schemas.ImagesOut
    datas, count = await crud.ImagesDal(auth.db).get_datas(
        **p.dict(),
        v_options=v_options,
        v_schema=v_schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/images", summary="创建图片")
async def create_images(file: UploadFile, auth: Auth = Depends(FullAdminAuth())):
    filepath = f"/resource/images/"
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(filepath, file)
    data = schemas.Images(
        filename=file.filename,
        image_url=result,
        create_user_id=auth.user.id
    )

    return SuccessResponse(await crud.ImagesDal(auth.db).create_data(data=data))


@app.delete("/images", summary="删除图片", description="硬删除")
async def delete_images(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ImagesDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.get("/images/{data_id}", summary="获取图片信息")
async def get_images(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ImagesDal(auth.db).get_data(data_id, v_schema=schemas.ImagesSimpleOut))



###########################################################
#    链接信息
###########################################################
@app.get("/links", summary="获取链接信息列表")
async def get_links_list(p: params.LinksParams = Depends(), auth: Auth = Depends(OpenAuth())):
    datas, count = await crud.LinksDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/links", summary="创建链接信息")
async def create_links(data: schemas.Links, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.LinksDal(auth.db).create_data(data=data))


@app.delete("/links", summary="删除链接信息", description="硬删除")
async def delete_links_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.LinksDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/links/{data_id}", summary="更新链接信息")
async def put_links(data_id: int, data: schemas.Links, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.LinksDal(auth.db).put_data(data_id, data))


@app.get("/links/{data_id}", summary="获取链接信息信息")
async def get_links(data_id: int, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.LinksDal(db).get_data(data_id, v_schema=schemas.LinksSimpleOut))

