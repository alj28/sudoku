
from rest_framework import serializers, status
from .services import DifficultyLevel


DIFFICULTY_LEVELS_TO_CHOICES_MAP = {
    'easy'      :   DifficultyLevel.EASY,
    'medium'    :   DifficultyLevel.MEDIUM,
    'hard'      :   DifficultyLevel.HARD
}

class GetNewGameSerializer(serializers.Serializer):
    difficulty = serializers.ChoiceField(choices=[c for c in DIFFICULTY_LEVELS_TO_CHOICES_MAP])
    
    def validate(self, data):
        data['difficulty_enumerated'] = DIFFICULTY_LEVELS_TO_CHOICES_MAP[data['difficulty']]
        return data