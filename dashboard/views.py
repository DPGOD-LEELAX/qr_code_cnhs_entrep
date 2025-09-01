from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
import os
from django.db.models import Count
from django.shortcuts import render
from .models import Student

from django.db.models import Count

def dashboard(request):
    students = Student.objects.all()
    strand_counts = Student.objects.values('strand').annotate(total=Count('strand')).order_by('strand')
    student_count = students.count()
    return render(request, 'dashboard/dashboard.html', {
        'students': students,
        'strand_counts': strand_counts,
        'student_count': student_count
    })

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    return buffer






from django.core.paginator import Paginator
from django.db.models import Q

def student_list(request):
    query = request.GET.get('q', '')
    students_qs = Student.objects.all()

    if query:
        students_qs = students_qs.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(strand__icontains=query) |
            Q(section__icontains=query) |
            Q(school__icontains=query)
        )

    paginator = Paginator(students_qs, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    strand_counts = Student.objects.values('strand').annotate(total=Count('strand')).order_by('strand')

    return render(request, 'dashboard/student_list.html', {
        'students': students,
        'strand_counts': strand_counts,
        'request': request,  # so we can access GET params in template
    })





def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            
            # Generate QR code
            qr_buffer = generate_qr_code(student.get_qr_data())
            
            # Save QR code to model
            filename = f'qr_{student.fname}_{student.lname}.png'
            student.qr_code.save(filename, File(qr_buffer), save=True)
            
            return redirect('dashboard:student_list')

    else:
        form = StudentForm()
    return render(request, 'dashboard/student_form.html', {'form': form})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboard/student_detail.html', {'student': student})

def qr_code_download(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if student.qr_code:
        file_path = os.path.join(settings.MEDIA_ROOT, student.qr_code.name)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response['Content-Disposition'] = f'attachment; filename="{student.qr_code.name}"'
            return response
    return HttpResponse("QR Code not found", status=404)


from django.contrib import messages

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)

            # regenerate QR if you want on edit
            qr_buffer = generate_qr_code(student.get_qr_data())
            filename = f'qr_{student.fname}_{student.lname}.png'
            student.qr_code.save(filename, File(qr_buffer), save=True)

            messages.success(request, "Student updated successfully.")
            return redirect('dashboard:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'dashboard/student_form.html', {'form': form, 'edit_mode': True, 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':  # confirm deletion
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('dashboard:student_list')
    return render(request, 'dashboard/student_confirm_delete.html', {'student': student})



