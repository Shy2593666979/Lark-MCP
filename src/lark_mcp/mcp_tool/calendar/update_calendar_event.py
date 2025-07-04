import json
import uuid

import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *
from typing import Optional
from pydantic import Field

def update_calendar_event(
        calendar_id: str = Field(..., description="日历ID（必填）"),
        event_id: str = Field(..., description="日程事件ID（必填）"),
        user_id_type: Optional[str] = Field(default="open_id",
                                            description="用户ID类型，可选值：open_id、union_id、user_id。"),
        summary: str = Field(None, description="需要更新的日程标题"),
        description: str = Field(None, description="需要更新的日程描述"),
        start_date: str = Field(None, description="需要更新的开始日期，格式YYYY-MM-DD"),
        start_timestamp: str = Field(None, description="需要更新的开始时间戳，例如1602504000"),
        end_date: str = Field(None, description="需要更新的结束日期，格式YYYY-MM-DD"),
        end_timestamp: str = Field(None, description="需要更新的结束时间戳， 例如1602504000"),
        location_name: str = Field(None, description="需要更新的日程的会议位置"),
        location_address: str = Field(None, description="需要更新的日程的会议具体地点，如301会议室"),        timezone: str = Field("Asia/Shanghai", description="时区"),
        visibility: str = Field(None, description="需要更新的日程公开范围"),
        attendee_ability: str = Field(None, description="需要更新的参与者权限"),
        free_busy_status: str = Field(None, description="需要更新的日程占用的忙闲状态，新建日程默认为 busy"),
        recurrence: str = Field(None, description="需要更新的重复规则，如FREQ=DAILY;INTERVAL=1"),
        app_id: Optional[str] = Field(None, description="应用唯一标识"),
        app_secret: Optional[str] = Field(None, description="应用密钥"),
):
    """
    更新飞书的日程

    Args:
        app_id: 应用ID（不需要提供）
        app_secret: 应用密钥（不需要提供）
        summary: 日程标题
        description: 日程描述
        start_date: 开始日期，格式YYYY-MM-DD
        start_timestamp: 开始时间戳
        end_date: 结束日期，格式YYYY-MM-DD
        end_timestamp: 结束时间戳
        timezone: 时区设置
        visibility: 可见性设置
        attendee_ability: 参与者权限
        free_busy_status: 忙闲状态
        recurrence: 重复规则
        user_id_type: 用户id类型
        location_name: 日程的地点名称, 如301会议室
        location_address: 日程的会议地点地址，如公司大楼一楼
        calendar_id: 日历ID（必填）
        event_id: 日程事件ID（必填）

    Returns:
        日程创建成功返回日程信息，失败返回错误信息
    """
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()

    # 构造请求对象
    request: PatchCalendarEventRequest = PatchCalendarEventRequest.builder() \
        .event_id(event_id) \
        .calendar_id(calendar_id) \
        .user_id_type(user_id_type) \
        .request_body(CalendarEvent.builder()
                      .summary(summary)
                      .description(description)
                      .start_time(TimeInfo.builder()
                                  .date(start_date)
                                  .timestamp(start_timestamp)
                                  .timezone(timezone)
                                  .build())
                      .end_time(TimeInfo.builder()
                                .date(end_date)
                                .timestamp(end_timestamp)
                                .timezone(timezone)
                                .build())
                      .visibility(visibility)
                      .location(EventLocation.builder().name(location_name).address(location_address).build())
                      .attendee_ability(attendee_ability)
                      .free_busy_status(free_busy_status)
                      .recurrence(recurrence)
                      .build()) \
        .build()

    # 发起请求
    response: PatchCalendarEventResponse = client.calendar.v4.calendar_event.patch(request)

    # 处理失败返回
    if not response.success():
        error_msg = (
            f"client.calendar.v4.calendar_event.create failed, "
            f"code: {response.code}, "
            f"msg: {response.msg}, "
            f"log_id: {response.get_log_id()}, "
            f"resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        )
        lark.logger.error(error_msg)
        return error_msg

    # 基础事件信息处理
    update_calendar_event_message = lark.JSON.marshal(response.data, indent=4)
    lark.logger.info(update_calendar_event_message)

    # 返回组合结果
    return update_calendar_event_message