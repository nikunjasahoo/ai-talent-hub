import yaml
import os
from typing import Dict, Any, List, Optional


class ConfigLoader:
    """Utility class to load and manage YAML configurations."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize with the configuration directory path."""
        self.config_dir = config_dir
        self.agents_config = None
        self.workflows_config = None
        self._load_configs()
    
    def _load_configs(self) -> None:
        """Load all configuration files."""
        self.agents_config = self._load_yaml(os.path.join(self.config_dir, "agents.yaml"))
        self.workflows_config = self._load_yaml(os.path.join(self.config_dir, "workflows.yaml"))
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load a YAML file into a dictionary."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get the model configuration."""
        return self.agents_config.get("model", {})
    
    def get_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific agent."""
        return self.agents_config.get("agents", {}).get(agent_id)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all agent configurations."""
        return self.agents_config.get("agents", {})
    
    def get_task_config(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific task."""
        return self.agents_config.get("tasks", {}).get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Any]:
        """Get all task configurations."""
        return self.agents_config.get("tasks", {})
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific workflow."""
        return self.workflows_config.get("workflows", {}).get(workflow_id)
    
    def get_all_workflows(self) -> Dict[str, Any]:
        """Get all workflow configurations."""
        return self.workflows_config.get("workflows", {})
    
    def get_workflow_tasks(self, workflow_id: str) -> List[str]:
        """Get the list of task IDs for a specific workflow."""
        workflow = self.get_workflow(workflow_id)
        if workflow:
            return workflow.get("tasks", [])
        return [] 