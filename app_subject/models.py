from django.db import models

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10, unique=True)
    
    teacher = models.ForeignKey('app_teacher.Teacher', on_delete=models.CASCADE, null=True, blank=True, related_name='taught_subjects')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.subject_name