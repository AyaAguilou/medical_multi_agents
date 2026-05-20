"""MCP Server for Medical Multi-Agents"""

import json
import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPServer:
    """Base Model Context Protocol Server"""
    
    def __init__(self, name: str = "MedicalMCPServer", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, callable] = {}
        self.resources: Dict[str, Any] = {}
        logger.info(f"Initialized {name} v{version}")
    
    def register_tool(self, name: str, func: callable, description: str = ""):
        """Register a tool that can be called by agents"""
        self.tools[name] = {
            "function": func,
            "description": description
        }
        logger.info(f"Registered tool: {name}")
    
    def register_resource(self, name: str, data: Any, description: str = ""):
        """Register a resource that can be accessed by agents"""
        self.resources[name] = {
            "data": data,
            "description": description
        }
        logger.info(f"Registered resource: {name}")
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {"name": name, "description": tool["description"]}
            for name, tool in self.tools.items()
        ]
    
    def list_resources(self) -> List[Dict[str, str]]:
        """List all available resources"""
        return [
            {"name": name, "description": res["description"]}
            for name, res in self.resources.items()
        ]
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        """Call a registered tool with arguments"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        try:
            result = tool["function"](**(arguments or {}))
            logger.info(f"Tool '{tool_name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            raise
    
    def get_resource(self, resource_name: str) -> Any:
        """Get a registered resource"""
        if resource_name not in self.resources:
            raise ValueError(f"Resource '{resource_name}' not found")
        
        return self.resources[resource_name]["data"]
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP protocol request"""
        method = request.get("method")
        params = request.get("params", {})
        
        try:
            if method == "list_tools":
                return {"result": self.list_tools()}
            elif method == "list_resources":
                return {"result": self.list_resources()}
            elif method == "call_tool":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.call_tool(tool_name, arguments)
                return {"result": result}
            elif method == "get_resource":
                resource_name = params.get("name")
                data = self.get_resource(resource_name)
                return {"result": data}
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            logger.error(f"Request handling error: {str(e)}")
            return {"error": str(e)}


def main():
    """Main entry point for MCP Server"""
    server = MCPServer("MedicalMCPServer", "1.0.0")
    
    # Register example tools
    def get_patient_info(patient_id: str) -> Dict[str, str]:
        """Get patient information"""
        return {"patient_id": patient_id, "status": "stub"}
    
    def diagnose(symptoms: str) -> Dict[str, str]:
        """Run diagnostic analysis"""
        return {"symptoms": symptoms, "diagnosis": "pending"}
    
    server.register_tool("get_patient_info", get_patient_info, "Retrieve patient information by ID")
    server.register_tool("diagnose", diagnose, "Run diagnostic analysis on patient symptoms")
    
    # Register example resources
    server.register_resource("patient_database", {"count": 0}, "Patient database storage")
    server.register_resource("diagnostic_rules", {}, "Diagnostic rules engine")
    
    logger.info(f"{server.name} ready with {len(server.tools)} tools and {len(server.resources)} resources")
    return server


if __name__ == "__main__":
    server = main()
    # Can be extended to run as a server (e.g., with uvicorn, etc.)
    print(json.dumps({"status": "MCP Server initialized", "tools": server.list_tools()}, indent=2))
