import enum
from django.db import models
from django.contrib.auth.models import User
from .services import DifficultyLevel

class ScoreState(enum.Enum):
    IN_PRORGESS = 'in_progress'
    COMPLETED = 'completed'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
    @classmethod
    def max_length(cls):
        lengths = [len(key.name) for key in cls]
        return max(lengths)

class ScoreModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(choices=DifficultyLevel.choices(), max_length=DifficultyLevel.max_length())
    status = models.CharField(choices=ScoreState.choices(), max_length=ScoreState.max_length())
    solved_board_hash = models.CharField(max_length=64)
    total_playtime = models.IntegerField()
    

class SessionState(enum.Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
    @classmethod
    def max_length(cls):
        lengths = [len(key.name) for key in cls]
        return max(lengths)
    
class SessionModel(models.Model):
    score_id = models.ForeignKey(ScoreModel, on_delete=models.CASCADE)
    status = models.CharField(choices=SessionState.choices(), max_length=SessionState.max_length())
    board_state = models.JSONField()
    solved_board = models.JSONField()
    started_at = models.CharField("", max_length=50)
    fail_count = models.IntegerField()
    
    
    