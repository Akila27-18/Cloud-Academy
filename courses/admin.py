from django.contrib import admin
from .models import Course, Lesson, Enrollment, Review, Certificate, Progress

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'course')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'student', 'course', 'issued_at')
    search_fields = ('certificate_id', 'student__username', 'course__title')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'lesson__course')