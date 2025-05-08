from django.db import models

class Class(models.Model):
    class_name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
