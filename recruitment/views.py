from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models import Q
from django.http import HttpResponse
from .models import Applicant
import csv


def home(request):
    return render(request, 'home.html')


def vacancies(request):
    return render(request, 'vacancies.html')


def fetch_nin_data(nin):
    """Mock NIN verification database"""
    mock_nin_database = {
        "12345678901": {
            "first_name": "John",
            "surname": "Doe",
            "middle_name": "James",
            "state": "Lagos",
            "lga": "Ikeja",
            "dob": "1990-01-01",
            "gender": "Male",
            "address": "123 Lagos Street",
            "phone_no": "08012345678",
            "email": "john.doe@example.com"
        },
        "98765432109": {
            "first_name": "Mary",
            "surname": "Smith",
            "middle_name": "Jane",
            "state": "Abuja",
            "lga": "Municipal",
            "dob": "1995-05-15",
            "gender": "Female",
            "address": "456 Abuja Road",
            "phone_no": "08087654321",
            "email": "mary.smith@example.com"
        }
    }

    return mock_nin_database.get(nin, None)


def apply(request):
    context = {}
    if request.method == 'POST' and 'nin' in request.POST:
        nin = request.POST.get('nin')
        nin_data = fetch_nin_data(nin)
        if nin_data:
            context.update(nin_data)
            messages.success(request, 'NIN data loaded successfully!')
        else:
            messages.error(request, 'NIN not found. Please enter your details manually.')
    return render(request, 'apply.html', context)


def submit_application(request):
    if request.method == 'POST':
        try:
            EmailValidator()(request.POST['email'])
            required_fields = ['surname', 'first_name', 'email', 'phone_no']
            if not all(request.POST.get(field) for field in required_fields):
                messages.error(request, 'All required fields must be filled.')
                return render(request, 'apply.html')
            applicant = Applicant(
                nin=request.POST.get('nin', ''),
                profession=request.POST['profession'],
                surname=request.POST['surname'],
                first_name=request.POST['first_name'],
                middle_name=request.POST['middle_name'],
                state=request.POST['state'],
                lga=request.POST['lga'],
                dob=request.POST['dob'],
                gender=request.POST['gender'],
                phone_no=request.POST['phone_no'],
                email=request.POST['email'],
                address=request.POST['address'],
                permanent_address=request.POST['permanent_address'],
                qualification=request.POST['qualification'],
                course=request.POST['course'],
                working_experience=request.POST['working_experience']
            )
            applicant.save()
            send_mail(
                'Application Received',
                'Thank you for applying to MAU. We will review your\
                    application and get back to you.',
                'mau_e_recruitment@gmail.com',   
                [request.POST['email']],
                fail_silently=False,
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('home')
        except ValidationError:
            messages.error(request, 'Invalid email format.')
    return render(request, 'apply.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'password':
            request.session['is_admin_authenticated'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_login.html')


def admin_dashboard(request):
    if not request.session.get('is_admin_authenticated', False):
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('admin_login')
    applicants = Applicant.objects.all()
    if request.method == 'POST':
        query = request.POST.get('search_query', '')
        qualification_filter = request.POST.get('qualification_filter', '')
        state_filter = request.POST.get('state_filter', '')
        nin_filter = request.POST.get('nin_filter', '')
        filters = Q()
        if query:
            filters &= (
                Q(qualification__icontains=query) |
                Q(course__icontains=query) |
                Q(working_experience__icontains=query) |
                Q(first_name__icontains=query) |
                Q(surname__icontains=query) |
                Q(email__icontains=query)
            )
        if qualification_filter:
            filters &= Q(qualification=qualification_filter)
        if state_filter:
            filters &= Q(state=state_filter)
        if nin_filter:
            filters &= Q(nin=nin_filter)
        applicants = Applicant.objects.filter(filters)
    return render(request, 'admin_dashboard.html', {'applicants': applicants})


def export_applicants(request):
    if not request.session.get('is_admin_authenticated', False):
        messages.error(request, 'Please log in to access this feature.')
        return redirect('admin_login')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applicants.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'First Name',
        'Surname',
        'Email',
        'Qualification',
        'Course',
        'Experience',
        'State'
        ])
    applicants = Applicant.objects.all()
    for applicant in applicants:
        writer.writerow([
            applicant.first_name,
            applicant.surname,
            applicant.email,
            applicant.qualification,
            applicant.course,
            applicant.working_experience,
            applicant.state
        ])
    return response


def send_status_update(applicant, status):
    send_mail(
        'Application Status Update',
        f'Hello {applicant.first_name}, your application status is now: {status}',
        'your_email@gmail.com',
        [applicant.email],
        fail_silently=False,
    )
