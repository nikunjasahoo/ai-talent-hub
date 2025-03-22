from typing import Dict, Any, List
import re
from crewai import Crew, Task

from src.utils.agent_factory import AgentFactory


class WorkflowEngine:
    """Engine for running task workflows based on configuration."""
    
    def __init__(self, config_loader, agent_factory: AgentFactory):
        """
        Initialize the workflow engine.
        
        Args:
            config_loader: Configuration loader instance
            agent_factory: Agent factory instance
        """
        self.config_loader = config_loader
        self.agent_factory = agent_factory
    
    def run_workflow(self, workflow_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run a workflow by ID.
        
        Args:
            workflow_id: ID of the workflow to run
            context: Optional context data for the workflow
            
        Returns:
            Dict[str, Any]: Results of the workflow execution
        """
        if context is None:
            context = {}
            
        workflow_config = self.config_loader.get_workflow(workflow_id)
        if not workflow_config:
            raise ValueError(f"No configuration found for workflow ID: {workflow_id}")
        
        task_ids = workflow_config.get("tasks", [])
        tasks = []
        
        # Create tasks with context
        for task_id in task_ids:
            task_config = self.config_loader.get_task_config(task_id)
            if task_config:
                # Replace placeholders in description
                description = task_config.get("description", "")
                for key, value in context.items():
                    placeholder = f"{{{{{key}}}}}"
                    description = description.replace(placeholder, str(value))
                
                # Update task config with new description
                task_config_with_context = task_config.copy()
                task_config_with_context["description"] = description
                
                # Create task with updated config
                agent_id = task_config.get("agent")
                agent_instance = self.agent_factory.get_agent(agent_id)
                tasks.append(agent_instance.create_task(task_config_with_context))
        
        print(f"\nRunning workflow: {workflow_config.get('name')}")
        print(f"Description: {workflow_config.get('description')}")
        print(f"Tasks: {', '.join(task_ids)}\n")
        
        results = self._execute_tasks(tasks, context)
        
        print(f"\nWorkflow '{workflow_config.get('name')}' completed.")
        return results
    
    def _execute_tasks(self, tasks: List[Task], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a sequence of tasks.
        
        Args:
            tasks: List of tasks to execute
            context: Context data for the tasks
            
        Returns:
            Dict[str, Any]: Results of task execution
        """
        crew = Crew(
            tasks=tasks,
            verbose=True
        )
        
        results = crew.kickoff(inputs=context)
        return {
            "workflow_results": results,
            "context": context
        } 