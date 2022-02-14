from tkinter import CENTER
from tkinter.ttk import Style
from django.shortcuts import render

import csv
from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from category_management.models import Category
from users_management.models import User
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.platypus import Table
from reportlab.lib import colors

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
    filename = "reports/users.pdf"
    pdf = SimpleDocTemplate(
    filename,
    pagesize=letter
)
    data = [
    ['Username', 'Name', 'Email', 'Created At']
]
    
    users = User.objects.all()
    for user in users:
        data.append([user.username, user.first_name+" "+user.last_name, user.email, user.created_at])
        
    table = Table(data)

    ts = TableStyle(
    [
    ('GRID',(0,0),(-1,-1),2,colors.black),
    ('ALIGN',(0,0),(-1,-1),"CENTER")
    ]
)
    title = "List of Users"
    table.setStyle(ts)    
    # elems = []
    # elems.append(title, height)
    # elems.append(table)

    styles = getSampleStyleSheet()
    flowables = [
        Paragraph(title, styles['Title']),
        table,
        Spacer(1 * cm, 1 * cm),
        Paragraph('text after spacer')
    ]


    pdf.build(flowables)