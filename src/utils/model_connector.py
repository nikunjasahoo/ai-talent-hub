from typing import Dict, Any, Optional
import os

from crewai import LLM


class ModelConnector:
    """A utility class to configure and connect to Ollama LLM."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the model connector with configuration.
        
        Args:
            config: Dictionary containing model configuration
        """
        self.config = config
        self.model = None
        self._configure_model()
    
    def _configure_model(self) -> None:
        """Configure the model based on the provided configuration."""
        provider = self.config.get("provider", "ollama")
        model_name = self.config.get("name", "llama3.1:latest")
        base_url = self.config.get("base_url", "http://localhost:11434")
        temperature = self.config.get("temperature", 0.7)
        max_tokens = self.config.get("max_tokens", 2000)
        
        if provider.lower() == "ollama":
            self.model = LLM(
                model=f"ollama/{model_name}",
                base_url=base_url,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError(f"Unsupported model provider: {provider}")
    
    def get_model(self) -> Any:
        """Get the configured model instance."""
        return self.model 