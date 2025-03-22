from typing import Dict, Any, List
from crewai import Agent, Task


class InterviewAgent:
    """
    Agent that conducts AI-driven interviews with candidates.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Interview Agent.
        
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
        Create a task for conducting interviews.
        
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
            output: Task output (interview transcript)
        """
        print("\n" + "="*50)
        print("Interview Complete:")
        print("="*50)
        print(output)
        print("="*50)
    
    def prepare_interview_questions(self, job_description: str, resume: str) -> List[str]:
        """
        Prepare interview questions based on job description and resume.
        
        Args:
            job_description: Job description text
            resume: Candidate's resume text
            
        Returns:
            List[str]: List of tailored interview questions
        """
        prompt = f"""
        I need to create 5-7 interview questions for a candidate based on their resume and the job description.
        
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE RESUME:
        {resume}
        
        Please create questions that:
        1. Assess technical skills relevant to the job
        2. Evaluate past experience and achievements
        3. Check for cultural fit and soft skills
        4. Test problem-solving abilities with realistic scenarios
        5. Allow the candidate to demonstrate their unique strengths
        
        The questions should be detailed, specific to this candidate's background, and designed to reveal their suitability for this particular role.
        Return only the list of numbered questions without any other text.
        """
        
        questions_text = self.agent.execute_task(prompt)
        
        # Convert the text into a list of questions
        questions = []
        for line in questions_text.strip().split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line[0] == '-'):
                # Remove number/bullet and clean up
                clean_question = line.split('.', 1)[-1].strip() if '.' in line else line[1:].strip()
                questions.append(clean_question)
        
        return questions
    
    def conduct_interview(self, job_description: str, resume: str, candidate_name: str) -> str:
        """
        Conduct an AI-driven interview with simulated candidate responses.
        
        Args:
            job_description: Job description text
            resume: Candidate's resume text
            candidate_name: Name of the candidate
            
        Returns:
            str: Complete interview transcript
        """
        # In a real application, this would be an interactive session with the actual candidate
        # For demonstration, we'll simulate the interview with the AI playing both roles
        
        questions = self.prepare_interview_questions(job_description, resume)
        
        prompt = f"""
        Conduct a simulated interview with {candidate_name} for a position described as:
        
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE RESUME:
        {resume}
        
        Use these questions as the basis for the interview:
        {chr(10).join([f"{i+1}. {q}" for i, q in enumerate(questions)])}
        
        For each question:
        1. Ask the question
        2. Generate a realistic candidate response based on their resume
        3. Follow up with a relevant question based on their response
        4. Generate another realistic response
        5. Move to the next question
        
        Format the transcript with "Interviewer:" and "Candidate:" prefixes.
        Begin with a brief introduction and end with a conclusion thanking the candidate.
        Make the responses realistic, not perfect, showing both strengths and areas for improvement.
        """
        
        return self.agent.execute_task(prompt)
    
    def conduct_interactive_interview(self, job_description: str, resume: str) -> str:
        """
        Conduct an interactive interview with a real candidate.
        
        Args:
            job_description: Job description text
            resume: Candidate's resume text
            
        Returns:
            str: Complete interview transcript
        """
        questions = self.prepare_interview_questions(job_description, resume)
        transcript = ["=== INTERVIEW TRANSCRIPT ==="]
        
        print("\nStarting interactive interview. Type your responses after each question.")
        print("Type 'end interview' at any point to finish the interview.\n")
        
        for i, question in enumerate(questions):
            # Ask the question
            print(f"\nInterviewer: {question}")
            transcript.append(f"Interviewer: {question}")
            
            # Get candidate response
            response = input("Your response: ")
            if response.lower() == "end interview":
                break
            transcript.append(f"Candidate: {response}")
            
            # Generate a follow-up question based on the response
            if i < len(questions) - 1:  # If not the last question
                follow_up_prompt = f"""
                Based on the candidate's response:
                "{response}"
                
                Generate a thoughtful follow-up question that digs deeper into their answer
                before moving on to the next main question. Keep it brief and focused.
                """
                
                follow_up = self.agent.execute_task(follow_up_prompt)
                print(f"Interviewer: {follow_up}")
                transcript.append(f"Interviewer: {follow_up}")
                
                # Get candidate's follow-up response
                follow_up_response = input("Your response: ")
                if follow_up_response.lower() == "end interview":
                    break
                transcript.append(f"Candidate: {follow_up_response}")
        
        print("\nInterview complete. Thank you for your time.")
        transcript.append("Interviewer: Thank you for your time today. We'll be in touch soon regarding next steps.")
        
        return "\n".join(transcript) 