from typing import Dict, Any
from crewai import Agent, Task


class JobDescriptionGenerator:
    """
    Agent that generates job descriptions based on provided requirements.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Job Description Generator agent.
        
        Args:
            config: Agent configuration from YAML
            llm: Language model instance
        """
        self.config = config
        self.llm = llm
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        """Create and configure the agent."""
        return Agent(
            role=self.config.get("role"),
            goal=self.config.get("goal"),
            backstory=self.config.get("backstory"),
            verbose=self.config.get("verbose", True),
            allow_delegation=self.config.get("allow_delegation", False),
            llm=self.llm
        )
    
    def create_task(self, task_config: Dict[str, Any]) -> Task:
        """
        Create a task for generating a job description.
        
        Args:
            task_config: Task configuration from YAML
            
        Returns:
            Task: Configured task instance
        """
        return Task(
            description=task_config.get("description"),
            expected_output=task_config.get("expected_output"),
            agent=self.agent,
            human_input_mode="ALWAYS" if task_config.get("human_input_required", False) else "NEVER",
            callback=self._task_callback
        )
    
    def _task_callback(self, output: str) -> None:
        """
        Callback function for task completion.
        
        Args:
            output: Task output (generated job description)
        """
        print("\n" + "="*50)
        print("Job Description Generated:")
        print("="*50)
        print(output)
        print("="*50)
        
    def generate_job_description(self, title: str, skills: str, experience: str) -> str:
        """
        Generate a job description based on the provided information.
        
        Args:
            title: Job title
            skills: Required skills
            experience: Required experience
            
        Returns:
            str: Generated job description
        """
        prompt = f"""
        Create a comprehensive job description for a {title} position.
        
        Required Skills:
        {skills}
        
        Experience Required:
        {experience}
        
        The job description should include:
        1. A compelling overview of the role
        2. Key responsibilities
        3. Required qualifications
        4. Preferred qualifications
        5. Benefits and perks
        6. Company overview
        7. Equal opportunity statement
        
        Make the job description engaging, professional, and thorough.
        """
        
        return self.agent.execute_task(prompt) 