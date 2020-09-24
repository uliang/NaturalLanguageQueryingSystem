import unittest

from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestQuestionAnsweringView(TestCase) : 
    fixtures = ['salary_data.json']

    # @unittest.skip("")
    @unittest.expectedFailure
    def test_salary_record_does_not_exist(self) : 
        """
        # TODO 
        AI is unable to recongize question because ips22 is outside the usual range and is 
        classifying question as unrecognized. 

        Need more salary like questions with ips outside valid ranges
        """
        response = self.client.get(reverse("question_answering:index"), 
                                   data={"q": "What is the pay range for staff under the ips22 scheme?" })
        self.assertContains(response, "Unable to retrieve salary records.") 

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
        self.assertContains(response, "Sorry, I do not understand this question. Please ask another question.")

    def test_initial_render_does_not_have_nones(self) : 
        response = self.client.get(reverse("question_answering:index"))
        self.assertNotContains(response, "None")
        self.assertNotContains(response, "Sorry, I do not understand this question.")
   
    def test_empty_query_raises_validation_notice(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertNotContains(response, "None")
        self.assertNotContains(response, "Sorry, I do not understand this question.")
        self.assertContains(response, "This field is required")

    def test_error_messages_are_not_duplicated_in_response(self) : 
        response = self.client.get(reverse("question_answering:index"), data={'q': ''})
        self.assertContains(response, "This field is required", count=1)