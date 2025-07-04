import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
from pydantic import Field
from typing import Optional


def get_document(
        document_id: str = Field(..., description="文档ID"),
        app_id: Optional[str] = Field(None, description="应用唯一标识"),
        app_secret: Optional[str] = Field(None, description="应用密钥")
):
    """获取文档内容"""
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: GetDocumentRequest = GetDocumentRequest.builder() \
        .document_id(document_id) \
        .build()

    # 发起请求
    response: GetDocumentResponse = client.docx.v1.document.get(request)

    # 处理失败返回
    if not response.success():
        fail_message = f"client.docx.v1.document.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        lark.logger.error(fail_message)
        return fail_message

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return lark.JSON.marshal(response.data, indent=4)