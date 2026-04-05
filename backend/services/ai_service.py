"""
AI Inference Service for running local AI tasks.
Supports text classification and simple image recognition.
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIInferenceService:
    """Service for running AI inference tasks locally."""
    
    def __init__(self):
        self.model_loaded = False
        self.model = None
        self.tokenizer = None
    
    def load_model(self, model_name: str = "distilbert-base-uncased"):
        """Load an AI model for inference."""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model_loaded = True
            logger.info(f"Loaded model: {model_name}")
            return True
        except Exception as e:
            logger.warning(f"Could not load model {model_name}: {e}")
            logger.info("Will use mock inference instead")
            return False
    
    async def run_task(self, task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run an AI inference task."""
        if task_type == "text_classification":
            return await self.classify_text(input_data)
        elif task_type == "sentiment_analysis":
            return await self.analyze_sentiment(input_data)
        elif task_type == "image_recognition":
            return await self.recognize_image(input_data)
        elif task_type == "mock_inference":
            return await self.mock_inference(input_data)
        else:
            return {
                "success": False,
                "error": f"Unknown task type: {task_type}"
            }
    
    async def classify_text(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify text into categories."""
        text = input_data.get("text", "")
        
        if not text:
            return {"success": False, "error": "No text provided"}
        
        if self.model_loaded and self.model and self.tokenizer:
            try:
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
                outputs = self.model(**inputs)
                predictions = outputs.logits.softmax(dim=1).tolist()[0]
                
                return {
                    "success": True,
                    "task_type": "text_classification",
                    "input": text,
                    "predictions": predictions[:5],  # Top 5 predictions
                    "model_used": "distilbert-base-uncased"
                }
            except Exception as e:
                logger.error(f"Text classification error: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Mock response
            return {
                "success": True,
                "task_type": "text_classification",
                "input": text,
                "predictions": [0.7, 0.2, 0.05, 0.03, 0.02],
                "labels": ["positive", "negative", "neutral", "question", "other"],
                "model_used": "mock",
                "note": "This is a mock response. Install transformers for real inference."
            }
    
    async def analyze_sentiment(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment of text."""
        text = input_data.get("text", "")
        
        if not text:
            return {"success": False, "error": "No text provided"}
        
        # Simple heuristic-based sentiment analysis (mock)
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "happy"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "worst"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "success": True,
            "task_type": "sentiment_analysis",
            "input": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_score": positive_count / max(1, positive_count + negative_count),
            "negative_score": negative_count / max(1, positive_count + negative_count),
            "model_used": "heuristic"
        }
    
    async def recognize_image(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize objects in an image."""
        # For MVP, we'll mock this since actual image recognition requires heavy models
        image_url = input_data.get("url", "")
        image_data = input_data.get("data", "")
        
        if not image_url and not image_data:
            return {"success": False, "error": "No image provided"}
        
        # Mock response
        mock_labels = [
            {"label": "object", "confidence": 0.85},
            {"label": "scene", "confidence": 0.72},
            {"label": "person", "confidence": 0.65}
        ]
        
        return {
            "success": True,
            "task_type": "image_recognition",
            "labels": mock_labels,
            "model_used": "mock",
            "note": "Install torchvision/torch for real image recognition"
        }
    
    async def mock_inference(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a mock inference for testing."""
        import time
        import random
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        return {
            "success": True,
            "task_type": "mock_inference",
            "input": input_data,
            "output": {
                "result": "mock_result",
                "confidence": random.uniform(0.7, 0.99)
            },
            "processing_time_ms": random.randint(50, 500),
            "model_used": "mock"
        }


# Import asyncio for mock inference
import asyncio

# Singleton instance
_ai_service: Optional[AIInferenceService] = None


def get_ai_service() -> AIInferenceService:
    """Get or create the AI inference service singleton."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIInferenceService()
    return _ai_service
