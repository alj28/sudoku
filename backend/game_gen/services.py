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
      
    EXPECTED_KEYWORDS = ['puzzle', 'solution', 'difficulty']
    if not all([k in data for k in EXPECTED_KEYWORDS]):
        raise ValueError('Invalid format of the response.')
    
    if difficulty.value != data['difficulty']:
        raise ValueError('Invalid difficulty level.')
    
    def is_cell_value_valid(value_str: str) -> bool:
        try:
            value_int = int(value_str)
        except:
            return False
        return value_int in range(10)
    
    def check_matrix_and_raise_error(matrix: list):
        if list != type(matrix):
            raise ValueError('Invalid matrix format.')
        if 9 != len(matrix):
            raise ValueError('Invalid martix format.')
        for r in matrix:
            if list != type(r):
                raise ValueError('Invalid matrix format.')
            if 9 != len(r):
                raise ValueError('Invalid matrix format.')
            are_cell_values_valid = all([
                all(str == type(v) for v in r),
                all(is_cell_value_valid(v) for v in r)
            ])
            if not are_cell_values_valid:
                raise ValueError('Invalid cell value.')
    check_matrix_and_raise_error(data['puzzle'])
    check_matrix_and_raise_error(data['solution'])

  
    try:
        output = SudokuGame(
            board=data['puzzle'],
            solution=data['solution'],
            difficulty_level=data['difficulty']
        )
    except:
        raise ValueError('Invalid format of the response.')
    return output
    

