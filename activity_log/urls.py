from django.urls import path
from . import views

app_name = "activity-log"
urlpatterns = [
    path('', views.index, name='index'),

    path('sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.index, name='filter1'),

    path('sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.index, name='filter2'),

    path('print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.printPDF, name='printFilter1'),

    path('print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.printPDF, name='printFilter2'),
]
