from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('add-course/', views.add_course, name='add_course'),
    path('match-courses/', views.match_courses, name='match_courses'),
    path('checkout-course/', views.checkout_course, name='checkout_course'),
    path('registered-students/', views.registered_students, name='registered_students'),
    path('courses-list/', views.courses_list, name='courses_list'),
]