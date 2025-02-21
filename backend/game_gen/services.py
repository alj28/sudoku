import json
import requests
import enum
from dataclasses import dataclass, asdict
from backend.settings import THIRD_PARTY_SUDOKU_GEN_API_URL

SUDOKU_GEN_URL = THIRD_PARTY_SUDOKU_GEN_API_URL

class DifficultyLevel(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class RequestBody:
    difficulty: DifficultyLevel
    solution: bool = True
    array: bool = True

@dataclass
class SudokuGame:
    board: list
    solution: list
    difficulty_level: DifficultyLevel

def generate_sudoku_game(difficulty: DifficultyLevel) -> SudokuGame:
    headers = {"Content-Type" : "application/json"}
    request_body = asdict(RequestBody(difficulty.value))
    try:
        response = requests.post(
            url=SUDOKU_GEN_URL,
            json=request_body,
            headers=headers
        )
    except:
        raise ConnectionError('Third-party API not accessible')
    
    if 200 != response.status_code:
        raise ConnectionError('Third-party API not accessible')

    # if response is invalid, it will throw JSONDecodeError
    data = json.loads(response.text)
  
    try:
        output = SudokuGame(
            board=data['puzzle'],
            solution=data['solution'],
            difficulty_level=data['difficulty']
        )
    except:
        raise ValueError('Invalid format of the response.')
    return output
    

