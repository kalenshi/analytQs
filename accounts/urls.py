from django.urls import path

from accounts.views.account_detail_view import AccountDetailView
from accounts.views.user_list_view import UserListView
from accounts.views.user_tokens import CreateTokenView

app_name = "accounts"

urlpatterns = [
    path("create/", UserListView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("account/<user_id>/", AccountDetailView.as_view(), name="account"),
]
