from django.urls import path
from . import views

app_name = "users-management"
urlpatterns = [
    path('', views.index, name='index'),
    path('temporary', views.profileViewOnly, name='temporary-index'),

    path('sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.index, name='filter1'),
    
    path('sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.index, name='filter2'),
    
    path('sort/<int:sort_by>/search=<str:query>',
         views.index, name='search'),
    
    path('archived', views.archivedIndex, name='archived-index'),

    path('archived/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.archivedIndex, name='archived-filter1'),
         
    path('archived/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.archivedIndex, name='archived-filter2'),

    path('print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.printActivePDF, name='printFilter1'),

    path('print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.printActivePDF, name='printFilter2'),

    path('archived/print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.printArchivedPDF, name='printArchivedFilter1'),

    path('archived/print/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.printArchivedPDF, name='printArchivedFilter2'),
]
