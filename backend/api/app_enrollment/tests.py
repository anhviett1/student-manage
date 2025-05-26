from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Enrollment
from app_student.models import Student
from app_class.models import Class

User = get_user_model()

class EnrollmentModelTest(TestCase):
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
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            class_obj=self.class_obj,
            status='active',
            created_by=self.user
        )

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.class_obj, self.class_obj)
        self.assertEqual(self.enrollment.status, 'active')
        self.assertTrue(self.enrollment.is_active)

    def test_enrollment_str_representation(self):
        expected_str = f"{self.student} - {self.class_obj}"
        self.assertEqual(str(self.enrollment), expected_str)

class EnrollmentViewTest(TestCase):
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
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            class_obj=self.class_obj,
            status='active',
            created_by=self.user
        )

    def test_enrollment_list_view(self):
        response = self.client.get(reverse('enrollment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_enrollment/enrollment_list.html')
        self.assertContains(response, str(self.student))

    def test_enrollment_detail_view(self):
        response = self.client.get(reverse('enrollment_detail', args=[self.enrollment.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_enrollment/enrollment_detail.html')
        self.assertContains(response, str(self.student))

    def test_enrollment_create_view(self):
        response = self.client.post(reverse('enrollment_create'), {
            'student': self.student.id,
            'class_obj': self.class_obj.id,
            'status': 'active'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(
            student=self.student,
            class_obj=self.class_obj
        ).exists())

    def test_enrollment_update_view(self):
        response = self.client.post(
            reverse('enrollment_edit', args=[self.enrollment.pk]),
            {
                'student': self.student.id,
                'class_obj': self.class_obj.id,
                'status': 'completed'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'completed')

    def test_enrollment_delete_view(self):
        response = self.client.post(reverse('enrollment_delete', args=[self.enrollment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(pk=self.enrollment.pk).exists())
