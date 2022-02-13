from django.shortcuts import render

import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from users_management.models import User

def profile(request):
    return render(request, 'profile/profile.html')

def manage_accounts(request):
    return render(request, 'user-accounts/manage-accounts.html')

def add_accounts(request):
    return render(request, 'user-accounts/add-account.html')

def edit_accounts(request):
    return render(request, 'user-accounts/edit-account.html')

def archive_accounts(request):
    return render(request, 'user-accounts/archive-account.html')

def view_accounts(request):
    return render(request, 'user-accounts/view-account.html')

def printpdf(request):
    return render(request, 'profile/print.html')

def printusers(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 12)

    # lines = ["1", "2", "3"]

    
    lines = []


    users = User.objects.all()
    for user in users:
        lines.append(user.user_type)
        lines.append(user.full_name())
        lines.append(user.gender)

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="users.pdf")