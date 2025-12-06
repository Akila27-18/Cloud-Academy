from django import forms
from .models import Course, Lesson
from .models import Review

class CourseSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label="Search")
    category = forms.ChoiceField(choices=[('', 'All Categories')] + Course.CATEGORY_CHOICES, required=False)
    min_rating = forms.IntegerField(required=False, min_value=1, max_value=5, label="Min Rating")
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'slug', 'description', 'is_published']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order', 'is_preview']