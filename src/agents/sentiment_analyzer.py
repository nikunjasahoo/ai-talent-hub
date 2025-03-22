from typing import Dict, Any, List
from crewai import Agent, Task


class SentimentAnalyzer:
    """
    Agent that analyzes interview transcripts for sentiment and emotional tone.
    """
    
    def __init__(self, config: Dict[str, Any], llm):
        """
        Initialize the Sentiment Analyzer agent.
        
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
        Create a task for sentiment analysis.
        
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
            output: Task output (sentiment analysis)
        """
        print("\n" + "="*50)
        print("Sentiment Analysis Complete:")
        print("="*50)
        print(output)
        print("="*50)
    
    def analyze_sentiment(self, interview_transcript: str) -> Dict[str, Any]:
        """
        Analyze the sentiment and emotional tone of an interview transcript.
        
        Args:
            interview_transcript: Complete interview transcript
            
        Returns:
            Dict[str, Any]: Sentiment analysis results
        """
        prompt = f"""
        Analyze the sentiment and emotional tone of this interview transcript.
        
        INTERVIEW TRANSCRIPT:
        {interview_transcript}
        
        Please provide a detailed analysis that includes:
        
        1. Overall sentiment (positive, negative, or neutral)
        2. Confidence level of the candidate (high, medium, or low) with examples
        3. Emotional patterns throughout the interview (e.g., started nervous but became more confident)
        4. Key moments of positive and negative sentiment
        5. Verbal cues that indicate the candidate's emotional state
        6. Signs of enthusiasm for the role/company
        7. Indications of stress or discomfort
        8. Overall emotional intelligence assessment
        
        For each point, provide specific examples from the transcript that support your analysis.
        Structure your response with clear headings and bullet points where appropriate.
        """
        
        sentiment_analysis = self.agent.execute_task(prompt)
        
        # For a real application, we would parse this into a structured format
        # For simplicity, we'll return it as is with a mock sentiment score
        sentiment_score = self._extract_sentiment_score(sentiment_analysis)
        
        return {
            "analysis": sentiment_analysis,
            "sentiment_score": sentiment_score,
            "timestamp": "2023-xx-xx xx:xx:xx"
        }
    
    def _extract_sentiment_score(self, analysis_text: str) -> Dict[str, float]:
        """
        Extract sentiment scores from the analysis text.
        
        Args:
            analysis_text: The full sentiment analysis text
            
        Returns:
            Dict[str, float]: Sentiment scores
        """
        # This is a simple implementation; in a real application, we would use 
        # sophisticated NLP to extract accurate sentiment scores
        
        scores = {
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 0.0,
            "confidence": 0.0
        }
        
        text_lower = analysis_text.lower()
        
        # Simple keyword matching for demonstration
        if "positive" in text_lower:
            scores["positive"] = 0.7
            scores["negative"] = 0.1
            scores["neutral"] = 0.2
        elif "negative" in text_lower:
            scores["positive"] = 0.2
            scores["negative"] = 0.7
            scores["neutral"] = 0.1
        else:
            scores["positive"] = 0.3
            scores["negative"] = 0.2
            scores["neutral"] = 0.5
            
        if "high confidence" in text_lower:
            scores["confidence"] = 0.8
        elif "medium confidence" in text_lower or "moderate confidence" in text_lower:
            scores["confidence"] = 0.5
        elif "low confidence" in text_lower:
            scores["confidence"] = 0.2
        else:
            scores["confidence"] = 0.4
            
        return scores 