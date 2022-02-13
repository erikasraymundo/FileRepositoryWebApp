from django.urls import path
from . import views

app_name = "file-management"
urlpatterns = [
    path('category=<int:category_id>/', views.index, name='category'),
    path('sort=<int:sort_by>/', views.index, name='sortBy'),
    path('category=<int:category_id>/sort=<int:sort_by>',
         views.index, name='filter'),
    path('category=<int:category_id>/sort=<int:sort_by>/search=<str:query>',
         views.index, name='search'),
    path('', views.index, name='index'),
    path('int<pk>', views.DetailView.as_view(), name='detail'),
    path('upload', views.openUploadView, name='openUploadView'),
    path('saveUpload', views.upload, name='upload')
]
