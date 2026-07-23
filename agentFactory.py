from autogen_agentchat.agents import AssistantAgent

from mcp_config import McpConfig


class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig()
        self._workbenches = []

    def _track(self, workbench):
        self._workbenches.append(workbench)
        return workbench

    async def aclose(self):
        for wb in self._workbenches:
            try:
                await wb.stop()
            except Exception:
                pass
        self._workbenches.clear()

    def create_database_agent(self, system_message):
        database_agent = AssistantAgent( name="DatabaseAgent", model_client=self.model_client,
                                         workbench=self._track(self.mcp_config.get_mysql_workbench()),
                                         system_message=system_message )
        return database_agent

    def create_api_agent(self, system_message):
        rest_api_workbench = self._track(self.mcp_config.get_rest_api_workbench())
        file_system_workbench = self._track(self.mcp_config.get_filesystem_workbench())

        api_agent = AssistantAgent(name="APIAgent", model_client=self.model_client,
                                   workbench=[rest_api_workbench, file_system_workbench],
                                   system_message=system_message)
        return api_agent

    def create_excel_agent(self, system_message=None):
        excel_workbench = self._track(self.mcp_config.get_excel_workbench())

        return AssistantAgent(
            name="ExcelAgent",
            model_client=self.model_client,
            workbench=excel_workbench,
            system_message=system_message
        )


