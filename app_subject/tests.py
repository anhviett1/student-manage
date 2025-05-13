from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Subject

User = get_user_model()

class SubjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.subject = Subject.objects.create(
            subject_id='SUB001',
            name='Test Subject',
            description='Test Description',
            credits=3,
            faculty='cntt',
            created_by=self.user
        )

    def test_subject_creation(self):
        self.assertEqual(self.subject.subject_id, 'SUB001')
        self.assertEqual(self.subject.name, 'Test Subject')
        self.assertEqual(self.subject.description, 'Test Description')
        self.assertEqual(self.subject.credits, 3)
        self.assertEqual(self.subject.faculty, 'cntt')
        self.assertTrue(self.subject.is_active)

    def test_subject_str_representation(self):
        expected_str = f"{self.subject.name} ({self.subject.subject_id})"
        self.assertEqual(str(self.subject), expected_str)

class SubjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo dữ liệu test
        self.subject = Subject.objects.create(
            subject_id='SUB001',
            name='Test Subject',
            description='Test Description',
            credits=3,
            faculty='cntt',
            created_by=self.user
        )

    def test_subject_list_view(self):
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_subject/subject_list.html')
        self.assertContains(response, 'Test Subject')

    def test_subject_detail_view(self):
        response = self.client.get(reverse('subject_detail', args=[self.subject.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_subject/subject_detail.html')
        self.assertContains(response, 'Test Subject')

    def test_subject_create_view(self):
        response = self.client.post(reverse('subject_create'), {
            'subject_id': 'SUB002',
            'name': 'New Subject',
            'description': 'New Description',
            'credits': 4,
            'faculty': 'cntt'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subject.objects.filter(subject_id='SUB002').exists())

    def test_subject_update_view(self):
        response = self.client.post(
            reverse('subject_edit', args=[self.subject.pk]),
            {
                'subject_id': 'SUB001',
                'name': 'Updated Subject',
                'description': 'Updated Description',
                'credits': 3,
                'faculty': 'cntt'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, 'Updated Subject')
        self.assertEqual(self.subject.description, 'Updated Description')

    def test_subject_delete_view(self):
        response = self.client.post(reverse('subject_delete', args=[self.subject.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subject.objects.filter(pk=self.subject.pk).exists())
