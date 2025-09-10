# recruitment/admin.py
from django.contrib import admin
from .models import Applicant


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'surname',
        'email',
        'qualification',
        'course'
    )
    search_fields = (
        'first_name',
        'surname',
        'email',
        'qualification',
        'course',
        'working_experience'
    )
    list_filter = ('qualification', 'course', 'state')
