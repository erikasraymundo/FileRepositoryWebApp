from ctypes import alignment
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
from report_generation.views import PageNumCanvas
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
import datetime
from reportlab.lib.units import inch

from tkinter import CENTER, Image
from tkinter.ttk import Style
from tkinter import CENTER
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from users_management.models import User
from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.platypus import Table
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from .models import User
from django.utils import timezone
from activity_log.models import Log
import PIL.Image
from reportlab.rl_config import defaultPageSize
from django.db.models import Q
from io import BytesIO

from reportlab.lib.units import mm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime

from reportlab.lib.enums import TA_LEFT, TA_CENTER
# ERIKA
def index(request,  sort_by=1, query=None, fromDate=None, toDate=None):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    template_name = 'activity_log/logs.html'

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "user_id__first_name"
    elif (sort_by == 3):
        sort_column = "description"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = Log.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(
        toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    log_list = Log.objects.filter(
        Q(id__icontains=query) |
        Q(description__icontains=query) |
        Q(user_id__first_name__icontains=query) |
        Q(user_id__last_name__icontains=query) |
        Q(created_at__icontains=query),
        created_at__gte=date1,
        created_at__lte=date2
    ).order_by(sort_column)

    return render(request, template_name,
                  {"log_list": log_list,
                  "user" : logged_user,
                   "sort_selected": sort_by,
                   "search_value": query,
                   "from_date": fromDate,
                   "to_date": toDate})


def printPDF(request,  sort_by=1, query=None, fromDate=None, toDate=None):

    if query == None:
        query = ""

    sort_column = "id"

    if (sort_by == 2):
        sort_column = "user_id__first_name"
    elif (sort_by == 3):
        sort_column = "description"
    elif (sort_by == 4):
        sort_column = "-created_at"
    elif (sort_by == 5):
        sort_column = "created_at"

    if fromDate == None:
        FromDate = Log.objects.order_by('id').first().created_at
        fromDate = FromDate.strftime("%Y-%m-%d")

        ToDate = datetime.date.today()
        toDate = ToDate.strftime("%Y-%m-%d")

    date1 = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(
        toDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)

    log_list = Log.objects.filter(
        Q(id__icontains=query) |
        Q(description__icontains=query) |
        Q(user_id__first_name__icontains=query) |
        Q(user_id__last_name__icontains=query) |
        Q(created_at__icontains=query),
        created_at__gte=date1,
        created_at__lte=date2
    ).order_by(sort_column)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "logs-%s.pdf" % str(
        datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name

    buff = BytesIO()
    paragraphStyle = getSampleStyleSheet()

    data = [
        ['Log ID', 'User', 'Description', 'Date Created']
    ]

    for log in log_list:
        created_at = log.created_at.strftime("%m/%d/%Y %I:%M %p")
        list = [Paragraph(f"{log.id}", paragraphStyle['Normal']),
                Paragraph(f"{log.user_id.full_name()}", paragraphStyle['Normal']),
                Paragraph(f"{log.description}", paragraphStyle['Normal']),
                Paragraph(f"{created_at}",  paragraphStyle['Normal'])]
        data.append(list)

    pdf = SimpleDocTemplate(
        buff,
        pagesize=letter,
        rightMargin=70,
        leftMargin=70, topMargin=50, bottomMargin=70
    )

    table = Table(data, colWidths=[
                  15 * mm, 40 * mm, 70 * mm, 40 * mm])

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

    title = "Activity Log"
    description = "The following are the activity logs for Soar Academy's English High School Department common drive."
    styles = getSampleStyleSheet()

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

