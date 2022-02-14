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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.platypus import Table
from reportlab.lib import colors
from .models import User
from django.utils import timezone
from activity_log.models import Log

def profile(request):
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, deleted_at__isnull = True),
    })

def UpdatePassword(request):
    admin = User.objects.get(pk = 1)
    admin.password = request.POST['newPassword']
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def DeleteAccount(request):
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def UpdateAccountDetails(request):
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.updated_at = timezone.now()
    admin.username = request.POST['username']
    admin.first_name = request.POST['first_name']
    admin.last_name = request.POST['last_name']
    admin.address = request.POST['address']
    admin.email = request.POST['email']
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def ManageAccounts(request):
    return render(request, 'user-accounts/manage-accounts.html', {
        'users' : User.objects.filter(is_active = 1),
    })

def ArchiveAccounts(request):
    return render(request, 'user-accounts/archive-account.html', {
        'users' : User.objects.filter(is_active = 0),
    })

def AddAccount(request):
    return render(request, 'user-accounts/add-account.html', {
        'users' : User.objects.all(),
    })
    
def EditAccount(request):
    return render(request, 'user-accounts/edit-account.html', {
        'users' : User.objects.filter(pk = request.POST['PK']),
    })

def ViewAccount(request):
    return render(request, 'user-accounts/view-account.html', {
        'users' : User.objects.filter(pk = request.POST['PK']),
    })

def ArchieveUserAccount(request):
    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'user-accounts/archive-account.html', {
        'users' : User.objects.filter(is_active = 0),
    })

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

    ps = ParagraphStyle

    styles = getSampleStyleSheet()
    flowables = [
        Paragraph(title, styles['Title']),
        table,
        Spacer(1 * cm, 1 * cm),
        Paragraph('text after spacer')
    ]


    pdf.build(flowables)

def printactivitylogs(request):
    filename = "reports/Activity Logs.pdf"
    pdf = SimpleDocTemplate(
    filename,
    pagesize=letter
)
    data = [
    ['Event', 'Date/Time', 'Responsible user']
]
    
    logs = Log.objects.all()
    for log in logs:
        data.append([log.description, log.created_at, log.user_id])
        
    table = Table(data)

    ts = TableStyle(
    [
    ('GRID',(0,0),(-1,-1),2,colors.black),
    ('ALIGN',(0,0),(-1,-1),"CENTER")
    ]
)
    title = "Activity Log"
    systemName = "Soar Academy File Repository System"
    table.setStyle(ts)    
    # elems = []
    # elems.append(title, height)
    # elems.append(table)

    styles = getSampleStyleSheet()
    flowables = [
        Paragraph(title, styles['Title']),
        Paragraph(systemName, styles['Heading1']),
        table,
        Spacer(1 * cm, 1 * cm),
        Paragraph('text after spacer')
    ]


    pdf.build(flowables)
    
def RestoreUserAccount(request):
    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = True
    admin.deleted_at = None
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'user-accounts/manage-accounts.html', {
        'users' : User.objects.filter(is_active = 1),
    })
