from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Class
from ..app_semester.models import Semester
from ..app_subject.models import Subject
from ..app_teacher.models import Teacher

User = get_user_model()


class ClassModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.semester = Semester.objects.create(
            semester_id="HK1", name="Học kỳ 1", start_date="2024-01-01", end_date="2024-05-31"
        )
        self.subject = Subject.objects.create(subject_id="SUB001", name="Test Subject", credits=3)
        self.teacher = Teacher.objects.create(
            teacher_id="T001", first_name="Test", last_name="Teacher", email="test@example.com"
        )
        self.class_obj = Class.objects.create(
            class_id="C001",
            name="Test Class",
            semester=self.semester,
            subject=self.subject,
            teacher=self.teacher,
            created_by=self.user,
        )

    def test_class_creation(self):
        self.assertEqual(self.class_obj.class_id, "C001")
        self.assertEqual(self.class_obj.name, "Test Class")
        self.assertEqual(self.class_obj.department, "cntt")
        self.assertTrue(self.class_obj.is_active)

    def test_class_str_representation(self):
        expected_str = f"{self.class_obj.name} ({self.class_obj.class_id})"
        self.assertEqual(str(self.class_obj), expected_str)


class ClassViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

        # Tạo dữ liệu test
        self.semester = Semester.objects.create(semester_id="HK1", name="Học kỳ 1")
        self.subject = Subject.objects.create(subject_id="SUB001", name="Test Subject")
        self.teacher = Teacher.objects.create(
            teacher_id="T001", first_name="Test", last_name="Teacher"
        )
        self.class_obj = Class.objects.create(
            class_id="C001",
            name="Test Class",
            department="cntt",
            semester=self.semester,
            subject=self.subject,
            teacher=self.teacher,
            created_by=self.user,
        )

    def test_class_list_view(self):
        response = self.client.get(reverse("class_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_class/class_list.html")
        self.assertContains(response, "Test Class")

    def test_class_detail_view(self):
        response = self.client.get(reverse("class_detail", args=[self.class_obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_class/class_detail.html")
        self.assertContains(response, "Test Class")

    def test_class_create_view(self):
        response = self.client.post(
            reverse("class_create"),
            {
                "class_id": "C002",
                "name": "New Class",
                "department": "cntt",
                "semester": self.semester.id,
                "subject": self.subject.id,
                "teacher": self.teacher.id,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Class.objects.filter(class_id="C002").exists())

    def test_class_update_view(self):
        response = self.client.post(
            reverse("class_edit", args=[self.class_obj.pk]),
            {
                "class_id": "C001",
                "name": "Updated Class",
                "department": "cntt",
                "semester": self.semester.id,
                "subject": self.subject.id,
                "teacher": self.teacher.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.class_obj.refresh_from_db()
        self.assertEqual(self.class_obj.name, "Updated Class")

    def test_class_delete_view(self):
        response = self.client.post(reverse("class_delete", args=[self.class_obj.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Class.objects.filter(pk=self.class_obj.pk).exists())
