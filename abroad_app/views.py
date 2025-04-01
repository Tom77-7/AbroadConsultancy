from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages

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