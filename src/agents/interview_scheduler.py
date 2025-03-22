from typing import Dict, Any, List
from crewai import Agent, Task
import datetime
import json


class InterviewScheduler:
    """
    Agent that schedules interviews and sends calendar invites.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Interview Scheduler agent.
        
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
        Create a task for scheduling interviews.
        
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
            output: Task output (scheduled interviews)
        """
        print("\n" + "="*50)
        print("Interview Scheduling Complete:")
        print("="*50)
        print(output)
        print("="*50)
    
    def schedule_interview(self, candidate_name: str, job_title: str, interviewers: List[str], 
                           candidate_availability: List[str] = None) -> Dict[str, Any]:
        """
        Schedule an interview based on availability.
        
        Args:
            candidate_name: Name of the candidate
            job_title: Title of the job
            interviewers: List of interviewer names
            candidate_availability: List of datetime strings when candidate is available
            
        Returns:
            Dict[str, Any]: Interview details
        """
        if candidate_availability is None:
            # Mock some availability if none provided
            start_date = datetime.datetime.now() + datetime.timedelta(days=3)
            candidate_availability = [
                (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d %H:00:00")
                for i in range(5)
            ]
        
        prompt = f"""
        Schedule an interview for {candidate_name} for the {job_title} position.
        
        The interview panel includes: {', '.join(interviewers)}
        
        The candidate is available on the following dates/times:
        {json.dumps(candidate_availability, indent=2)}
        
        Based on the information provided:
        1. Select the best date and time for the interview
        2. Determine the interview format (in-person, video call, etc.)
        3. Decide on the interview duration
        4. Prepare any specific instructions for the candidate
        
        Provide a response that includes all these details in a structured format.
        """
        
        scheduling_result = self.agent.execute_task(prompt)
        
        # For demonstration purposes, we'll mock a calendar invite
        calendar_invite = self.mock_calendar_invite(
            candidate_name=candidate_name,
            job_title=job_title,
            interviewers=interviewers,
            scheduling_details=scheduling_result
        )
        
        return {
            "candidate": candidate_name,
            "job_title": job_title,
            "interviewers": interviewers,
            "scheduling_details": scheduling_result,
            "calendar_invite": calendar_invite
        }
    
    def mock_calendar_invite(self, candidate_name: str, job_title: str, 
                             interviewers: List[str], scheduling_details: str) -> Dict[str, Any]:
        """
        Mock sending a Google Calendar invite.
        
        Args:
            candidate_name: Name of the candidate
            job_title: Title of the job
            interviewers: List of interviewer names
            scheduling_details: Details from the scheduling task
            
        Returns:
            Dict[str, Any]: Mock calendar invite details
        """
        # In a real application, this would use the Google Calendar API
        # For now, we'll just return a mock representation
        
        print(f"\nMOCK CALENDAR INVITE:")
        print(f"Title: Interview for {job_title} with {candidate_name}")
        print(f"Attendees: {candidate_name}, {', '.join(interviewers)}")
        print(f"Details: {scheduling_details}")
        
        return {
            "event_id": "mock-event-id-12345",
            "title": f"Interview for {job_title} with {candidate_name}",
            "attendees": [candidate_name] + interviewers,
            "details": scheduling_details,
            "status": "created (mocked)"
        } 