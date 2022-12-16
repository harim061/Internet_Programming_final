from django.urls import path
from . import views

urlpatterns = [

    path('',views.ShoppingItemList.as_view()),
    path('<int:pk>/',views.ShoppingItemDetail.as_view()),
    path('tag/<str:slug>/',views.tag_page),
    path('<int:pk>/new_comment/',views.new_comment),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('category/<str:slug>/',views.category_page),
    path('m_company/<str:slug>/',views.company_page),
    path('create_post/',views.ShoppingItemCreate.as_view()),
    path('update_post/<int:pk>/',views.ShoppingItemUpdate.as_view()),
    path('search/<str:q>/', views.ShoppingItemSearch.as_view()),
    path('delete_comment/<int:pk>/',views.delete_comment),
]
