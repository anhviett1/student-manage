from django.db import models

class Score(models.Model):
    
    score = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    subject = models.ForeignKey('app_subject.Subject', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('app_student.Student', on_delete=models.CASCADE, null=True, blank=True)
    
    enrollment = models.ForeignKey('app_enrollment.Enrollment', on_delete=models.CASCADE, null=True, blank=True)
 
    
    def __str__(self):
        return {self.student_id}, {self.class_id}
    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"