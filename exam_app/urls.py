from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home), #localhost:8000/wishes/home
    path('logout',views.logout), #localhost:8000/wishes/logout
    path('new', views.new), #localhost:8000/wishes/new
    path('create', views.create), #localhost:8000/wishes/create
    path('edit/<int:wish_id>', views.edit), #localhost:8000/wishes/edit/<int:wish_id>
    path('update/<int:wish_id>', views.update), #localhost:8000/wishes/update/<int:wish_id>
    path('delete/<int:wish_id>', views.delete), #localhost:8000/wishes/delete
    path('stats',views.stats), #localhost:8000/wishes/stats
    path('granted/<int:wish_id>', views.granted), #localhost:8000/wishes/granted/<int:wish_id>
    path('like/<int:wish_id>', views.like), #localhost:8000/wishes/like/<int:wish_id>
]