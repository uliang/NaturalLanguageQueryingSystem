import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse

from question_answering.models import Salary

from .stubs import FakeDoc
# Create your tests here.


class TestQuestionAnsweringHappyPath(TestCase):
    fixtures = ['test_salary_data.json']

    def setUp(self): 
        self.test_question = "What is the pay range for a GRADE 1 staff?"
        patcher = patch('question_answering.middleware.nlp',
             return_value=FakeDoc(self.test_question, 'Salary', 'GRADE 1'))
        self.FakeNlp = patcher.start()
        self.addCleanup(patcher.stop)

    def test_index_page_renders_answer_to_payroll_question(self):
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": self.test_question})

        self.FakeNlp.assert_called_with(self.test_question)
        self.assertContains(response, "$10 to $20" )    
        self.assertContains(response, "What is the pay range for a GRADE 1 staff?")                               

class TestQuestionAnsweringSadPath(TestCase) : 
    fixtures = ['test_salary_data.json']

    def setUp(self):
        def side_effect(text): 
            if text ==  "Where can I find the sports center?": 
                return FakeDoc("Where can I find the sports center?", 'Unrecognized', 'GRADE 1')
            elif text is None: 
                return FakeDoc("", "Unrecognized", None)
            elif text == "": 
                return FakeDoc("", "Unrecognized", None)
            elif text == "What is the pay range for a GRADE UNKNOWN staff?": 
                return FakeDoc("What is the pay range for a GRADE UNKNOWN staff?",
                                "Salary", "GRADE UNKNOWN")

        patcher = patch('question_answering.middleware.nlp',
             side_effect=side_effect)
        self.FakeNlp = patcher.start()
        self.addCleanup(patcher.stop)

    def test_index_page_no_question_received(self) : 
        response = self.client.get(reverse("question_answering:index"), data={"q": '42' })
        self.assertContains(response, "Ensure this value has at least 5 characters (it has 2).") 
    
    def test_index_page_responds_with_an_ask_again_message_to_an_unrecognized_question(self):
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": "Where can I find the sports center?"})
        self.assertContains(response, "Unrecognized question")

    def test_initial_render_does_not_have_nones(self) : 
        response = self.client.get(reverse("question_answering:index"))
        self.assertNotContains(response, "None")
        self.assertNotContains(response, 'Unrecognized question')
   
    def test_empty_query_raises_validation_notice(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertNotContains(response, "None")
        self.assertNotContains(response, 'Unrecognized question')
        self.assertContains(response, "This field is required")

    def test_error_messages_are_not_duplicated_in_response(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertContains(response, "This field is required", count=1)

    def test_no_records_found(self):
        response = self.client.get(reverse("question_answering:index"), 
                                data={"q": "What is the pay range for a GRADE UNKNOWN staff?"})
        self.assertContains(response, "Data not found")

class TestQuestionAnsweringNoModel(TestCase): 
    fixtures = ['test_salary_data.json']

    def test_that_if_no_lang_model_loaded_message_is_shown(self): 
        with patch('question_answering.middleware.nlp', 
            side_effect=NotImplementedError("No model loaded")):
            
            response = self.client.get(reverse("question_answering:index"), 
                                    data={"q": "What is the pay range for a GRADE 1 staff?"})
        
            self.assertContains(response, "No model loaded")