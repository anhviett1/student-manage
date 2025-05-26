from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()

class TeacherModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.teacher = Teacher.objects.create(
            teacher_id='T001',
            first_name='Test',
            last_name='Teacher',
            email='test@example.com',
            phone='0123456789',
           
            degree='thac_si',
            created_by=self.user
        )

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.teacher_id, 'T001')
        self.assertEqual(self.teacher.first_name, 'Test')
        self.assertEqual(self.teacher.last_name, 'Teacher')
        self.assertEqual(self.teacher.email, 'test@example.com')
        self.assertEqual(self.teacher.phone, '0123456789')
        self.assertEqual(self.teacher.department, 'cntt')
        self.assertEqual(self.teacher.degree, 'thac_si')
        self.assertTrue(self.teacher.is_active)

    def test_teacher_str_representation(self):
        expected_str = f"{self.teacher.first_name} {self.teacher.last_name} ({self.teacher.teacher_id})"
        self.assertEqual(str(self.teacher), expected_str)

class TeacherViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo dữ liệu test
        self.teacher = Teacher.objects.create(
            teacher_id='T001',
            first_name='Test',
            last_name='Teacher',
            email='test@example.com',
            phone='0123456789',
          
            degree='thac_si',
            created_by=self.user
        )

    def test_teacher_list_view(self):
        response = self.client.get(reverse('teacher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_teacher/teacher_list.html')
        self.assertContains(response, 'Test Teacher')

    def test_teacher_detail_view(self):
        response = self.client.get(reverse('teacher_detail', args=[self.teacher.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_teacher/teacher_detail.html')
        self.assertContains(response, 'Test Teacher')

    def test_teacher_create_view(self):
        response = self.client.post(reverse('teacher_create'), {
            'teacher_id': 'T002',
            'first_name': 'New',
            'last_name': 'Teacher',
            'email': 'new@example.com',
            'phone': '0987654321',
            
            'degree': 'tien_si'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Teacher.objects.filter(teacher_id='T002').exists())

    def test_teacher_update_view(self):
        response = self.client.post(
            reverse('teacher_edit', args=[self.teacher.pk]),
            {
                'teacher_id': 'T001',
                'first_name': 'Updated',
                'last_name': 'Teacher',
                'email': 'updated@example.com',
                'phone': '0123456789',
               
                'degree': 'thac_si'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.first_name, 'Updated')
        self.assertEqual(self.teacher.email, 'updated@example.com')

    def test_teacher_delete_view(self):
        response = self.client.post(reverse('teacher_delete', args=[self.teacher.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Teacher.objects.filter(pk=self.teacher.pk).exists())
