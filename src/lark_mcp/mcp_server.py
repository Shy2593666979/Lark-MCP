from lark_mcp.mcp_tool.batch_get_id_user import get_id_user_request
from lark_mcp.mcp_tool import contact_v3_user_batch
from lark_mcp.mcp_tool import create_chats
from lark_mcp.mcp_tool import create_document
from lark_mcp.mcp_tool.create_folder import create_folder
from lark_mcp.mcp_tool import delete_chat
from lark_mcp.mcp_tool import get_chat_data
from lark_mcp.mcp_tool.get_document_data import get_document
from lark_mcp.mcp_tool.im_v1_chats import create_message
from lark_mcp.mcp_tool import list_files
from mcp.server.fastmcp import FastMCP


def register_mcp_server(mcp: FastMCP):
    mcp.tool(description=get_id_user_request.__doc__)(get_id_user_request)
    mcp.tool(description=contact_v3_user_batch.__doc__)(contact_v3_user_batch)
    mcp.tool(description=create_chats.__doc__)(create_chats)
    mcp.tool(description=create_document.__doc__)(create_document)
    mcp.tool(description=create_folder.__doc__)(create_folder)
    mcp.tool(description=delete_chat.__doc__)(delete_chat)
    mcp.tool(description=get_chat_data.__doc__)(get_chat_data)
    mcp.tool(description=get_document.__doc__)(get_document)
    mcp.tool(description=create_message.__doc__)(create_message)
    mcp.tool(description=list_files.__doc__)(list_files)