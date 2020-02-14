import ast
import pytest
import mock_leantaas_request

"""mock_leantaas_request returns the response of the fake API which was used as mock request."""

response = mock_leantaas_request.mock_api_url_response()
response_json = ast.literal_eval(response.json())

"""
Procedure followed to write the tests:
1. To simulate the request, mock api request was created with a response of 200 and expected JSON as output. 
Please refer to input_response.txt and mock_leantaas_request.py.

2. To validate the given questions,following tests were written:
        1) Validate all questions have four non null options.
        Solution:test_check_quiz_subject_has_non_null_options

        2) Validate ["New York Bulls", "Los Angeles Kings", "Golden State Warriors", "Houston Rocket"] 
        are the options for sports q1.
        Solution:test_check_sports_has_given_options
        
3.Code flow:Created a utility function get_question_dic_for_subject which returns a dictionary for the given subjects 
as input. The utility function is used in fixture :
        1.get_question_dict_for_all_subjects - This is used in most of the tests as it passes both given parameters
          as input. This is used to test the conditions for both the subjects.
        2.get_question_dict_for_sports - This is used where only sports is being passed as a parameter for question 2.
        3.get_child_json_from_key - This fixture is being used to fetch JSON object of quizSubject
"""


def test_status_code():
    """To validate if the status code of the response is 200"""
    assert response.status_code == 200


def test_response_notempty():
    """To validate if the returned response json is non-empty and valid """
    assert response_json != ''


def test_check_quiz_subject_in_response_json():
    """To validate if quizSubject is present in the API response """
    assert 'quizSubject' in response_json


def test_check_quiz_subject_is_list():
    """To validate if the quizSubject is of type: list """
    assert type(response_json['quizSubject']) is list


@pytest.mark.parametrize("question_key,expected_data_type", [("question", str), ("options", list)])
def test_check_quiz_subject_has_questions(get_question_dict_for_all_subjects, question_key, expected_data_type):
    """
    This test is to check if all the questions in the JSON are of data type: String and options are of the data
    type:list.

    """
    question_dict = get_question_dict_for_all_subjects
    for k, value in question_dict.items():
        q_num_key = 'q' + str(k + 1)
        assert type(question_dict[k][q_num_key][question_key]) is expected_data_type


def test_check_quiz_subject_has_non_null_options(get_question_dict_for_all_subjects):
    """
    To validate if all questions have four non null options.

    Input:
        get_question_dict_for_all_subjects <dict> - fixture which returns a dictionary

    Output: True or False with assertion error.

     """
    question_dict = get_question_dict_for_all_subjects
    for k, value in question_dict.items():
        q_num_key = 'q' + str(k + 1)
        assert len(question_dict[k][q_num_key]['options']) == 4
        assert all(option for option in question_dict[k][q_num_key]['options'])


@pytest.mark.parametrize("question_number,expected_options_list",
                         [("q1", ["New York Bulls", "Los Angeles Kings", "Golden State Warriors", "Houston Rocket"])])
def test_check_sports_has_given_options(get_question_dict_for_sports, question_number, expected_options_list):
    """
    To validate if q1 within sports has options with expected values.
     Input:
        get_question_dict_for_sports - Fixture which returns only sports object
        question_number  <str> - Question number passed as a parameter in parametrisation e.g "q1"
        expected_options_list <list> - The given list i.e ["New York Bulls", "Los Angeles Kings",
          "Golden State Warriors", "Houston Rocket"]

    Output:
        True or False with assertion error.
    """
    question_dict = get_question_dict_for_sports
    for k, value in question_dict.items():
        q_num_key = 'q' + str(k + 1)
        # if q_num_key == 'q1':
        if q_num_key == question_number:
            assert question_dict[k][q_num_key]['options'] == expected_options_list


def get_question_dic_for_subject(input_subject, response):
    """
    This is a utility function which is used to get the questions as an objec(dictionary) that is used in fixtures

    Input :
        input_subject <str> - eg. "sports","math"
        response <list> - Returned from fetching the value of quizSubject or any other parent key

    Output:
        returns a dictionary with keys/questions/options/answer

        eg. Output for "sports" as input

        {0:{
        'q1':{
            'question': 'Which one is correct team name in NBA?',
            'options': ['New York Bulls', 'Los Angeles Kings', 'Golden State Warriors', 'Houston Rocket'],
            'answer': 'Houston Rocket'
        }
        }}
    """
    question_list = []
    question_dict = {}

    for i in range(len(response)):
        subject = response[i]
        if input_subject in subject:
            question_list = subject[input_subject]

    for j in range(len(question_list)):
        each_question = question_list[j]
        question_dict[j] = each_question

    return question_dict


@pytest.fixture(params=["quizSubject"])
def get_child_json_from_key(request):
    """
    This is the fixture which is passed in the tests to check for both the subjects i.e math and sports
    Input :
        request <str> - eg. "quizSubject" passed as parameter

    Output:
        response_json["quizSubject"] <list> - Returned from fetching the value of quizSubject or any other parent key
    """
    return response_json[request.param]


@pytest.fixture(params=["sports", "math"])
def get_question_dict_for_all_subjects(request, get_child_json_from_key):
    """
    This fixture is used in tests for the given subjects (sports,math) as parameters
     If this fixture is passed in a test, it will run for all the subjects given in the parameters

     Input :
        request <str> - eg. "sports" and "math" passed as parameter
        get_child_json_from_key<list>- quizSubject list for sports and math.

    Output:f
        <dict> object which is returned from calling the utility function get_child_json_from_key.
     """
    return get_question_dic_for_subject(request.param, get_child_json_from_key)


@pytest.fixture(params=["sports"])
def get_question_dict_for_sports(request, get_child_json_from_key):
    """
    This fixture is used in tests for sports as parameters.
    If this fixture is passed in a test, it will run for only sports

    Input :
        request <str> -  "sports" is passed as parameter
        get_child_json_from_key<list>- quizSubject list for sports.

    Output:
        <dict> object which is returned from calling the utility function get_child_json_from_key for sports.
     """
    return get_question_dic_for_subject(request.param, get_child_json_from_key)


"Used to test the output"
# a = get_question_dic_for_subject("sports",response_json["quizSubject"])
# print(a)
