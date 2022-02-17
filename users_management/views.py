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

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Image
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from report_generation.views import PageNumCanvas


# ERIKA 
def index(request,  sort_by=5, query=None, fromDate=None, toDate=None, success=0):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    template_name = 'user-accounts/manage-accounts.html'

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "username"
    elif (sort_by == 3):
        sort_column = "first_name"
    elif (sort_by == 4):
        sort_column = "email"
    elif (sort_by == 5):
        sort_column = "-created_at"
    elif (sort_by == 6):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = User.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
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
        ~Q(pk = session_user_id),
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


def archivedIndex(request,  sort_by=5, query=None, fromDate=None, toDate=None, success=0):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'user-accounts/archive-account.html'

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "username"
    elif (sort_by == 3):
        sort_column = "first_name"
    elif (sort_by == 4):
        sort_column = "email"
    elif (sort_by == 5):
        sort_column = "-created_at"
    elif (sort_by == 6):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = User.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
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

def printActivePDF(request,  sort_by=5, query=None, fromDate=None, toDate=None):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "username"
    elif (sort_by == 3):
        sort_column = "first_name"
    elif (sort_by == 4):
        sort_column = "email"
    elif (sort_by == 5):
        sort_column = "-created_at"
    elif (sort_by == 6):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = User.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
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
        ['ID', 'Username', 'Name', 'Email', 'Account Created']
    ]

    for user in users:
        created_at = user.created_at.strftime("%m/%d/%Y %I:%M %p")

        list = [Paragraph(f"{user.id}", paragraphStyle['Normal']),
                Paragraph(f"{user.username}", paragraphStyle['Normal']),
                Paragraph(f"{user.full_name()}", paragraphStyle['Normal']),
                Paragraph(f"{user.email}", paragraphStyle['Normal']),
                Paragraph(f"{created_at}",  paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  15 * mm, 30 * mm, 40 * mm, 42 * mm, 38 * mm])

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

    title = "Users Management - Active Accounts"
    description = "The following are the active user accounts of Soar Academy's English High School Department common drive."
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Subtitle',
                                  fontSize=12,
                                  leading=14,
                                  spaceAfter=6),
                   alias='subtitle')
    styles.add(ParagraphStyle(name='DefaultHeading',
                                  fontSize=18,
                                  leading=22,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='dh')    

    table.setStyle(borderStyle)

    elems = []
    elems.append(Image('reports/logo_header.jpg',width = 6.5 * inch, height = 0.885 * inch))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Paragraph(title, styles['DefaultHeading']))
    elems.append(Paragraph(description, styles['Subtitle']))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(table)
    elems.append(Spacer(1 * cm, 1 * cm))

    pdf.build(elems, canvasmaker=PageNumCanvas)

    response.write(buff.getvalue())
    buff.close()
    return response


def printArchivedPDF(request,  sort_by=5, query=None, fromDate=None, toDate=None):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "username"
    elif (sort_by == 3):
        sort_column = "first_name"
    elif (sort_by == 4):
        sort_column = "email"
    elif (sort_by == 5):
        sort_column = "-created_at"
    elif (sort_by == 6):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = User.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
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
        ['ID', 'Username', 'Name', 'Email', 'Account Archived']
    ]

    for user in users:
        deleted_at = user.deleted_at.strftime("%m/%d/%Y %I:%M %p")

        list = [Paragraph(f"{user.id}", paragraphStyle['Normal']),
                Paragraph(f"{user.username}", paragraphStyle['Normal']),
                Paragraph(f"{user.full_name()}", paragraphStyle['Normal']),
                Paragraph(f"{user.email}", paragraphStyle['Normal']),
                Paragraph(f"{deleted_at}",  paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  15 * mm, 30 * mm, 40 * mm, 42 * mm, 38 * mm])

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

    title = "Users Management - Archived Accounts"
    description = "The following are the archived user accounts of Soar Academy's English High School Department common drive."
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Subtitle',
                                  fontSize=12,
                                  leading=14,
                                  spaceAfter=6),
                   alias='subtitle')
    styles.add(ParagraphStyle(name='DefaultHeading',
                                  fontSize=18,
                                  leading=22,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='dh')    

    table.setStyle(borderStyle)

    elems = []
    elems.append(Image('reports/logo_header.jpg',width = 6.5 * inch, height = 0.885 * inch))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Paragraph(title, styles['DefaultHeading']))
    elems.append(Paragraph(description, styles['Subtitle']))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(table)
    elems.append(Spacer(1 * cm, 1 * cm))

    pdf.build(elems, canvasmaker=PageNumCanvas)

    response.write(buff.getvalue())
    buff.close()
    return response


