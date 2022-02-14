from django.shortcuts import render
from . models import Log

def view_logs(request):
    return render(request, 'activity_log/logs.html')

def index(request,  category_id=0, sort_by=1, query=None, success = 0):
    template_name = 'activity_log/logs.html'

    log_list = Log.objects.all()

    return render(request, template_name, 
    {"log_list": log_list,
     })