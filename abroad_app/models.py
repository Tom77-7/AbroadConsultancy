from django.db import models

class Student(models.Model):
    STREAM_CHOICES = [
        ('Science - Biology', 'Science Stream - Biology'),
        ('Science - Computer', 'Science Stream - Computer'),
        ('Commerce', 'Commerce'),
        ('Humanities', 'Humanities'),
    ]

    student_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)  
    address = models.TextField()
    dob = models.DateField()  # Date of Birth field
    stream = models.CharField(max_length=50, choices=STREAM_CHOICES)  # Dropdown for Stream
    preferred_courses = models.TextField()
    preferred_countries = models.TextField()
    marks_12th = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate a unique student ID
            import uuid
            self.student_id = str(uuid.uuid4())[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
class Course(models.Model):
    STREAM_CHOICES = [
        ('Science - Biology', 'Science Stream - Biology'),
        ('Science - Computer', 'Science Stream - Computer'),
        ('Commerce', 'Commerce'),
        ('Humanities', 'Humanities'),
    ]

    course_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    stream = models.CharField(
        max_length=50,
        choices=STREAM_CHOICES,
        null=True,  # Allow NULL for existing rows
        blank=True  # Allow blank values in forms
    )
    basic_requirements = models.TextField()
    minimum_marks = models.FloatField()
    ielts_score = models.FloatField()
    fees = models.IntegerField(default=200000)

    def __str__(self):
        return f"{self.course_name} - {self.university} ({self.country})"
    
    from django.db import models

class Checkout(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student_custom_id = models.CharField(max_length=10, editable=False)  # Renamed field
    total_fees = models.FloatField()
    amount_paid = models.FloatField()
    payment_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically set the student_custom_id from the related student object
        if self.student and not self.student_custom_id:
            self.student_custom_id = self.student.student_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Checkout for {self.student.name} - {self.course.course_name}"