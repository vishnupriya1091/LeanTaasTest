# LeanTaasTest
Lean Taas Assignment with test cases implemented in pytest for given questions

Procedure followed to write the tests:
1. To simulate the request, mock api request was created with a response of 200 and expected JSON as output. 
Please refer to input_response.txt and mock_leantaas_request.py.

2. To validate the given questions,following tests were written:
        1) Validate all questions have four non null options.
        Solution:test_check_quiz_subject_has_non_null_options

        2) Validate ["New York Bulls", "Los Angeles Kings", "Golden State Warriors", "Houston Rocket"] 
        are the options for sports q1.
        Solution:test_check_sports_has_given_options
        
3.Code flow:
  Created a utility function get_question_dic_for_subject which returns a dictionary for the given subjects as input. 
  The utility function is used in fixture :
        1) get_question_dict_for_all_subjects - This is used in most of the tests as it passes both given parameters
          as input. This is used to test the conditions for both the subjects.
        2) get_question_dict_for_sports - This is used where only sports is being passed as a parameter for question 2.
        3) get_child_json_from_key - This fixture is being used to fetch JSON object of quizSubject
