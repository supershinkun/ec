from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *

# user.pkで、同一ユーザーか確認(ユーザー情報画面、編集画面)
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']

# ショッピングカートとuser.pkが異なるので、わちゃわちゃしてユーザーが同一か確認(ショッピングカート画面)
class CartMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        spc = ShoppingCart.objects.filter(id=self.kwargs['pk']).first()
        return user.pk == spc.user_id



