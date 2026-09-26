"""Dynamic tool registry for binding and executing tools."""

from typing import Dict, Any, List, Optional
import pandas as pd
from tools.base_tool import BaseTool


class ToolRegistry:
    """Dynamic registry for discovering, validating, and executing tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._capability_map: Dict[str, str] = {} # capability -> tool_name

    def register_tool(self, tool: BaseTool) -> bool:
        """Register a domain tool instance."""
        if not isinstance(tool, BaseTool):
            raise TypeError("Tool must inherit from BaseTool")
        
        self._tools[tool.name] = tool
        if tool.capability:
            self._capability_map[tool.capability] = tool.name
        return True

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Retrieve registered tool by name."""
        return self._tools.get(tool_name)

    def get_tool_for_capability(self, capability_name: str) -> Optional[BaseTool]:
        """Retrieve tool associated with a passport capability."""
        tool_name = self._capability_map.get(capability_name)
        if tool_name:
            return self.get_tool(tool_name)
        return None

    def list_tools(self) -> List[Dict[str, Any]]:
        """List metadata for all registered tools."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "capability": t.capability,
            }
            for t in self._tools.values()
        ]

    def execute_tool(self, tool_name: str, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specified tool dynamically."""
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "status": "ERROR",
                "message": f"Tool '{tool_name}' not registered in registry.",
            }

        try:
            return tool.execute(df, context)
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Execution error in tool '{tool_name}': {str(e)}",
            }
