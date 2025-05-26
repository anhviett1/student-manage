from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Semester

User = get_user_model()

class SemesterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.semester = Semester.objects.create(
            semester_id='HK1',
            name='Học kỳ 1',
            start_date='2024-01-01',
            end_date='2024-05-31',
            created_by=self.user
        )

    def test_semester_creation(self):
        self.assertEqual(self.semester.semester_id, 'HK1')
        self.assertEqual(self.semester.name, 'Học kỳ 1')
        self.assertEqual(str(self.semester.start_date), '2024-01-01')
        self.assertEqual(str(self.semester.end_date), '2024-05-31')
        self.assertTrue(self.semester.is_active)

    def test_semester_str_representation(self):
        expected_str = f"{self.semester.name} ({self.semester.semester_id})"
        self.assertEqual(str(self.semester), expected_str)

class SemesterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo dữ liệu test
        self.semester = Semester.objects.create(
            semester_id='HK1',
            name='Học kỳ 1',
            start_date='2024-01-01',
            end_date='2024-05-31',
            created_by=self.user
        )

    def test_semester_list_view(self):
        response = self.client.get(reverse('semester_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_semester/semester_list.html')
        self.assertContains(response, 'Học kỳ 1')

    def test_semester_detail_view(self):
        response = self.client.get(reverse('semester_detail', args=[self.semester.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_semester/semester_detail.html')
        self.assertContains(response, 'Học kỳ 1')

    def test_semester_create_view(self):
        response = self.client.post(reverse('semester_create'), {
            'semester_id': 'HK2',
            'name': 'Học kỳ 2',
            'start_date': '2024-06-01',
            'end_date': '2024-12-31'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Semester.objects.filter(semester_id='HK2').exists())

    def test_semester_update_view(self):
        response = self.client.post(
            reverse('semester_edit', args=[self.semester.pk]),
            {
                'semester_id': 'HK1',
                'name': 'Học kỳ 1 (Cập nhật)',
                'start_date': '2024-01-01',
                'end_date': '2024-05-31'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.semester.refresh_from_db()
        self.assertEqual(self.semester.name, 'Học kỳ 1 (Cập nhật)')

    def test_semester_delete_view(self):
        response = self.client.post(reverse('semester_delete', args=[self.semester.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Semester.objects.filter(pk=self.semester.pk).exists())
