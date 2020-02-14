import requests
import requests_mock

payload = {
    "quizSubject": [
        "sports",
        "math"
    ],
    "semester": "2"
}

adapter = requests_mock.Adapter()
session = requests.Session()
session.mount('mock', adapter)


def request_callback(request, context):
    request.json = payload
    context.status_code = 200
    with open('input_response.txt', 'r') as response_file:
        api_response = \
            response_file.read()
    return api_response


def mock_api_url_response():
    """
    Mocks the API request to the url: https://validate.test.com/api/quiz-questions with status code as 200
    and response from the file input_response.txt which was given as the reference.
    request_callback is the function which returns the response object.

    """
    adapter.register_uri('POST', 'mock://https://validate.test.com/api/quiz-questions', json=request_callback)
    resp = session.post('mock://https://validate.test.com/api/quiz-questions', json=payload)
    return resp
