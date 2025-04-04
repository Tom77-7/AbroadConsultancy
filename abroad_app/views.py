from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
from .models import Course
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from .models import Student, Course, Checkout
from django.shortcuts import render, redirect, get_object_or_404


def register_student(request):

    # Clear any existing messages
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        # Handle form submission logic
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')  # Handle Date of Birth
        stream = request.POST.get('stream')  # Handle Stream
        preferred_courses = request.POST.getlist('preferred_courses')  # Get multiple selected courses
        preferred_countries = request.POST.getlist('preferred_countries')  # Get multiple selected countries
        marks_12th = request.POST.get('marks_12th')

        # Convert preferred_courses and preferred_countries to comma-separated strings
        preferred_courses_str = ', '.join(preferred_courses)
        preferred_countries_str = ', '.join(preferred_countries)

        # Save the student record
        try:
            student = Student(
                name=name,
                phone_number=phone_number,
                address=address,
                dob=dob,  # Save DOB
                stream=stream,  # Save Stream
                preferred_courses=preferred_courses_str,
                preferred_countries=preferred_countries_str,
                marks_12th=marks_12th
            )
            student.save()

            # Show success message and redirect
            messages.success(request, f"Student registered successfully! Student ID: {student.student_id}")
            return redirect('register_student')
        except Exception as e:
            # Handle any errors during saving
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register_student')

    # Fetch unique courses with their stream and country
    courses = Course.objects.order_by('course_name').distinct('course_name')
    countries = Course.objects.values_list('country', flat=True).distinct().order_by('country')

    return render(request, 'student/registration.html', {'courses': courses, 'countries': countries})

def add_course(request):

    # Clear any existing messages
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        university = request.POST.get('university')
        country = request.POST.get('country')
        stream = request.POST.get('stream')
        basic_requirements = request.POST.get('basic_requirements')
        minimum_marks = request.POST.get('minimum_marks')
        ielts_score = request.POST.get('ielts_score')
        fees = request.POST.get('fees')  # Get the fees from the form

        try:
            # Save the course to the database
            course = Course(
                course_name=course_name,
                university=university,
                country=country,
                stream=stream,
                basic_requirements=basic_requirements,
                minimum_marks=minimum_marks,
                ielts_score=ielts_score,
                fees=fees  # Save the fees
            )
            course.save()
            messages.success(request, f"Course '{course_name}' added successfully!")
            return redirect('add_course')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_course')

    return render(request, 'course/add_course.html')

def match_courses(request):
    student = None
    eligible_courses = []

    if request.method == 'POST':
        student_id = request.POST.get('student_id')  # Get the Student ID from the form

        if not student_id:
            messages.error(request, "Please enter a valid Student ID.")
            return redirect('match_courses')

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

            # If no eligible courses are found, show an info message
            if not eligible_courses.exists():
                messages.info(request, "No eligible courses found for this student.")

            # Store the correct student_id (from the column) in the session
            request.session['student_id'] = student.student_id

        except Student.DoesNotExist:
            # If the Student ID is invalid, show an error message
            messages.error(request, "Student ID not found. Please try again.")
            return redirect('match_courses')  # Redirect back to the same page

    # Handle GET request for selected course
    if request.method == 'GET' and 'selected_course' in request.GET:
        selected_course_id = request.GET.get('selected_course')
        student_id = request.session.get('student_id')  # Retrieve the correct student_id from the session

        if student_id:
            return redirect('checkout_page', student_id, selected_course_id)
        else:
            messages.error(request, "Student information is missing. Please try again.")
            return redirect('match_courses')

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
        
def registered_students(request):
    # Fetch all registered students
    students = Student.objects.all().order_by('student_id')  # Order by Student ID
    return render(request, 'student/registered_students.html', {'students': students})

def courses_list(request):
    # Fetch all courses
    courses = Course.objects.all().order_by('course_name')  # Order by course name
    return render(request, 'course/courses_list.html', {'courses': courses})

def checkout_page(request, student_id, course_id):
    # Fetch the student using the student_id column
    student = get_object_or_404(Student, student_id=student_id)
    course = get_object_or_404(Course, id=course_id)

    # Fixed charges
    application_charge = 5000
    agency_charge = 10000
    visa_charge = 15000
    processing_fee = 5000

    # Calculate total fees
    total_fees = course.fees + application_charge + agency_charge + visa_charge + processing_fee
    amount_to_pay = total_fees * 0.4  # 40% of the total fees

    if request.method == 'POST':

        if Checkout.objects.filter(student__student_id=student.student_id, course_id=course.id).exists():
            messages.error(request, "Checkout already exists for this student and course.")
            return redirect('match_courses')  # Redirect back to the match_courses page
        
        # Save the checkout record
        checkout = Checkout(
            student=student,
            course=course,
            total_fees=total_fees,
            amount_paid=amount_to_pay,
            payment_verified=True  # Assuming payment is verified for now
        )
        checkout.save()

        messages.success(request, "Payment verified and checkout completed successfully!")
        # Redirect to the match_courses page
        return redirect('match_courses')

    return render(request, 'course/checkout_page.html', {
        'student': student,
        'course': course,
        'application_charge': application_charge,
        'agency_charge': agency_charge,
        'visa_charge': visa_charge,
        'processing_fee': processing_fee,
        'total_fees': total_fees,
        'amount_to_pay': amount_to_pay,
    })

def checkout_details(request):
    # Fetch all checkout records
    checkouts = Checkout.objects.select_related('student', 'course').all().order_by('-created_at')  # Order by most recent

    return render(request, 'course/checkout_details.html', {
        'checkouts': checkouts
    })