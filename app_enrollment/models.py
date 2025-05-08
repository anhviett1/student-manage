from django.db import models

class Enrollment(models.Model):
    student = models.ForeignKey('app_student.Student', on_delete=models.CASCADE, null=True, blank=True)
    class_id = models.ForeignKey('app_class.Class', on_delete=models.CASCADE, null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    ])
