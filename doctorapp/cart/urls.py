from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns=[
    url(r'^home/', views.home, name='home'),
    path('itemlist/', views.itemlist, name='itemlist'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('search/', views.searchpage , name='searchpage'),
    path('searchitem/', views.search , name='search'),
    path('checkout/', views.checkout , name='checkout'),
    path('productpage/(?P<Id>[0-9]+)', views.product_page, name='product_page'),
    path('add_to_cart/(?P<Item_id>[0-9]+)',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/(?P<Item_id>[0-9]+)',views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/(?P<Item_id>[0-9]+)',views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add_single_item_into_cart/(?P<Item_id>[0-9]+)',views.add_single_item_into_cart, name='add_single_item_into_cart')

]

