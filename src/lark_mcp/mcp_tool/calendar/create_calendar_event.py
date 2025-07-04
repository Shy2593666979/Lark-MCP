import json
import uuid

import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *
from typing import Optional
from pydantic import Field
from lark_mcp.mcp_tool.calendar.primary_calendar import get_primary_calendar
from lark_mcp.mcp_tool.calendar.append_event_attendees import append_calendar_event_attendee


def create_calendar_event(
        user_id_type: Optional[str] = Field(default="open_id",
                                            description="用户ID类型，可选值：open_id、union_id、user_id。"),
        summary: str = Field(..., description="日程标题"),
        description: str = Field(..., description="日程描述"),
        need_notification: bool = Field(True, description="更新日程时，是否给日程参与人发送通知。"),
        start_date: str = Field(..., description="开始日期，格式YYYY-MM-DD"),
        start_timestamp: str = Field(..., description="开始时间戳，例如1602504000"),
        end_date: str = Field(..., description="结束日期，格式YYYY-MM-DD"),
        end_timestamp: str = Field(..., description="结束时间戳， 例如1602504000"),
        location_name: str = Field(None, description="日程的会议位置"),
        location_address: str = Field(None, description="日程的会议具体地点，如301会议室"),
        attendees: List[str] = Field(None, description="参会者列表，每个元素需包含用户的open_id，"),
        timezone: str = Field("Asia/Shanghai", description="时区"),
        visibility: str = Field("default", description="日程公开范围"),
        attendee_ability: str = Field("can_see_others", description="参与者权限"),
        free_busy_status: str = Field("busy", description="日程占用的忙闲状态，新建日程默认为 busy"),
        recurrence: str = Field("", description="重复规则，如FREQ=DAILY;INTERVAL=1"),
        app_id: Optional[str] = Field(None, description="应用唯一标识"),
        app_secret: Optional[str] = Field(None, description="应用密钥"),
):
    """
    创建飞书日历日程

    Args:
        app_id: 应用ID
        app_secret: 应用密钥
        summary: 日程标题
        description: 日程描述
        need_notification: 是否需要通知
        start_date: 开始日期，格式YYYY-MM-DD
        start_timestamp: 开始时间戳
        end_date: 结束日期，格式YYYY-MM-DD
        end_timestamp: 结束时间戳
        timezone: 时区设置
        visibility: 可见性设置
        attendee_ability: 参与者权限
        free_busy_status: 忙闲状态
        recurrence: 重复规则
        attendees: 参会者列表
        user_id_type: 用户id类型
        location_name: 日程的地点名称, 如301会议室
        location_address: 日程的会议地点地址，如公司大楼一楼

    Returns:
        日程创建成功返回日程信息，失败返回错误信息
    """
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .build()

    # 获取一个公共日历
    calendar_id = get_primary_calendar(app_id, app_secret)

    # 构造请求对象
    request: CreateCalendarEventRequest = CreateCalendarEventRequest.builder() \
        .calendar_id(calendar_id) \
        .idempotency_key(uuid.uuid4().hex) \
        .user_id_type(user_id_type) \
        .request_body(CalendarEvent.builder()
                      .summary(summary)
                      .description(description)
                      .need_notification(need_notification)
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
    response: CreateCalendarEventResponse = client.calendar.v4.calendar_event.create(request)

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
    calendar_event_message = lark.JSON.marshal(response.data, indent=4)
    lark.logger.info(calendar_event_message)

    # 参会人处理（如果有参会人）
    event_attendee_message = ""
    if attendees:
        try:
            event_id = response.data.event.event_id
            attendee_response = append_calendar_event_attendee(
                app_id=app_id,
                app_secret=app_secret,
                event_id=event_id,
                calendar_id=calendar_id,
                user_id_type=user_id_type,
                attendees=attendees,
                need_notification=need_notification
            )
            event_attendee_message = lark.JSON.marshal(attendee_response, indent=4)
            lark.logger.info(event_attendee_message)
        except Exception as err:
            error_msg = f"添加参会人失败: {str(err)}"
            lark.logger.error(error_msg)
            # 这里根据业务需求决定：是忽略错误继续返回基础事件信息，还是直接返回错误
            # 当前选择忽略错误继续返回，可根据实际情况调整
            # return error_msg

    # 返回组合结果
    return calendar_event_message + event_attendee_message if event_attendee_message else calendar_event_message
