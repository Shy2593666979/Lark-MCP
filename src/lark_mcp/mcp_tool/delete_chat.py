import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from pydantic import Field
from typing import Optional


def delete_chat(
        chat_id: str = Field(..., description="群聊ID"),
        app_id: Optional[str] = Field(None, description="应用唯一标识"),
        app_secret: Optional[str] = Field(None, description="应用密钥")
):
    """删除群聊"""
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: DeleteChatRequest = DeleteChatRequest.builder() \
        .chat_id(chat_id) \
        .build()

    # 发起请求
    response: DeleteChatResponse = client.im.v1.chat.delete(request)

    # 处理失败返回
    if not response.success():
        fail_message = f"client.im.v1.chat.delete failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        lark.logger.error(fail_message)
        return fail_message

    # 处理业务结果
    return f"chat id: {chat_id}已经被删除！"