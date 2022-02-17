import datetime
# Import mimetypes module
import mimetypes
# import os module
import os
from io import BytesIO

from activity_log.models import Log
from category_management.models import Category
from django.core.exceptions import PermissionDenied
from django.core.files import File as DjangoFile
from django.db.models import Q
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from users_management.models import User

from .models import File


def index(request,  category_id=0, sort_by=4, query=None, fromDate=None, toDate=None, success = 0):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'file_management/index.html'

    if query == None: query = ""
    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = File.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
            fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    if (category_id > 0):
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(
            toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            created_at__gte=date1,
            created_at__lte=date2,
            category_id=category_id, deleted_at=None
        ).order_by(sort_column)

    else:
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            created_at__gte=date1,
            created_at__lte=date2,
            deleted_at=None
        ).order_by(sort_column)

    return render(request, template_name, 
    {"file_list": file_list,
     "category_selected" : category_id,
     "sort_selected": sort_by,
     "search_value": query,
     "from_date": fromDate,
     "to_date": toDate,
     "success": success,
     "user" : logged_user,
     "category_list": Category.objects.filter(isArchived = False)})

def detail(request, file_id):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    template_name = 'file_management/detail.html'
    file = get_object_or_404(File, pk=file_id)
    return render(request, template_name, {"file": file, "user" : logged_user})


def archivedIndex(request,  category_id=0, sort_by=4, query=None, fromDate=None, toDate=None, success=0):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    template_name = 'file_management/archive.html'

    if query == None: query = ""
    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "-deleted_at"
    elif (sort_by == 5):
        sort_column = "deleted_at"

    if fromDate == None:

        try:
            FromDate = File.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
            fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    if (category_id > 0):
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(
            toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            ~Q(deleted_at=None),
            deleted_at__gte=date1,
            deleted_at__lte=date2,
            category_id=category_id
        ).order_by(sort_column)

    else:
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            ~Q(deleted_at=None),
            deleted_at__gte=date1,
            deleted_at__lte=date2
        ).order_by(sort_column)

    return render(request, template_name, 
    {"file_list": file_list,
     "category_selected" : category_id,
     "sort_selected": sort_by,
     "search_value": query,
     "from_date": fromDate,
     "to_date": toDate,
     "success": success,
     "user" : logged_user,
     "category_list": Category.objects.filter(isArchived = False)})


def openUploadView(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'file_management/upload.html', 
    {"category_list": Category.objects.filter(isArchived = False),
    "user" : logged_user,
    "error" : 0})

