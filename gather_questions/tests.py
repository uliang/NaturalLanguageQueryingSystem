import io 
import json 

from django.test import TestCase
from django.urls import reverse

from .models import Question


# Create your tests here.


class QuestionIndexView(TestCase) : 
    def test_index_view_renders(self) : 
        response = self.client.get(reverse('gather_questions:index'))
        self.assertEqual(response.status_code, 200) 

    def test_number_of_question_info_does_not_render_if_no_questions_collected(self) :
        response = self.client.get(reverse('gather_questions:index'))
        self.assertNotContains(response, "Number of questions")

class QuestionSubmitView(TestCase) :  
    def test_add_question_route(self) : 
        response = self.client.post(reverse('gather_questions:submit'), 
                                    data={"question": "What is this?"}, 
                                    follow=True)
        self.assertRedirects(response, reverse('gather_questions:index'))
        self.assertContains(response, "Number of questions: 1")

    def test_that_empty_string_is_not_saved(self) :
        response = self.client.post(reverse('gather_questions:submit'), 
                                    data={"question": ""}, 
                                    follow=True)
        self.assertRedirects(response, reverse('gather_questions:index'))
        self.assertNotContains(response, "Number of questions: ")

    def test_that_empty_string_does_not_increment_counter(self) :
        Question(question_text="Lunch?").save()
        response = self.client.post(reverse('gather_questions:submit'), 
                                    data={"question": ""}, 
                                    follow=True)
        self.assertContains(response, "Number of questions: 1")

class DownloadJSONLView(TestCase) : 
    def setUp(self):
        q = Question(question_text = "I love ham?")
        q.save() 

    def test_download_button_shows(self) : 
        response = self.client.get(reverse('gather_questions:index'))
        self.assertContains(response, "DOWNLOAD")

    def test_file_downloads(self) : 
        response = self.client.get(reverse('gather_questions:download'))
        content_disposition = response.get('Content-Disposition')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content_disposition, 'attachment; filename="questions.jsonl"')
        self.assertDictEqual(data, {"text": "I love ham?"})
        self.assertTrue(response.content.decode().endswith('\n'))
    
    def test_download_with_offset_properly_offsets_downloads(self) :
        q = Question(question_text="Another question?")
        q.save() 

        response = self.client.get(reverse('gather_questions:download'), data={"offset": "1"})
        data = json.loads(response.content)
        self.assertDictEqual(data, {"text": "Another question?"})