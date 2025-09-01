from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'strand', 'section', 'school', 'phone_no', 'guardian_phone')
    search_fields = ('fname', 'lname', 'strand', 'section', 'school')
    list_filter = ('strand', 'section', 'school')
    ordering = ('lname', 'fname')
