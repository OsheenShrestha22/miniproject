from django.conf.urls import url
from . import views

app_name = 'tracker'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<transaction_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<item_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^items/(?P<filter_by>[a-zA_Z]+)/$', views.items, name='items'),
    url(r'^create_transaction/$', views.create_transaction, name='create_transaction'),
    url(r'^(?P<transaction_id>[0-9]+)/create_item/$', views.create_item, name='create_item'),
    url(r'^(?P<transaction_id>[0-9]+)/delete_item/(?P<item_id>[0-9]+)/$', views.delete_item, name='delete_item'),
    url(r'^(?P<transaction_id>[0-9]+)/favorite_transaction/$', views.favorite_transaction, name='favorite_transaction'),
    url(r'^(?P<transaction_id>[0-9]+)/delete_transaction/$', views.delete_transaction, name='delete_transaction'),
    url(r'^report_item/$', views.report_item, name='report_item'),
    url(r'^send_mail', views.send_email, name="send_email"),
]


