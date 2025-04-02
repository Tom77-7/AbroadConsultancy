from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
from .models import Course

def register_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')  # Handle Date of Birth
        stream = request.POST.get('stream')  # Handle Stream
        preferred_courses = request.POST.get('preferred_courses')
        preferred_countries = request.POST.get('preferred_countries')
        marks_12th = request.POST.get('marks_12th')

        # Save the student record
        student = Student(
            name=name,
            phone_number=phone_number,
            address=address,
            dob=dob,  # Save DOB
            stream=stream,  # Save Stream
            preferred_courses=preferred_courses,
            preferred_countries=preferred_countries,
            marks_12th=marks_12th
        )
        student.save()

        # Show success message and redirect
        messages.success(request, f"Student registered successfully! Student ID: {student.student_id}")
        return redirect('register_student')

    return render(request, 'student/registration.html')

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        university = request.POST.get('university')
        country = request.POST.get('country')
        stream = request.POST.get('stream')  # Handle stream
        basic_requirements = request.POST.get('basic_requirements')
        minimum_marks = request.POST.get('minimum_marks')
        ielts_score = request.POST.get('ielts_score')

        # Save the course record
        course = Course(
            course_name=course_name,
            university=university,
            country=country,
            stream=stream,  # Save stream
            basic_requirements=basic_requirements,
            minimum_marks=minimum_marks,
            ielts_score=ielts_score
        )
        course.save()

        # Show success message and redirect
        messages.success(request, f"Course '{course_name}' added successfully!")
        return redirect('add_course')

    return render(request, 'course/add_course.html')

def match_courses(request):
    student = None
    eligible_courses = []

    if request.method == 'POST':
        student_id = request.POST.get('student_id')  # Get the Student ID from the form

        try:
            # Fetch the student based on the entered Student ID
            student = Student.objects.get(student_id=student_id)

            # Filter courses based on the student's preferences and eligibility
            eligible_courses = Course.objects.filter(
                country__in=student.preferred_countries.split(', '),
                course_name__in=student.preferred_courses.split(', '),
                stream=student.stream,  # Match stream
                minimum_marks__lte=student.marks_12th,
                ielts_score__lte=6.5  # Assuming a default IELTS score for matching
            )
        except Student.DoesNotExist:
            # If the Student ID is invalid, show an error message
            messages.error(request, "Student ID not found. Please try again.")

    return render(request, 'course/match_courses.html', {
        'student': student,
        'eligible_courses': eligible_courses
    })

def checkout_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('selected_course')  # Get the selected course ID
        try:
            course = Course.objects.get(id=course_id)
            messages.success(request, f"You have successfully checked out the course: {course.course_name}")
            return redirect('match_courses')
        except Course.DoesNotExist:
            messages.error(request, "Invalid course selection. Please try again.")
            return redirect('match_courses')