def profile(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

   #For Username Cheching
    list = []
    listEmails = []
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        list.append(user.username)
    #for email checking
    users = User.objects.exclude(pk = request.session.get('user_id') )
    for user in users:
        listEmails.append(user.email)

    forDate = logged_user
    asd = forDate.birthdate
    date = asd.isoformat()

    return render(request, 'profile/profile.html', {
        'user' : logged_user,
        'details' : User.objects.filter(pk = request.session.get('user_id'), is_active = 1 , ),
        'username': list,
        'emails': listEmails,
        'bday': date,
    })

def UpdatePassword(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    admin = User.objects.get(pk = request.session.get('user_id'))
    admin.password = request.POST['newPassword']
    admin.updated_at = timezone.now()
    admin.save()
    log = Log()
    log.user_id = User.objects.get(pk= session_user_id)
    log.description = 'User with ID: #' + str(request.session.get('user_id'))+ ' ( username - ' +  log.user_id.username+ ' ) ' + 'updated his/her password'
    log.save()

    return HttpResponseRedirect(reverse('profile'))

def DeleteAccount(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    #TODO punta ng login, tanggalin session.
    log = Log()
    log.user_id = User.objects.get(pk= request.session.get('user_id'))
    log.description = 'User with ID: #' + str(request.session.get('user_id'))+ ' ( username - ' +  log.user_id.username+ ' ) ' + 'archived his/her account.'
    log.save()
    del request.session['user_id']
    del request.session['is_superuser']
    return HttpResponseRedirect(reverse('loginView'))

def UpdateAccountDetails(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.updated_at = timezone.now()
    admin.username = request.POST['username']
    admin.first_name = request.POST['first_name']
    admin.middle_name = request.POST['middle_name']
    admin.last_name = request.POST['last_name']
    admin.address = request.POST['address']
    admin.email = request.POST['email']
    admin.birthdate = request.POST['bday']
    admin.gender = request.POST['group']
    admin.save()
    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = 'User with ID: #' + str(request.session.get('user_id'))+ ' ( username - ' +  log.user_id.username+ ' ) ' + 'updated his/her account.'
    log.save()

    return HttpResponseRedirect(reverse('profile'))

def ManageAccounts(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'user-accounts/manage-accounts.html', {
        'user' : logged_user,
        'user' : User.objects.filter(is_active =  1),
        'admin' : session_user_id,
    })

def ArchiveAccounts(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    pk2 =  request.session.get('user_id')
    return render(request, 'user-accounts/archive-account.html', {
        'user' : logged_user,
        'users' : User.objects.filter(~Q(pk =  request.session.get('user_id'), is_active =  0)),
    })

def AddAccount(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    generatedPassword = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
   #For Usernameand email Checking
    list = []
    listEmails = []
    users = User.objects.all()
    for user in users:
        list.append(user.username)
        listEmails.append(user.email)

    return render(request, 'user-accounts/add-account.html', {
        'user' : logged_user,
        'users' : User.objects.all(),
        'username' : list,
        'emails' : listEmails,
        'password' : generatedPassword,
    })

def AddUserAccount(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

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
    log.description = 'A new account was created by the administrator.'
    log.save()

    if len(request.FILES) != 0:
        user.image = request.FILES['image']
    user.save()
    return HttpResponseRedirect(reverse('users-management:index'))
    
def EditAccount(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    #For Usernameand email Checking
    list = []
    listEmails = []
    users = User.objects.exclude(pk = request.POST['PK'])
    for user in users:
        list.append(user.username)
        listEmails.append(user.email)
    
    user2 = User.objects.get(pk = request.POST['PK'])
    asd = user2.birthdate
    date = asd.isoformat()
    return render(request, 'user-accounts/edit-account.html', {
        'user' : logged_user,
        'users' : User.objects.filter(pk = request.POST['PK']),
        'bday' : date,
        'invalidUsernames' : list,
        'emails' : listEmails,
    })

def SaveChangesOnEditUserAccount(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

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
    log.description = 'Administrator with ID: #' + str(request.session.get('user_id'))+ ' ( username - ' +  log.user_id.username+ ' ) ' + 'edited account details for user with ID: #' + str(request.POST['PK']) + ' ( username: ' +  user.username + ' ) '
    log.save()
    return HttpResponseRedirect(reverse('users-management:index'))

def ViewAccount(request):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'user-accounts/view-account.html', {
        'user' : logged_user,
        'users' : User.objects.filter(pk = request.POST['PK']),
    })

def ArchieveUserAccount(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save() 
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Administrator has archived the user with ID: #' + str(request.POST['ID']) + ' ( username - ' + admin.username + ' ).'
    log.save()
    return HttpResponseRedirect(reverse('users-management:index'))

def RestoreUserAccount(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = True
    admin.deleted_at = None
    admin.updated_at = timezone.now()
    admin.save()
    log = Log()
    log.user_id = User.objects.get(pk= request.session.get('user_id'))
    log.description = 'Administrator has restored the user with ID: #' + str(request.POST['ID']) + ' ( username - ' + admin.username + ' ).'
    log.save()
    return HttpResponseRedirect(reverse('users-management:archived-index'))

def UploadProfilePicture(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

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
    log.description = 'User with ID: #' + str(request.session.get('user_id'))+ ' ( username - ' +  log.user_id.username+ ' ) ' + 'updated his/her profile picture.'
    log.save()


    return HttpResponseRedirect(reverse('profile'))
