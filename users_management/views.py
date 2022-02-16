from tkinter import CENTER
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
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
from django.db.models import Q
import datetime
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from reportlab.lib.units import mm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
import string

# ERIKA 
def index(request,  sort_by=1, query=None, fromDate=None, toDate=None, success=0):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'user-accounts/manage-accounts.html'

    if query == None:
        query = ""

    sort_column = "username"

    if (sort_by == 2):
        sort_column = "first_name"
    elif (sort_by == 3):
        sort_column = "email"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = User.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(created_at__icontains=query),
        created_at__gte=date1,
        created_at__lte=date2,
        deleted_at=None
    ).order_by(sort_column)

    return render(request, template_name,
                  {"users": users,
                  "user" : logged_user, #logged in user
                   "sort_selected": sort_by,
                   "search_value": query,
                   "from_date": fromDate,
                   "to_date": toDate,
                   "success": success})


def archivedIndex(request,  sort_by=1, query=None, fromDate=None, toDate=None, success=0):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'user-accounts/archive-account.html'

    if query == None:
        query = ""

    sort_column = "username"

    if (sort_by == 2):
        sort_column = "first_name"
    elif (sort_by == 3):
        sort_column = "email"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = User.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(
        toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(created_at__icontains=query),
        ~Q(deleted_at=None),
        deleted_at__gte=date1,
        deleted_at__lte=date2,
    ).order_by(sort_column)

    return render(request, template_name,
                  {"users": users,
                  "user" : logged_user, #logged in user
                   "sort_selected": sort_by,
                   "search_value": query,
                   "from_date": fromDate,
                   "to_date": toDate,
                   "success": success})

def printActivePDF(request,  sort_by=1, query=None, fromDate=None, toDate=None):

    if query == None:
        query = ""

    sort_column = "username"

    if (sort_by == 2):
        sort_column = "first_name"
    elif (sort_by == 3):
        sort_column = "email"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = User.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(
        toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(created_at__icontains=query),
        created_at__gte=date1,
        created_at__lte=date2,
        deleted_at=None
    ).order_by(sort_column)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "users_management-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    paragraphStyle = getSampleStyleSheet()

    data = [
        ['Username', 'Name', 'Email', 'Account Created']
    ]

    for user in users:
        list = [Paragraph(f"{user.username}", paragraphStyle['Normal']),
                Paragraph(f"{user.full_name()}", paragraphStyle['Normal']),
                Paragraph(f"{user.email}", paragraphStyle['Normal']),
                Paragraph(f"{user.created_at}",  paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  30 * mm, 40 * mm, 60 * mm, 35 * mm])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (5, 0), colors.HexColor("#8761F4")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ])

    table.setStyle(style)

    rowNumber = len(data)
    for i in range(1, rowNumber):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.HexColor("#DDDDDD")
        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    borderStyle = TableStyle([
        ('BOX', (0, 0), (-1, -1), .5, colors.HexColor("#777777")),
        ('GRID', (0, 1), (-1, -1), .5, colors.HexColor("#777777"))
    ])

    table.setStyle(borderStyle)
    elems = []
    elems.append(table)

    pdf.build(elems)

    response.write(buff.getvalue())
    buff.close()
    return response


def printArchivedPDF(request,  sort_by=1, query=None, fromDate=None, toDate=None):

    if query == None:
        query = ""

    sort_column = "username"

    if (sort_by == 2):
        sort_column = "first_name"
    elif (sort_by == 3):
        sort_column = "email"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = User.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(
        toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(created_at__icontains=query),
        ~Q(deleted_at=None),
        deleted_at__gte=date1,
        deleted_at__lte=date2,
    ).order_by(sort_column)
    
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "archived_users-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    paragraphStyle = getSampleStyleSheet()

    data = [
        ['Username', 'Name', 'Email', 'Account Created']
    ]

    for user in users:
        list = [Paragraph(f"{user.username}", paragraphStyle['Normal']),
                Paragraph(f"{user.full_name()}", paragraphStyle['Normal']),
                Paragraph(f"{user.email}", paragraphStyle['Normal']),
                Paragraph(f"{user.created_at}",  paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  35 * mm, 45 * mm, 60 * mm, 40 * mm])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (5, 0), colors.HexColor("#8761F4")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ])

    table.setStyle(style)

    rowNumber = len(data)
    for i in range(1, rowNumber):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.HexColor("#DDDDDD")
        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    borderStyle = TableStyle([
        ('BOX', (0, 0), (-1, -1), .5, colors.HexColor("#777777")),
        ('GRID', (0, 1), (-1, -1), .5, colors.HexColor("#777777"))
    ])

    table.setStyle(borderStyle)
    elems = []
    elems.append(table)

    pdf.build(elems)

    response.write(buff.getvalue())
    buff.close()
    return response


