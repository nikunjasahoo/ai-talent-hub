from typing import Dict, Any, Optional

from src.agents import (
    JobDescriptionGenerator,
    ResumeRanker,
    EmailAutomation,
    InterviewScheduler,
    InterviewAgent,
    HireRecommendation,
    SentimentAnalyzer
)


class AgentFactory:
    """Factory for creating agent instances from configuration."""
    
    def __init__(self, config_loader, model_connector):
        """
        Initialize the agent factory.
        
        Args:
            config_loader: Configuration loader instance
            model_connector: Model connector instance
        """
        self.config_loader = config_loader
        self.model_connector = model_connector
        self.llm = model_connector.get_model()
        self.agent_instances = {}
    
    def get_agent(self, agent_id: str):
        """
        Get or create an agent instance by ID.
        
        Args:
            agent_id: ID of the agent to create/retrieve
            
        Returns:
            Agent instance
        """
        if agent_id in self.agent_instances:
            return self.agent_instances[agent_id]
        
        agent_config = self.config_loader.get_agent_config(agent_id)
        if not agent_config:
            raise ValueError(f"No configuration found for agent ID: {agent_id}")
        
        agent_instance = self._create_agent_instance(agent_id, agent_config)
        self.agent_instances[agent_id] = agent_instance
        
        return agent_instance
    
    def create_task(self, task_id: str):
        """
        Create a task from a task ID.
        
        Args:
            task_id: ID of the task to create
            
        Returns:
            Task instance
        """
        task_config = self.config_loader.get_task_config(task_id)
        if not task_config:
            raise ValueError(f"No configuration found for task ID: {task_id}")
        
        agent_id = task_config.get("agent")
        if not agent_id:
            raise ValueError(f"No agent specified for task ID: {task_id}")
        
        agent_instance = self.get_agent(agent_id)
        return agent_instance.create_task(task_config)
    
    def _create_agent_instance(self, agent_id: str, agent_config: Dict[str, Any]):
        """
        Create an agent instance based on agent ID and configuration.
        
        Args:
            agent_id: ID of the agent
            agent_config: Agent configuration
            
        Returns:
            Agent instance
        """
        agent_map = {
            "job_description_generator": JobDescriptionGenerator,
            "resume_ranker": ResumeRanker,
            "email_automation": EmailAutomation,
            "interview_scheduler": InterviewScheduler,
            "interview_agent": InterviewAgent,
            "hire_recommendation": HireRecommendation,
            "sentiment_analyzer": SentimentAnalyzer
        }
        
        agent_class = agent_map.get(agent_id)
        if not agent_class:
            raise ValueError(f"Unknown agent type for ID: {agent_id}")
        
        return agent_class(agent_config, self.llm) 