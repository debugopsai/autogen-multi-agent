import os
from dotenv import load_dotenv
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

load_dotenv()


class McpConfig:

    @staticmethod
    def get_mysql_workbench():
        mysql_server_params = StdioServerParams(
            command="/Users/codeclouds-shahrukh/.local/bin/uvx",
            args=["mysql_mcp_server"],
            env={
                "MYSQL_HOST": os.getenv("MYSQL_HOST"),
                "MYSQL_PORT": os.getenv("MYSQL_PORT"),
                "MYSQL_USER": os.getenv("MYSQL_USER"),
                "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
                "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE")
            },
            read_timeout_seconds=60
        )
        return McpWorkbench( server_params=mysql_server_params )

    @staticmethod
    def get_rest_api_workbench():
        rest_api_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": os.getenv("REST_BASE_URL"),
                "HEADER_Accept": "application/json"
            },
            read_timeout_seconds=60
        )
        return McpWorkbench( rest_api_server_params )

    @staticmethod
    def get_excel_workbench():
        excel_server_params = StdioServerParams(
            command="npx",
            args=["--yes", "@negokaz/excel-mcp-server"],
            env={
                "EXCEL_MCP_PAGING_CELLS_LIMIT": os.getenv("EXCEL_MCP_PAGING_CELLS_LIMIT", "4000")
            },
            read_timeout_seconds=60
        )
        return McpWorkbench( server_params=excel_server_params )

    @staticmethod
    def get_filesystem_workbench():
        filesystem_server_params = StdioServerParams(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", os.getenv("FILES_DIR")],
            read_timeout_seconds=60
        )
        return McpWorkbench( server_params=filesystem_server_params )
