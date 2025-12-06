from django.contrib import admin
from .models import Course, Lesson, Enrollment

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'order', 'is_preview')
    list_filter = ('course', 'is_preview')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course',)