def upload(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    name = request.POST['name']
    description = request.POST['description']
    category_id = Category.objects.get(pk=request.POST['category_id'])
    user_id = User.objects.get(pk=session_user_id)

    file = File()
    file.name = name
    file.description = description
    file.category_id = category_id
    file.user_id = user_id
    file.url = request.FILES['file']

    try:
        file.save()

        log = Log()
        log.description = f"Uploaded a file ({file.id} - {file.name}) under {file.category_id.title}."
        log.user_id = user_id
        log.save()

        return HttpResponseRedirect(reverse('file-management:success', args={1}))
    except:
        return render(request, 'file_management/upload.html',
            {"category_list": Category.objects.filter(isArchived = False),
            "file" : file,
            "error": 1,
            "user" : logged_user})  # 2 means general error

def openEditView(request, file_id):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    file = get_object_or_404(File, pk=file_id)
    return render(request, 'file_management/edit.html', 
        {"category_list": Category.objects.filter(isArchived = False), 
         "file": file,
         "error": 0,
         "user" : logged_user})

def update(request, file_id):


    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    name = request.POST['name']
    description = request.POST['description']
    category_id = Category.objects.get(pk=request.POST['category_id'])
    user_id = User.objects.get(pk=session_user_id)

    file = File.objects.get(pk=file_id)
    file.name = name
    file.description = description
    file.category_id = category_id
    file.user_id = user_id

    try:
        file.url = request.FILES['file']
    except:
        pass
    try:
        file.save()
        log = Log()
        log.description = f"Updated a file ({file.id} - {file.name}) under {file.category_id.title}."
        log.user_id = user_id
        log.save()
        return HttpResponseRedirect(reverse('file-management:success', args={2}))
    except:
        return render(request, 'file_management/upload.html',
                      {"category_list": Category.objects.filter(isArchived = False),
                       "file": file,
                       "error": 1,
                       "user" : logged_user})  # 2

def archive(request, file_id):
    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    session_user_id = request.session.get('user_id')
    file = get_object_or_404(File, pk=file_id)
    file.deleted_at = timezone.localtime(timezone.now())
    file.save()

    log = Log()
    log.description = f"Archived a file ({file.id} - {file.name})."
    log.user_id = User.objects.get(pk=session_user_id)
    log.save()

    return HttpResponseRedirect(reverse('file-management:success', args={3}))


def restore(request, file_id):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    file = get_object_or_404(File, pk=file_id)
    file.deleted_at = None
    file.save()

    log = Log()
    log.description = f"Restored a file ({file.id} - {file.name})."
    log.user_id = User.objects.get(pk=session_user_id)
    log.save()

    return HttpResponseRedirect(reverse('file-management:archived-success', args={4}))

def checkDuplicateName(request):


    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    file_id = int(request.GET['file_id'])
    duplicated_list = File.objects.filter(name__iexact=request.GET['name']).exclude(id=file_id)

    if file_id != 0:
        duplicated_list = File.objects.filter(~Q(id=file_id), name__iexact=request.GET['name'])
    else:
        duplicated_list = File.objects.filter(name__iexact=request.GET['name'])

    if not duplicated_list:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

# Define function to download pdf file using template


def download(request, file_id):

    
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    file = get_object_or_404(File, pk=file_id)
    filename = file.getFileUrl()

    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % file.getNewFileName()
        # Return the response value

        log = Log()
        log.description = f"Downloaded a file ({file.id} - {file.name})."
        log.user_id = file.user_id
        log.save()

        return response
    else:
        # Load the template
        # return HttpResponse("An error has oc!")
        pass


def pdf_view(request, file_id):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    try:
        file = get_object_or_404(File, pk=file_id)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + file.getFileUrl()

        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        # pass
        # return HttpResponse("error")
        raise Http404()


from report_generation.views import PageNumCanvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Table, TableStyle


def printActivePDF(request,  category_id=0, sort_by=4, query=None, fromDate=None, toDate=None):


    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'file_management/index.html'

    if query == None: query = ""
    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        try:
            FromDate = File.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
            fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    if (category_id > 0):
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(
            toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            created_at__gte=date1,
            created_at__lte=date2,
            category_id=category_id, deleted_at=None
        ).order_by(sort_column)

    else:
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            created_at__gte=date1,
            created_at__lte=date2,
            deleted_at=None
        ).order_by(sort_column)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "file_management-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    paragraphStyle = getSampleStyleSheet()

    data = [
        ['ID', 'Name', 'Category', 'Uploader', 'Date Uploaded']
    ]

    for file in file_list:

        created_at = file.created_at.strftime("%m/%d/%Y %I:%M %p")

        list = [Paragraph(f"{file.id}", paragraphStyle['Normal']),
                Paragraph(f"{file.getNewFileName()}",
                          paragraphStyle['Normal']),
                Paragraph(f"{file.category_id.title}",
                          paragraphStyle['Normal']),
                Paragraph(f"{file.user_id.full_name()}",
                          paragraphStyle['Normal']),
                Paragraph(f"{created_at}", paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  15 * mm, 45 * mm, 25 * mm, 40 * mm, 40 * mm])

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


    title = "File Management - Uploaded Files"
    description = "The following are the upload files in Soar Academy's English High School Department common drive."
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


