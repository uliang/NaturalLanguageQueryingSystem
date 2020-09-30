import unittest

from django.test import TestCase, override_settings
from django.urls import reverse

from question_answering.models import Salary
# Create your tests here.


class TestQuestionAnsweringView(TestCase) : 
    fixtures = ['salary_data.json']

    # @unittest.skip("")
    def test_index_page_no_question_received(self) : 
        response = self.client.get(reverse("question_answering:index"), data={"q": '22' })
        # print(response.content)
        self.assertContains(response, "Ensure this value has at least 5 characters (it has 2).") 
        
    # @unittest.skip("")
    def test_index_page_renders_answer_to_payroll_question(self) :
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": "What is the pay range for a ips7 staff?"})
        self.assertContains(response, "$4900 to $6800" )    
        self.assertContains(response, "What is the pay range for a ips7 staff?")                               

    # @unittest.skip("")
    def test_index_page_responds_with_an_ask_again_message_to_an_unrecognized_question(self) :
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": "Where can I find the sports center?"})
        self.assertContains(response, "Unrecognized question")

    # @unittest.skip("")
    def test_initial_render_does_not_have_nones(self) : 
        response = self.client.get(reverse("question_answering:index"))
        self.assertNotContains(response, "None")
        self.assertNotContains(response, 'Unrecognized question')
   
    #@unittest.skip("")
    def test_empty_query_raises_validation_notice(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertNotContains(response, "None")
        self.assertNotContains(response, 'Unrecognized question')
        self.assertContains(response, "This field is required")

    #@unittest.skip("")
    def test_error_messages_are_not_duplicated_in_response(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertContains(response, "This field is required", count=1)

    def test_no_records_found(self):
        Salary.objects.get(pk=18).delete()
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": "What is the pay range for a ips7 staff?"})
        
        self.assertContains(response, "Data not found")

@override_settings(LANG_MODEL='none')
class TestNoModel(TestCase): 
    """
    This test case works only in isolation due to the fact that the language model
    needs to be initialized only once. This means once the model must be loaded 
    once for all requests and thus overriding the LANG_MODEL settings will not work 
    if this test is run with other tests.  
    """
    fixtures = ['salary_data.json']

    def test_that_if_no_lang_model_loaded_message_is_shown(self): 
        response = self.client.get(reverse("question_answering:index"), 
                                data={"q": "What is the pay range for a ips7 staff?"})
    
        self.assertContains(response, "No model loaded")