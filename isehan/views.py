from django.views.generic import *
# from .models import *
from django.contrib.auth.views import LoginView
from .forms import *
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.urls import reverse
from .forms import UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OnlyYouMixin, CartMixin
from django.db.models import Q



# Create your views here.
class TopPage(TemplateView):
    model = Product
    template_name = 'isehan/top.html'

    def get_context_data(self, **kwargs):
        context = super(TopPage, self).get_context_data(**kwargs)
        products = Product.objects.all()
        context['all_items'] = products
        random_items = Product.objects.order_by('?')[:4]
        context['random_items'] = random_items
        context
        return context

class BasePage(TemplateView):
    template_name = 'isehan/base.html'


class ItemList(ListView):
    model = Product
    template_name = 'isehan/item_list.html'

    def get_queryset(self):
        products = Product.objects.all()
        if 'query' in self.request.GET and self.request.GET['query'] != None:
            query = self.request.GET['query']
            products = products.filter(name__icontains=query)
        return products


class ItemDetail(DetailView):
    model = Product
    template_name = 'isehan/item_detail.html'


class ParentCategoryView(TemplateView):
    template_name = 'isehan/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(ParentCategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        category_items = Product.objects.filter(p_category=category_id)
        context['category_items'] = category_items
        context['category_name'] = ParentCategory.objects.filter(id=category_id)
        return context

class CategoryView(TemplateView):
    template_name = 'isehan/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        category_items = Product.objects.filter(
            Q(category1=category_id)
        )
        context['category_items'] = category_items
        context['category_name'] = Category.objects.filter(id=category_id)
        return context



class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'isehan/login.html'

class SignUp(CreateView):
    """ユーザー仮登録"""
    template_name = 'isehan/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('isehan/mail_template/signup/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('isehan/mail_template/signup/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        messages.success(self.request, '本登録用リンクを送付しました')
        return HttpResponseRedirect(reverse('isehan:signup'))

class SignUpDone(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'isehan/signup_done.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()

                    his_cart = ShoppingCart()
                    his_cart.user = user
                    his_cart.save()

                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class UserDetailView(OnlyYouMixin, DetailView):
    model = User
    template_name = 'isehan/user_detail.html'

class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = 'isehan/user_update.html'
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('isehan: user_detail', pk=self.kwargs['pk'])


class ShoppingCartDetail(CartMixin, DetailView):
    model = ShoppingCart
    template_name = "isehan/shopping_cart.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        product_pk = request.POST.get('product_pk')
        product = Product.objects.get(pk=product_pk)
        amount = request.POST.get('amount')

        exist = ShoppingCartItem.objects.filter(cart__user=user).filter(product=product)

        # すでにカートに存在する商品の場合は個数をインクリメント
        if len(exist) > 0:
            current_amount = exist[0].amount
            exist[0].amount = current_amount + int(amount)
            exist[0].save()
        else:
            new_cart_item = ShoppingCartItem()
            new_cart_item.cart = request.user.cart
            new_cart_item.product = product
            new_cart_item.amount = int(amount)
            new_cart_item.save()
        return HttpResponseRedirect(reverse('isehan:cart', kwargs={'pk': self.get_object().pk}))

def update_cart_item_amount(request):
    cart_item_pk = request.POST.get('cart_item_pk')
    new_amount = request.POST.get('amount')

    if cart_item_pk == None or new_amount == None:
        return JsonResponse({'error': 'invalid parameter'})
    if int(new_amount) <= 0:
        return JsonResponse({'error': 'amount must be greater than zero'})

    try:
        cart_item = ShoppingCartItem.objects.get(pk=cart_item_pk)
        cart_item.amount = int(new_amount)
        cart_item.save()
        print(cart_item.amount)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})

def delete_cart_item(request):
    cart_item_pk = request.POST.get('cart_item_pk')
    if cart_item_pk == None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        cart_item = ShoppingCartItem.objects.get(pk=cart_item_pk)
        cart_item.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})
