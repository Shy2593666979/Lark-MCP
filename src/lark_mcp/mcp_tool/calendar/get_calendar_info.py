import json
import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *
from pydantic import Field
from typing import Optional, Literal

def get_calendar_event(
    calendar_id: str = Field(..., description="日历ID（必填）"),
    event_id: str = Field(..., description="日程事件ID（必填）"),
    need_meeting_settings: bool = Field(True, description="是否需要返回会议设置信息"),
    need_attendee: bool = Field(True, description="是否需要返回参会者信息"),
    max_attendee_num: int = Field(10, description="最大返回参会者数量"),
    user_id_type: Literal["open_id", "user_id", "union_id"] = Field("open_id", description="用户ID类型"),
    app_id: Optional[str] = Field(None, description="应用唯一标识"),
    app_secret: Optional[str] = Field(None, description="应用密钥")
):
    """获取日历事件详情"""
    # 初始化客户端
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: GetCalendarEventRequest = GetCalendarEventRequest.builder() \
        .calendar_id(calendar_id) \
        .event_id(event_id) \
        .need_meeting_settings(need_meeting_settings) \
        .need_attendee(need_attendee) \
        .max_attendee_num(max_attendee_num) \
        .user_id_type(user_id_type) \
        .build()

    # 发起请求
    response: GetCalendarEventResponse = client.calendar.v4.calendar_event.get(request)

    # 处理失败返回
    if not response.success():
        fail_message = f"client.calendar.v4.calendar_event.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        lark.logger.error(fail_message)
        return fail_message

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return lark.JSON.marshal(response.data, indent=4)