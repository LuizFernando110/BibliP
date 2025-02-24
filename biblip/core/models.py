from django.db import models

from django.db import models
from employee.models import Profile


class Student(models.Model):
    student_name=models.CharField(max_length=244)
    student_registration=models.CharField(max_length=14)


    def __str__(self):
        return self.student_name

class SchoolClass(models.Model):
    school_class_name=models.CharField(max_length=244)
    school_class_teacher=models.ForeignKey(Profile,on_delete=models.CASCADE)
    school_class_students=models.ManyToManyField('Student')

    def __str__(self):
        return self.school_class_name