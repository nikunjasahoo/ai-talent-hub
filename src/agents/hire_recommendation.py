from typing import Dict, Any, Tuple, List
from crewai import Agent, Task


class HireRecommendation:
    """
    Agent that analyzes interview transcripts and provides hiring recommendations.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Hire Recommendation agent.
        
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
        Create a task for generating hire recommendations.
        
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
            output: Task output (hire recommendation)
        """
        print("\n" + "="*50)
        print("Hire Recommendation:")
        print("="*50)
        print(output)
        print("="*50)
    
    def analyze_interview(self, job_description: str, resume: str, interview_transcript: str) -> Dict[str, Any]:
        """
        Analyze an interview transcript and provide a hiring recommendation.
        
        Args:
            job_description: Job description text
            resume: Candidate's resume text
            interview_transcript: Complete interview transcript
            
        Returns:
            Dict[str, Any]: Analysis results including strengths, weaknesses, and recommendation
        """
        prompt = f"""
        Analyze this interview transcript and provide a hiring recommendation.
        
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE RESUME:
        {resume}
        
        INTERVIEW TRANSCRIPT:
        {interview_transcript}
        
        Please provide a comprehensive analysis that includes:
        
        1. Key strengths demonstrated in the interview (minimum 3)
        2. Areas for improvement or concerns (minimum 2)
        3. Alignment with job requirements (rate as Strong, Moderate, or Weak with explanation)
        4. Cultural fit assessment
        5. Technical skill assessment
        6. Final recommendation: Hire, Consider, or Do Not Hire
        7. Justification for your recommendation (3-5 sentences)
        
        Structure your response with clear headings and concise bullet points where appropriate.
        """
        
        analysis_text = self.agent.execute_task(prompt)
        
        # For a real application, we would parse the text into a structured format
        # For simplicity, we'll return it as is with a mock decision
        recommendation = self._extract_hire_decision(analysis_text)
        
        return {
            "analysis": analysis_text,
            "hire_decision": recommendation[0],
            "confidence": recommendation[1],
            "timestamp": "2023-xx-xx xx:xx:xx"
        }
    
    def _extract_hire_decision(self, analysis_text: str) -> Tuple[str, float]:
        """
        Extract the hire decision and confidence from the analysis text.
        
        Args:
            analysis_text: The full analysis text
            
        Returns:
            Tuple[str, float]: The hire decision and confidence score
        """
        # This is a simple implementation; in a real application, we would use more 
        # sophisticated NLP to extract the decision and confidence
        
        if "hire" in analysis_text.lower():
            if "do not hire" in analysis_text.lower() or "don't hire" in analysis_text.lower():
                return "Do Not Hire", 0.8
            elif "consider" in analysis_text.lower():
                return "Consider", 0.6
            else:
                return "Hire", 0.9
        elif "consider" in analysis_text.lower():
            return "Consider", 0.6
        else:
            return "No clear recommendation", 0.5 