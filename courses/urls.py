from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    homepage,
    course_list,
    course_detail,
    enroll,
    lesson_detail,
    create_course,
    create_lesson,
    mark_completed,
    issue_certificate,
    add_review,
)

app_name = "courses"


urlpatterns = [
    # Homepage
    path("", homepage, name="homepage"),

    # Course routes
    path("courses/", course_list, name="course_list"),
    path("courses/create/", create_course, name="create_course"),
    path("courses/<slug:slug>/", course_detail, name="course_detail"),
    path("courses/<slug:slug>/enroll/", enroll, name="enroll"),

    # Lesson routes
    path("courses/<slug:slug>/lesson/create/", create_lesson, name="create_lesson"),
    path('<slug:slug>/lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
    path("courses/<slug:slug>/lesson/<int:order>/complete/", mark_completed, name="mark_completed"),

    # Certificate + Reviews
    path("courses/<slug:slug>/certificate/", issue_certificate, name="issue_certificate"),
    path("courses/<slug:slug>/review/", add_review, name="add_review"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

