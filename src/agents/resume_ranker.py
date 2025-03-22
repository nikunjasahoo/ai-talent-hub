import os
from typing import Dict, Any, List
from crewai import Agent, Task
from crewai_tools import DirectoryReadTool, FileReadTool


class ResumeRanker:
    """
    Agent that ranks resumes based on their match to a job description.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Resume Ranker agent.
        
        Args:
            config: Agent configuration from YAML
            llm: Language model instance
        """
        self.config = config
        self.llm = llm
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        """Create and configure the agent."""
        # Initialize tools for reading resumes
        self.dir_tool = DirectoryReadTool(directory="./data/resumes", description="Lists all resume files in a directory")
        self.file_tool = FileReadTool(description="Reads the content of a resume file")
        
        return Agent(
            role=self.config.get("role"),
            goal=self.config.get("goal"),
            backstory=self.config.get("backstory"),
            verbose=self.config.get("verbose", True),
            allow_delegation=self.config.get("allow_delegation", False),
            tools=[self.dir_tool, self.file_tool],
            llm=self.llm
        )
    
    def create_task(self, task_config: Dict[str, Any]) -> Task:
        """
        Create a task for ranking resumes.
        
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
            output: Task output (ranked resumes)
        """
        print("\n" + "="*50)
        print("Resume Ranking Complete:")
        print("="*50)
        print(output)
        print("="*50)
    
    def rank_resumes(self, job_description: str) -> str:
        """
        Rank resumes based on their match to the job description.
        
        Args:
            job_description: Job description to match against
            
        Returns:
            str: Ranked list of resumes with scores and justification
        """
        # The tools are now embedded in the agent, so we let the agent handle the directory and file reading
        prompt = f"""
        I need you to rank candidate resumes based on their match to this job description.
        
        First, use the DirectoryReadTool to list all resume files in the 'data/resumes' directory.
        Then, use the FileReadTool to read the content of each resume file.
        
        JOB DESCRIPTION:
        {job_description}
        
        For each resume, provide:
        1. A match score from 0-100
        2. Key strengths relative to the job description
        3. Missing qualifications or weaknesses
        4. Brief justification for the score
        
        Then, provide a final ranked list from best match to worst match.
        """
        
        return self.agent.execute_task(prompt) 