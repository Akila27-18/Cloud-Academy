from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg



class Course(models.Model):
    CATEGORY_CHOICES = [
        ('devops', 'DevOps'),
        ('cloud', 'Cloud'),
        ('programming', 'Programming'),
        ('data', 'Data Science'),
        ('design', 'Design'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='programming')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0


    def __str__(self):
        return self.title

class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)  # 1–5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')  # one review per student per course

    def __str__(self):
        return f'{self.student.username} - {self.course.title} ({self.rating}★)'

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'Certificate {self.certificate_id} - {self.student.username} - {self.course.title}'



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    is_preview = models.BooleanField(default=False)  # allow viewing without enrollment

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f'{self.course.title} - {self.title}'

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.username} -> {self.course.title}'
    
class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f'{self.student.username} - {self.lesson.title} ({self.completed})'