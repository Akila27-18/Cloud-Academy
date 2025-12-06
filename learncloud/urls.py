from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Courses app (homepage + all course-related routes)
    path('', include('courses.urls')),
]