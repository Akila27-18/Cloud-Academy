from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Course, Lesson, Enrollment, Review, Progress, Certificate
from .forms import CourseForm, LessonForm, ReviewForm, CourseSearchForm
import uuid
from django.utils import timezone
from django.db.models import Avg


def homepage(request):
    # Featured = latest published courses
    featured_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:5]

    # Top-rated = courses with highest average rating
    top_courses = Course.objects.filter(is_published=True).annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:5]

    # Categories = distinct categories
    categories = Course.CATEGORY_CHOICES

    return render(request, 'courses/homepage.html', {
        'featured_courses': featured_courses,
        'top_courses': top_courses,
        'categories': categories,
    })
def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related('instructor')
    form = CourseSearchForm(request.GET or None)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')
        min_rating = form.cleaned_data.get('min_rating')

        if keyword:
            courses = courses.filter(title__icontains=keyword)
        if category:
            courses = courses.filter(category=category)
        if min_rating:
            courses = courses.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)

    return render(request, 'courses/course_list.html', {'courses': courses, 'form': form})

@login_required
def add_review(request, slug):
    course = get_object_or_404(Course, slug=slug)
    # Only allow if enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must enroll before reviewing.')
        return redirect('course_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                student=request.user,
                course=course,
                defaults=form.cleaned_data
            )
            messages.success(request, 'Review submitted successfully!')
            return redirect('course_detail', slug=slug)
    else:
        form = ReviewForm()
    return render(request, 'courses/add_review.html', {'form': form, 'course': course})

@login_required
def issue_certificate(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.count()
    completed = Progress.objects.filter(student=request.user, lesson__course=course, completed=True).count()

    if lessons > 0 and lessons == completed:
        cert, created = Certificate.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'certificate_id': str(uuid.uuid4())[:8]}
        )
        return render(request, 'courses/certificate.html', {'certificate': cert})
    else:
        messages.warning(request, 'Complete all lessons to get your certificate.')
        return redirect('course_detail', slug=slug)

@login_required
def mark_completed(request, slug, order):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, course=course, order=order)
    progress, created = Progress.objects.get_or_create(student=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    messages.success(request, f'Lesson "{lesson.title}" marked as completed!')
    return redirect('lesson_detail', slug=slug, order=order)

# Existing views: course_list, course_detail, enroll, lesson_detail

@login_required
def create_course(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'instructor':
        messages.error(request, 'Only instructors can create courses.')
        return redirect('course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def create_lesson(request, slug):
    course = get_object_or_404(Course, slug=slug, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson added successfully!')
            return redirect('course_detail', slug=slug)
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form, 'course': course})

def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related('instructor')
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    is_enrolled = request.user.is_authenticated and Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, 'Enrolled successfully!')
    else:
        messages.info(request, 'You are already enrolled.')
    return redirect('course_detail', slug=slug)

def lesson_detail(request, slug, pk):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    is_enrolled = request.user.is_authenticated and Enrollment.objects.filter(student=request.user, course=course).exists()
    if not (lesson.is_preview or is_enrolled):
        messages.warning(request, 'Please enroll to access this lesson.')
        return redirect('course_detail', slug=slug)
    return render(request, 'courses/lesson_detail.html', {'course': course, 'lesson': lesson, 'is_enrolled': is_enrolled})