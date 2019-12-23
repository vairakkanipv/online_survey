from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Question, Options
from django.conf import settings


class QuestionListViewTest(TestCase):

    def setUp(self):
        self.user = User(username='tester')
        self.user.set_password('1234')
        self.user.save()
        self.client.login(username='tester',password='1234')
        question_text_list = ['this issecond  question', 'this is test question']
        for question_text in question_text_list:
            question = Question(text=question_text, datetime=timezone.now(), author_id=self.user.id)
            question.save()

    def test_question_list(self):

        response = self.client.get(reverse('myapp:question_list'))
        question_list = Question.objects.all()
        for question in question_list:
            self.assertContains(response, question.text)


class QuestionDetailTest(TestCase):
    '''
    create a class questiondetail test
    create questions and options and save
    test figure out how to test it
    '''

    def setUp(self):
        self.user = User(username='tester')
        self.user.set_password('1234')
        self.user.save()
        self.question = Question(text='this is questiondetail test question',
                                 datetime=timezone.now(),
                                 author_id=self.user.id)
        self.question.save()
        option_text_list = ['sample1', 'sample2', 'sample3']
        for option_text in option_text_list:
            option = Options(text=option_text, question_id=self.question.id)
            option.save()

    def test_login_redirect(self):
        response = self.client.get(reverse('myapp:question_details', args=(self.question.id,)))
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))

    def test_question_detail(self):
        self.client.login(username='tester', password='1234')
        response = self.client.get(reverse('myapp:question_details', args=(self.question.id, )))
        self.assertContains(response, self.question.text)

        option_list = self.question.options_set.all()
        for option in option_list:
            self.assertContains(response, option.text)


class VotingTest(TestCase):

    def setUp(self):
        self.user = User(username='tester')
        self.user.set_password('1234')
        self.user.save()
        self.question = Question(text='this is test of vote answer test question', datetime=timezone.now(),author_id=self.user.id)
        self.question.save()
        option_text_list = ['answer1', 'answer2', 'answer3']
        for option_text in option_text_list:
            option = Options(text=option_text, question_id=self.question.id)
            option.save()
            self.answer = option.id

    def test_result(self):
        response = self.client.get(reverse('myapp:results', args=(self.question.id, )))
        option_list = self.question.options_set.all()
        for option in option_list:
            search_word = f"{option.text} - {option.votes}"
            self.assertContains(response, search_word)

    def test_vote(self):
        response = self.client.get(reverse('myapp:vote', args=(self.question.id,)), {'answer': self.answer})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('myapp:results', args=(self.question.id, )))


class AddQuestionTest(TestCase):

    def setUp(self):
        self.user = User(username='tester')
        self.user.set_password('1234')
        self.user.save()
        self.client.login(username='tester', password='1234')

    def test_get(self):
        response = self.client.get(reverse('myapp:add_question'))
        self.assertContains(response, 'New Question')
        self.assertContains(response, 'Enter option2 here')
        self.assertContains(response, 'Enter option1 here')

    def test_post_invalid_question(self):
        response = self.client.post(reverse('myapp:add_question'), {
            'question_text': 'this is a question',
            'option1': 'option1',
            'option2': 'option2',
            'option3': ''})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('myapp:question_list'))
        question = Question.objects.filter(text='this is a question').first()
        self.assertIsNone(question)

    def test_post_valid_question(self):
        response = self.client.post(reverse('myapp:add_question'), {
            'question_text': 'this is a question',
            'option1': 'option1',
            'option2': 'option2',
            'option3': 'option3'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('myapp:question_list'))
        question = Question.objects.filter(text='this is a question').first()
        self.assertIsNotNone(question)
        options = question.options_set.all()
        self.assertEquals(len(options), 3)