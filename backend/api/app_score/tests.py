from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Score
from ..app_student.models import Student
from ..app_class.models import Class

User = get_user_model()

class ScoreModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.student = Student.objects.create(
            student_id='S001',
            first_name='Test',
            last_name='Student',
            email='test@example.com'
        )
        self.class_obj = Class.objects.create(
            class_id='C001',
            name='Test Class',
            
            created_by=self.user
        )
        self.score = Score.objects.create(
            student=self.student,
            class_obj=self.class_obj,
            midterm_score=8.5,
            final_score=9.0,
            created_by=self.user
        )

    def test_score_creation(self):
        self.assertEqual(self.score.student, self.student)
        self.assertEqual(self.score.class_obj, self.class_obj)
        self.assertEqual(self.score.midterm_score, 8.5)
        self.assertEqual(self.score.final_score, 9.0)
        self.assertEqual(self.score.total_score, 8.75)  # (8.5 + 9.0) / 2
        self.assertTrue(self.score.is_active)

    def test_score_str_representation(self):
        expected_str = f"{self.student} - {self.class_obj} - {self.score.total_score}"
        self.assertEqual(str(self.score), expected_str)

class ScoreViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo dữ liệu test
        self.student = Student.objects.create(
            student_id='S001',
            first_name='Test',
            last_name='Student'
        )
        self.class_obj = Class.objects.create(
            class_id='C001',
            name='Test Class',
            department='cntt',
            created_by=self.user
        )
        self.score = Score.objects.create(
            student=self.student,
            class_obj=self.class_obj,
            midterm_score=8.5,
            final_score=9.0,
            created_by=self.user
        )

    def test_score_list_view(self):
        response = self.client.get(reverse('score_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_score/score_list.html')
        self.assertContains(response, str(self.student))

    def test_score_detail_view(self):
        response = self.client.get(reverse('score_detail', args=[self.score.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_score/score_detail.html')
        self.assertContains(response, str(self.student))

    def test_score_create_view(self):
        response = self.client.post(reverse('score_create'), {
            'student': self.student.id,
            'class_obj': self.class_obj.id,
            'midterm_score': 7.5,
            'final_score': 8.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Score.objects.filter(
            student=self.student,
            class_obj=self.class_obj
        ).exists())

    def test_score_update_view(self):
        response = self.client.post(
            reverse('score_edit', args=[self.score.pk]),
            {
                'student': self.student.id,
                'class_obj': self.class_obj.id,
                'midterm_score': 9.0,
                'final_score': 9.5
            }
        )
        self.assertEqual(response.status_code, 302)
        self.score.refresh_from_db()
        self.assertEqual(self.score.midterm_score, 9.0)
        self.assertEqual(self.score.final_score, 9.5)
        self.assertEqual(self.score.total_score, 9.25)

    def test_score_delete_view(self):
        response = self.client.post(reverse('score_delete', args=[self.score.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Score.objects.filter(pk=self.score.pk).exists())
