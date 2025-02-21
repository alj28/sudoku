from copy import copy
from django.urls import reverse
from unittest.mock import patch, Mock
from django.test import TestCase

GET_NEW_GAME_URL = reverse('get_new_game')

THIRD_PARTY_API_VALID_RESPONSE_1 = {
    "difficulty": "medium",
    "puzzle": [
        ["0","0","0","1","0","0","5","0","0"],
        ["0","3","1","0","9","0","2","4","6"],
        ["0","9","0","0","2","4","3","8","0"],
        ["0","1","0","0","0","0","0","2","4"],
        ["0","0","5","0","0","0","0","0","9"],
        ["9","0","0","0","4","0","7","0","5"],
        ["4","0","2","0","0","0","0","7","0"],
        ["0","0","0","3","0","0","0","1","0"],
        ["0","0","0","4","7","0","6","0","0"]
    ],
    "solution": [
        ["8","2","4","1","3","6","5","9","7"],
        ["5","3","1","8","9","7","2","4","6"],
        ["7","9","6","5","2","4","3","8","1"],
        ["3","1","7","9","6","5","8","2","4"],
        ["2","4","5","7","8","3","1","6","9"],
        ["9","6","8","2","4","1","7","3","5"],
        ["4","5","2","6","1","8","9","7","3"],
        ["6","7","9","3","5","2","4","1","8"],
        ["1","8","3","4","7","9","6","5","2"]
    ]
}

THIRD_PARTY_API_VALID_RESPONSE_3 = {
    "difficulty": "medium",
    "puzzle": [
        ["6","0","0","0","0","5","7","3","0"],
        ["0","7","0","0","0","3","2","0","5"],
        ["0","0","0","7","2","0","9","0","0"],
        ["0","0","1","0","0","0","0","0","0"],
        ["7","0","0","8","6","0","3","0","0"],
        ["0","0","3","0","0","9","0","8","0"],
        ["9","0","0","0","3","0","0","5","1"],
        ["0","0","7","0","8","0","0","0","0"],
        ["0","4","6","1","0","0","8","7","0"]
    ],
    "solution": [
        ["6","1","2","9","4","5","7","3","8"],
        ["8","7","9","6","1","3","2","4","5"],
        ["3","5","4","7","2","8","9","1","6"],
        ["2","8","1","3","7","4","5","6","9"],
        ["7","9","5","8","6","1","3","2","4"],
        ["4","6","3","2","5","9","1","8","7"],
        ["9","2","8","4","3","7","6","5","1"],
        ["1","3","7","5","8","6","4","9","2"],
        ["5","4","6","1","9","2","8","7","3"]
    ]
}

THIRD_PARTY_API_VALID_RESPONSE_4 = {
    "difficulty": "medium",
    "puzzle": [
        ["0","0","0","0","0","0","0","8","4"],
        ["4","8","0","7","2","1","5","0","0"],
        ["3","0","0","0","0","0","6","2","7"],
        ["0","0","0","0","9","3","0","0","0"],
        ["7","4","8","0","5","0","3","1","0"],
        ["0","3","0","0","0","0","4","0","0"],
        ["0","5","0","0","0","7","0","0","0"],
        ["0","0","0","9","6","0","0","5","1"],
        ["0","0","0","0","1","0","0","0","6"]
    ],
    "solution": [
        ["5","2","7","6","3","9","1","8","4"],
        ["4","8","6","7","2","1","5","9","3"],
        ["3","1","9","8","4","5","6","2","7"],
        ["1","6","5","4","9","3","2","7","8"],
        ["7","4","8","2","5","6","3","1","9"],
        ["9","3","2","1","7","8","4","6","5"],
        ["6","5","1","3","8","7","9","4","2"],
        ["2","7","3","9","6","4","8","5","1"],
        ["8","9","4","5","1","2","7","3","6"]
    ]
}

import json
# Create your tests here.
class GetNewGameViewTest(TestCase):
    
    @patch('requests.post')
    def test_success(self, mock_request):
        # Prepare mock response object
        mock_response = mock_request.return_value
        mock_response.status_code = 200
        mock_response.text = json.dumps(THIRD_PARTY_API_VALID_RESPONSE_1)
       
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   'medium'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['board'], THIRD_PARTY_API_VALID_RESPONSE_1['puzzle'])
        self.assertEqual(response.data['solution'], THIRD_PARTY_API_VALID_RESPONSE_1['solution'])
        
    @patch('requests.post')
    def test_invalid_request(self, mock_request):
        # missing payload
        response = self.client.post(
            GET_NEW_GAME_URL
        )
        self.assertEqual(response.status_code, 400)
        
        # not allowed methods
        def test_not_allowed_method(method):
            response = method(
                GET_NEW_GAME_URL,
                {'difficulty'   :   'medium'}
                
            )
            self.assertEqual(response.status_code, 405)
        test_not_allowed_method(self.client.put)
        test_not_allowed_method(self.client.patch)
        test_not_allowed_method(self.client.get)
        test_not_allowed_method(self.client.delete)
        
        # invalid payload
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty-123'   :   'medium'}
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   'medium-123'}
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   123}
        )
        self.assertEqual(response.status_code, 400)

        
    @patch('requests.post')
    def test_external_api_fail(self, mock_request):
        # internal error
        mock_response = mock_request.return_value
        mock_response.status_code = 500
        mock_response.text = json.dumps(THIRD_PARTY_API_VALID_RESPONSE_1)
       
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   'medium'}
        )
        self.assertEqual(response.status_code, 503)
        
        # no response payload
        mock_response = mock_request.return_value
        mock_response.status_code = 200
        mock_response.text = ""
       
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   'medium'}
        )
        self.assertEqual(response.status_code, 500)
        
        # format error of the response payload
        mock_response = mock_request.return_value
        mock_response.status_code = 200
        mock_response.text = json.dumps(THIRD_PARTY_API_VALID_RESPONSE_1) + '1'
       
        response = self.client.post(
            GET_NEW_GAME_URL,
            {'difficulty'   :   'medium'}
        )
        self.assertEqual(response.status_code, 500)