def printArchivedPDF(request,  category_id=0, sort_by=4, query=None, fromDate=None, toDate=None):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    template_name = 'file_management/archive.html'

    if query == None: query = ""
    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "-deleted_at"
    elif (sort_by == 5):
        sort_column = "deleted_at"

    if fromDate == None:

        try:
            FromDate = File.objects.order_by('id').first().created_at
            fromDate = FromDate.strftime("%Y-%m-%d")
        except:
            FromDate = datetime.date.today()
            fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    if (category_id > 0):
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(
            toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            ~Q(deleted_at=None),
            deleted_at__gte=date1,
            deleted_at__lte=date2,
            category_id=category_id
        ).order_by(sort_column)

    else:
        date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(url__endswith=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query) |
            Q(user_id__last_name__icontains=query) |
            Q(user_id__created_at__icontains=query),
            ~Q(deleted_at=None),
            deleted_at__gte=date1,
            deleted_at__lte=date2
        ).order_by(sort_column)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "archived_files-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    paragraphStyle = getSampleStyleSheet()

    data = [
        ['ID', 'Name', 'Category', 'Uploader', 'Date Uploaded']
    ]

    for file in file_list:

        created_at = file.created_at.strftime("%m/%d/%Y %I:%M %p")

        list = [Paragraph(f"{file.id}", paragraphStyle['Normal']),
                Paragraph(f"{file.getNewFileName()}",
                          paragraphStyle['Normal']),
                Paragraph(f"{file.category_id.title}",
                          paragraphStyle['Normal']),
                Paragraph(f"{file.user_id.full_name()}",
                          paragraphStyle['Normal']),
                Paragraph(f"{created_at}", paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  15 * mm, 45 * mm, 25 * mm, 40 * mm, 40 * mm])

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


    title = "File Management - Archived Files"
    description = "The following are the archived files in Soar Academy's English High School Department common drive."
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

def printIndivualFilePDF(request, file_id):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "file-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    labelStyle = ParagraphStyle(
        name='Bold',
        fontSize=12,
    )
    contentStyle = ParagraphStyle(
        name='Normal',
        fontSize=12,
    )

    file = get_object_or_404(File, pk=file_id)
    uploaded_on = file.created_at.strftime("%m/%d/%Y %I:%M %p")
    updated_at = file.updated_at.strftime("%m/%d/%Y %I:%M %p")

    table1 = [
        [Paragraph('<b>File ID:</b> ', labelStyle), Paragraph(f"{file.id}", contentStyle), 
         Paragraph('<b>Uploaded on:</b> ', labelStyle), Paragraph(f"{uploaded_on}", contentStyle)],
         
        [Paragraph('<b>File Name:</b> ', labelStyle), Paragraph(file.getNewFileName(), contentStyle),
         Paragraph('<b>Updated on:</b> ', labelStyle), Paragraph(f"{updated_at}", contentStyle)],
    ]

    table2 = [
        [Paragraph('<b>File Size:</b> ', labelStyle), Paragraph(''+ file.getSize(), contentStyle),
        Paragraph('<b>Category:</b> ', labelStyle), Paragraph(''+ file.category_id.title, contentStyle)]
    ]

    table3 = [
        [Paragraph('<b>Uploaded by:</b> ', labelStyle),
         Paragraph(file.user_id.full_name(), contentStyle)]
    ]

    table4 = [
        [Paragraph('<b>Details of the file:</b>', labelStyle)]
    ]

    table5 = [
        [Paragraph(file.description, contentStyle)]
    ]

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )


    Table1 = Table(table1, colWidths=[
        35 * mm, 50 * mm, 35 * mm, 45 * mm])
    Table2 = Table(table2, colWidths=[
        35 * mm, 50 * mm, 35 * mm, 45 * mm])
    Table3 = Table(table3, colWidths=[
        35 * mm, 130 * mm])
    Table4 = Table(table4, colWidths=[
        165*mm])
    Table5 = Table(table5, colWidths=[
        165*mm])



    title = "File Management - Individual File Details"
    description = "The following are information of the printed individual file's details from Soar Academy's English High School Department common drive."
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

    elems = []
    elems.append(Image('reports/logo_header.jpg',width = 6.5 * inch, height = 0.885 * inch))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Paragraph(title, styles['DefaultHeading']))
    elems.append(Paragraph(description, styles['Subtitle']))
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Table1)
    elems.append(Table2)
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Table3)
    elems.append(Spacer(.5 * cm, .5 * cm))
    elems.append(Table4)
    elems.append(Spacer(.25 * cm, .25 * cm))
    elems.append(Table5)
    elems.append(Spacer(1 * cm, 1 * cm))

    pdf.build(elems, canvasmaker=PageNumCanvas)

    response.write(buff.getvalue())
    buff.close()
    return response
