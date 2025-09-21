from django.shortcuts import render, redirect, get_object_or_404
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


def apply(request):
    context = {}
    if request.method == 'POST' and 'nin' in request.POST:
        nin = request.POST.get('nin')
        # Accept only if NIN is 11 digits and numeric (no characters)
        if not nin or len(nin) != 11 or not nin.isdigit():
            messages.error(request, 'Invalid NIN format. NIN must be exactly 11 digits and contain only numbers.')
        else:
            messages.success(request, 'NIN verified successfully!')
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
                profession=request.POST.get('profession', ''),
                surname=request.POST.get('surname', ''),
                first_name=request.POST.get('first_name', ''),
                middle_name=request.POST.get('middle_name', ''),
                state=request.POST.get('state', ''),
                lga=request.POST.get('lga', ''),
                dob=request.POST.get('dob', ''),
                gender=request.POST.get('gender', ''),
                phone_no=request.POST.get('phone_no', ''),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', ''),
                permanent_address=request.POST.get('permanent_address', ''),
                qualification=request.POST.get('qualification', ''),
                course=request.POST.get('course', ''),
                working_experience=request.POST.get('working_experience', '')
            )
            applicant.save()
            messages.success(request, 'Application submitted successfully! Email sent successfully.')
            request.session['new_applicant_notification'] = True
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
    notification = request.session.pop('new_applicant_notification', False)
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
    return render(request, 'admin_dashboard.html', {'applicants': applicants, 'notification': notification})


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


def edit_applicant(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        # Update fields from POST data
        for field in ['profession', 'surname', 'first_name', 'middle_name', 'state', 'lga', 'dob', 'gender', 'phone_no', 'email', 'address', 'permanent_address', 'qualification', 'course', 'working_experience', 'nin']:
            setattr(applicant, field, request.POST.get(field, getattr(applicant, field)))
        applicant.save()
        messages.success(request, 'Applicant updated successfully!')
        return redirect('admin_dashboard')
    return render(request, 'edit_applicant.html', {'applicant': applicant})


def delete_applicant(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        applicant.delete()
        messages.success(request, 'Applicant deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'delete_applicant.html', {'applicant': applicant})
