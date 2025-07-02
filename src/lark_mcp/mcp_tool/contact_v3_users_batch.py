import json

import lark_oapi as lark
from lark_oapi.api.contact.v3 import *
from pydantic import Field, BaseModel
from typing import Literal, List, Optional


def contact_v3_user_batch(user_ids: List[str] = Field(...,
                                                      description="用户ID列表，ID类型与 user_id_type 参数一致。单次请求最多支持50个用户ID。"),
                          user_id_type: Optional[str] = Field(default="open_id",
                                                              description="用户ID类型，可选值：open_id、union_id、user_id。"),
                          department_id_type: Optional[str] = Field(default="open_department_id",
                                                                    description="部门ID类型，可选值：open_department_id、department_id。"),
                          app_id: Optional[str] = Field(None, description="应用唯一标识"),
                          app_secret: Optional[str] = Field(None, description="应用密钥")
                          ):
    """根据该工具可以批量获取用户的具体信息"""
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: BatchUserRequest = BatchUserRequest.builder() \
        .user_id_type(user_id_type) \
        .department_id_type(department_id_type) \
        .user_ids(user_ids) \
        .build()

    # 发起请求
    response: BatchUserResponse = client.contact.v3.user.batch(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.contact.v3.user.batch failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return str(f"client.contact.v3.user.batch failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return lark.JSON.marshal(response.data, indent=4)
