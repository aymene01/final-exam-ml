from dataclasses import dataclass
from typing import Optional


@dataclass
class Tweet:
    """Model representing a tweet in the database"""
    id: Optional[int] = None
    text: str = ""
    positive: int = 0  # 1 if positive, 0 if not
    negative: int = 0  # 1 if negative, 0 if not
    
    def to_dict(self):
        """Convert the model to a dictionary"""
        return {
            "id": self.id,
            "text": self.text,
            "positive": self.positive,
            "negative": self.negative
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a model from a dictionary"""
        return cls(
            id=data.get("id"),
            text=data.get("text", ""),
            positive=data.get("positive", 0),
            negative=data.get("negative", 0)
        ) 