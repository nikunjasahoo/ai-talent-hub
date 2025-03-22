from typing import Dict, Any, List
from crewai import Agent, Task


class EmailAutomation:
    """
    Agent that automates email communications with candidates and hiring teams.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Email Automation agent.
        
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
        Create a task for generating emails.
        
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
            output: Task output (generated emails)
        """
        print("\n" + "="*50)
        print("Email Templates Generated:")
        print("="*50)
        print(output)
        print("="*50)
    
    def generate_candidate_email(self, job_title: str, candidate_name: str, is_selected: bool) -> str:
        """
        Generate an email for a candidate.
        
        Args:
            job_title: Title of the job
            candidate_name: Name of the candidate
            is_selected: Whether the candidate is selected for interview
            
        Returns:
            str: Generated email content
        """
        email_type = "selection" if is_selected else "rejection"
        
        prompt = f"""
        Generate a professional email to {candidate_name} regarding their application for the {job_title} position.
        
        This is a {email_type} email.
        
        If this is a selection email, include:
        1. Congratulations on being selected for an interview
        2. Brief mention of their qualifications that stood out
        3. Next steps in the interview process
        4. Request to confirm availability
        
        If this is a rejection email, include:
        1. Appreciation for their application
        2. Gentle rejection language
        3. Encouragement for future applications
        4. Best wishes for their job search
        
        The email should be professional, warm, and concise.
        """
        
        return self.agent.execute_task(prompt)
    
    def generate_hiring_team_email(self, job_title: str, candidate_names: List[str]) -> str:
        """
        Generate an email to the hiring team with candidate information.
        
        Args:
            job_title: Title of the job
            candidate_names: List of selected candidate names
            
        Returns:
            str: Generated email content
        """
        candidates_str = ", ".join(candidate_names)
        
        prompt = f"""
        Generate a professional email to the hiring team regarding candidates for the {job_title} position.
        
        The following candidates have been selected for interviews: {candidates_str}
        
        The email should include:
        1. Introduction to the selected candidates
        2. Request for the team to review the provided resumes
        3. Ask for their availability for interview panels
        4. Next steps in the hiring process
        
        The email should be professional, concise, and action-oriented.
        """
        
        return self.agent.execute_task(prompt)
    
    def mock_send_email(self, recipient: str, subject: str, content: str) -> Dict[str, Any]:
        """
        Mock sending an email by printing the details.
        
        Args:
            recipient: Email recipient
            subject: Email subject
            content: Email content
            
        Returns:
            Dict[str, Any]: Status information about the "sent" email
        """
        print(f"\nEMAIL TO: {recipient}")
        print(f"SUBJECT: {subject}")
        print(f"CONTENT:\n{content}")
        
        return {
            "recipient": recipient,
            "subject": subject,
            "status": "sent (mocked)",
            "timestamp": "2023-xx-xx xx:xx:xx"
        } 