from django.shortcuts import render

def view_logs(request):
    return render(request, 'activity_log/logs.html')
