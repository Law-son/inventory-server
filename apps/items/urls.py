from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('user/', views.get_user_items, name='user_items'),
    path('archives/', views.get_user_archives, name='user_archives'),
    path('create/', views.create_item, name='creat_item'),
    path('update/<int:item_id>/', views.update_item, name='update_item'),
    path('archive/<int:item_id>/', views.archive_item, name='archive_item'),
    path('delete/all/', views.delete_all_archives, name='delete_all_items'),
    path('restore/all/', views.restore_all_items, name='restore_all_items'),
    path('delete/<int:item_id>/', views.delete_archive, name='delete_archive'),
    path('restore/<int:item_id>/', views.restore_archive, name='restore_archive'),
    path('categories/', views.get_categories, name='get_categories'),
    path('units/', views.get_units, name='get_units'),
    path('category/add/', views.add_category, name='add_category'),
    path('unit/add/', views.add_unit, name='add_unit'),
]
