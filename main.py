import os
import sys
import argparse
import requests
from typing import Dict, Any

from src.utils import ConfigLoader, ModelConnector, AgentFactory, WorkflowEngine


def check_ollama():
    """Check if Ollama is installed and running with the llama3.1 model."""
    try:
        # Check if Ollama service is running
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print("Ollama service is not running. Please start Ollama.")
            return False
            
        # Check if llama3.1 model is available
        models = response.json().get("models", [])
        if not any(model.get("name") == "llama3.1:latest" for model in models):
            print("llama3.1:latest model not found. Please run 'ollama pull llama3.1' to download it.")
            return False
            
        return True
    except requests.RequestException:
        print("Could not connect to Ollama. Please make sure Ollama is installed and running.")
        print("You can install Ollama from: https://ollama.ai/")
        print("After installation, run: ollama pull llama3.1")
        return False


def main():
    """Main entry point for the AI Talent Hub application."""
    parser = argparse.ArgumentParser(description="AI Talent Hub - AI-powered recruitment system")
    parser.add_argument(
        "--workflow", 
        choices=["recruitment_process", "job_posting", "candidate_selection", "interview_process"],
        default="job_posting",
        help="Workflow to run"
    )
    parser.add_argument("--job-title", default="Software Engineer", help="Job title for job description")
    parser.add_argument("--skills", default="Python, JavaScript, AWS, Docker", help="Required skills for job")
    parser.add_argument("--experience", default="3+ years", help="Required experience for job")
    parser.add_argument("--email", default="recruiter@example.com", help="Recruiter email address")
    parser.add_argument("--positions", default="1", help="Number of open positions")
    parser.add_argument("--skip-check", action="store_true", help="Skip Ollama check")
    args = parser.parse_args()
    
    # Check if Ollama is installed and running
    if not args.skip_check and not check_ollama():
        return 1
    
    # Initialize configuration and model
    print("Initializing AI Talent Hub...")
    config_loader = ConfigLoader()
    model_config = config_loader.get_model_config()
    model_connector = ModelConnector(model_config)
    
    # Create agent factory and workflow engine
    agent_factory = AgentFactory(config_loader, model_connector)
    workflow_engine = WorkflowEngine(config_loader, agent_factory)
    
    # Prepare context for the workflow
    context = {
        "job_title": args.job_title,
        "skills": args.skills,
        "experience": args.experience,
        "email": args.email,
        "positions": args.positions
    }
    
    # Run the selected workflow
    try:
        print(f"Starting workflow: {args.workflow}")
        workflow_engine.run_workflow(args.workflow, context)
    except Exception as e:
        print(f"Error running workflow: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main()) 