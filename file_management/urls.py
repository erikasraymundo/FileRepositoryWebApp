from django.urls import path
from . import views

app_name = "file-management"
urlpatterns = [
    path('category/<int:category_id>/', views.index, name='category'),
    path('sort/<int:sort_by>/', views.index, name='sortBy'),
    path('category/<int:category_id>/sort/<int:sort_by>',
         views.index, name='filter'),
    path('category/<int:category_id>/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.index, name='filter1'),
    path('category/<int:category_id>/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.index, name='filter2'),
    path('category/<int:category_id>/sort/<int:sort_by>/search=<str:query>',
         views.index, name='search'),
    path('success/<int:success>/', views.index, name='success'),
    path('', views.index, name='index'),
    path('<int:isAdded>', views.index, name='index'),

    path('archived', views.archivedIndex, name='archived-index'),
    path('archived/category/<int:category_id>/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>',
         views.archivedIndex, name='archived-filter1'),
    path('archived/category/<int:category_id>/sort/<int:sort_by>/from/<str:fromDate>/to/<str:toDate>/search=<str:query>',
         views.archivedIndex, name='archived-filter2'),


    path('file/<int:file_id>/', views.detail, name='detail'),
    path('upload', views.openUploadView, name='openUploadView'),
    path('edit/<int:file_id>/', views.openEditView, name='openEditView'),
    path('archive/<int:file_id>/', views.archive, name='archive'),
    path('saveUpload', views.upload, name='upload'),
    path('updateFile/<int:file_id>/', views.update, name='update'),

    path('restore/<int:file_id>/', views.restore, name='restore'),
    path('download=<int:file_id>', views.download, name='download'),
    
    path('checkDuplicateName', views.checkDuplicateName, name='check_duplicate_name'),
    path('view/pdf/<int:file_id>/', views.pdf_view, name='pdf_view'),
    path('getpdf', views.getpdf, name='get_pdf')
]
