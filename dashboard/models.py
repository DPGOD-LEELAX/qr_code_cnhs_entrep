from django.db import models
from django.urls import reverse

class Student(models.Model):
    # Strand/Track Choices
    STRAND_CHOICES = [
        ('HUMMS', 'HUMMS'),
        ('STEM', 'STEM'),
        ('TVL', 'TVL'),
        ('ABM', 'ABM'),
        ('GAS', 'GAS'),
        ('SAND', 'SAND'),
        ('ICT', 'ICT'),
        ('SPORTS', 'SPORTS'),
    ]

    # Personal Information
    fname = models.CharField(max_length=100, verbose_name="First Name")
    lname = models.CharField(max_length=100, verbose_name="Last Name")
    phone_no = models.CharField(max_length=20, verbose_name="Phone Number")
    
    # Address Information
    full_address = models.TextField(verbose_name="Full Address")
    
    # School Information
    strand = models.CharField(
        max_length=10,
        choices=STRAND_CHOICES,
        verbose_name="Strand/Track"
    )
    section = models.CharField(max_length=50, verbose_name="Section")
    school = models.CharField(max_length=200, verbose_name="School")
    
    # Guardian Information
    guardian_phone = models.CharField(max_length=20, verbose_name="Guardian Phone Number")
    
    # QR Code Information
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fname} {self.lname} - {self.strand}"
    
    def get_absolute_url(self):
        return reverse('dashboard:student_detail', kwargs={'pk': self.pk})
    
    def get_qr_data(self):
        return f"""
        Student Information:
        Name: {self.fname} {self.lname}
        Phone: {self.phone_no}
        Address: {self.full_address}
        Strand: {self.strand}
        Section: {self.section}
        School: {self.school}
        Guardian Phone: {self.guardian_phone}
        """