def profile(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    list = []
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        list.append(user.username)

    forDate =  User.objects.get(pk = request.session.get('user_id'))
    asd = forDate.birthdate
    date = asd.isoformat()

    return render(request, 'profile/profile.html', {
        'user' : logged_user,
        'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
        'bday': date,
    })

def UpdatePassword(request):
    list = []
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        list.append(user.username)
    admin = User.objects.get(pk = request.session.get('user_id'))
    admin.password = request.POST['newPassword']
    admin.updated_at = timezone.now()
    admin.save()
    forDate =  User.objects.get(pk = request.session.get('user_id'))
    asd = forDate.birthdate
    date = asd.isoformat()
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Password has been updated for user with ID: ' + str(request.session.get('user_id'))
    log.save()
    return render(request, 'profile/profile.html', {
       'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
          'bday': date,
    })

def DeleteAccount(request):
    list = []
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        list.append(user.username)
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    #TODO punta ng login, tanggalin session.
    log = Log()
    log.user_id = User.objects.get(pk= request.session.get('user_id'))
    log.description = 'User with ID: ' + request.session.get('user_id') + ' archived his/her account'
    log.save()
    forDate =  User.objects.get(pk = request.session.get('user_id'))
    asd = forDate.birthdate
    date = asd.isoformat()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
          'bday': date,
    })

def UpdateAccountDetails(request):
    list = []
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        list.append(user.username)
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.updated_at = timezone.now()
    admin.username = request.POST['username']
    admin.first_name = request.POST['first_name']
    admin.last_name = request.POST['last_name']
    admin.address = request.POST['address']
    admin.email = request.POST['email']
    admin.birthdate = request.POST['bday']
    admin.gender = request.POST['group']
    admin.save()
    forDate =  User.objects.get(pk =  request.session.get('user_id'))
    asd = forDate.birthdate
    date = asd.isoformat()
    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = 'User with ID: ' + str(request.session.get('user_id'))+ ' updated his/her account'
    log.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
          'bday': date,
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
    generatedPassword = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    list = []
    users = User.objects.all()
    for user in users:
        list.append(user.username)
    return render(request, 'user-accounts/add-account.html', {
        'users' : User.objects.all(),
        'username' : list,
        'password' : generatedPassword,
    })

def AddUserAccount(request):
    user = User()
    user.username = request.POST['username']
    user.password = request.POST['password']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.middle_name = request.POST['middle_name']
    user.address = request.POST['address']
    user.email = request.POST['email']
    user.gender = request.POST['group']
    birthdate = request.POST['birthday']
    user.birthdate = datetime.datetime(int(birthdate[6:10]), int(birthdate[0:2]), int(birthdate[3:5]))
    user.date_joined =  timezone.now()
    user.is_superuser = False
    user.is_staff = False
    user.user_type = 1

    log = Log()
    log.user_id = User.objects.get(pk= request.session.get('user_id'))
    log.description = 'A new account was created by admin with ID: ' + str(request.session.get('user_id'))
    log.save()

    if len(request.FILES) != 0:
        user.image = request.FILES['image']
    user.save()
    return HttpResponseRedirect(reverse('users-management:index'))
    
def EditAccount(request):
    list = []
    users = User.objects.exclude(pk = request.POST['PK'])
    for user in users:
        list.append(user.username)
    user = User.objects.get(pk = request.POST['PK'])
    asd = user.birthdate
    date = asd.isoformat()
    return render(request, 'user-accounts/edit-account.html', {
        'users' : User.objects.filter(pk = request.POST['PK']),
        'bday' : date,
        'invalidUsernames' : list,
    })

def SaveChangesOnEditUserAccount(request):
    user = User.objects.get(pk = request.POST['PK'])
    user.username = request.POST['username']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.middle_name = request.POST['middle_name']
    user.address = request.POST['address']
    user.email = request.POST['email']
    user.gender = request.POST['group']
    user.birthdate = request.POST['bday']
    if len(request.FILES) != 0:
        user.image = request.FILES['image']
    user.save()
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Admin with ID: ' + str(request.session.get('user_id')) + 'edited account details for user with ID: ' + str(request.POST['PK'])
    log.save()
    return HttpResponseRedirect(reverse('users-management:index'))

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
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Admin with ID: ' + str(request.session.get('user_id')) + 'archived user with ID: ' + str(request.POST['ID'])
    log.save()
    return HttpResponseRedirect(reverse('users-management:index'))


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
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    data = [['Event', 'Date/Time', 'Responsible user']]
    
    logs = Log.objects.all()
    for log in logs:
        data.append([log.description, log.created_at, log.user_id])
        
    table = Table(data)

    ts = TableStyle([('GRID',(0,0),(-1,-1),2,colors.black), ('ALIGN',(0,0),(-1,-1),"CENTER")])
    title = "Activity Log"
    systemName = "Soar Academy File Repository System"
    table.setStyle(ts)

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
    log = Log()
    log.user_id = User.objects.get(pk= request.session.get('user_id'))
    log.description = 'Admin with ID: ' + str(request.session.get('user_id')) + 'restored user with ID: ' + str(request.POST['ID'])
    log.save()
    return HttpResponseRedirect(reverse('users-management:archived-index'))


def UploadProfilePicture(request):
    admin = User.objects.get(pk = request.POST['ID'])
    admin.image = request.FILES['image']
    admin.save()

    list = []
    users = User.objects.exclude(pk =  request.session.get('user_id') )
    for user in users:
        list.append(user.username)

    forDate =  User.objects.get(pk =  request.session.get('user_id'))
    asd = forDate.birthdate
    date = asd.isoformat()

    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = 'User with ID: ' + str(request.session.get('user_id')) + ' updated his/her profile picture'
    log.save()

    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
        'bday': date,
    })

#temporary - erika
def profileViewOnly(request):
    return render(request, 'profile/profile.html')