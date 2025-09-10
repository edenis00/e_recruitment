from django.db import models


class Applicant(models.Model):
    profession = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    lga = models.CharField(max_length=20)
    dob = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    phone_no = models.IntegerField()
    email = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    permanent_address = models.CharField(max_length=20)
    qualification = models.CharField(max_length=20)
    course = models.CharField(max_length=20)
    working_experience = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
