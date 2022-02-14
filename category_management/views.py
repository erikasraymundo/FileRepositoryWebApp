from re import template
from django.shortcuts import render
from .models import Category
from django.http import HttpResponse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from category_management.models import Category


def categoryManagement(request):
    categoryNames = Category.objects.all()
    return render(request, 'category-management.html', {
        'categories' : categoryNames,
    })

def SaveACategory(request):
    if(request.POST['CategoryInput'] == ''):
        categoryNames = Category.objects.all()
        return render(request, 'category-management.html', {  'categories' : categoryNames, })
    else:
        categoryNames = Category.objects.all()
        for category in categoryNames:
            if(category.title ==  request.POST['CategoryInput']):
                break
        else:
            category = Category()
            category.title = request.POST['CategoryInput']
            category.save()
    
        categoryNames = Category.objects.all()
        return render(request, 'category-management.html', {  'categories' : categoryNames, })

def printcategories(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 12)

    # lines = ["1", "2", "3"]

    
    lines = []


    categories = Category.objects.all()
    for category in categories:
        lines.append(category.title)

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="users.pdf")