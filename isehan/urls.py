from django.conf.urls import url
from django.urls import path
from isehan import views
from django.contrib.auth import views as django_auth_views

app_name = 'isehan'

urlpatterns = [
    path('', views.TopPage.as_view(), name='top'),
    path('base/', views.BasePage.as_view(), name='base'),
    path('items/', views.ItemList.as_view(), name='item_list'),
    path('items/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('parent_category/<int:pk>', views.ParentCategoryView.as_view(), name='parent_category_view'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category_view'),
    path('login', views.Login.as_view(), name="login"),
    path('logout', django_auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup_done/<token>', views.SignUpDone.as_view(), name='signup_done'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path('cart/<int:pk>', views.ShoppingCartDetail.as_view(), name='cart'),
    path('ajax_amount/', views.update_cart_item_amount, name='update_cart_item_amount'),
    path('ajax_delete/', views.delete_cart_item, name='delete_cart_item'),
]



