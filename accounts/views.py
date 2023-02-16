# import urllib.parse
import unicodedata
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in, authenticate, login as auth_login, logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.dispatch.dispatcher import receiver
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from imagediff.functions.SQL import MySQL
from .forms import SignUpForm, LoginForm
from .models import UserSession

# 決済ページ関連
# import stripe
# import json
# import os
# from django.http.response import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# ユーザログイン時に他セッションを削除する
@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    Session.objects.filter(usersession__user=user).delete()
    request.session.save()
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
    )


def terms_service(request):
    return render(request, "accounts/terms_service.html", {})


def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html", {})


def signup_step1(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        # ユーザー名チェック
        chk_flg = 0
        for c in request.POST.get("username"):
            if unicodedata.east_asian_width(c) != "Na":
                chk_flg = 1
                break

        if chk_flg == 0:
            if form.is_valid():
                # アカウント仮登録
                user = form.save()

                # 認証メール送信
                subject = "【Imagediff】アカウント登録のお知らせ"
                message = ""
                message += "{}様\n\n".format(user.username)
                message += "この度は、画像内テキスト比較サービス「Imagediff tgt.Text」の利用をご検討いただき、誠にありがとうございます。\n\n"
                message += "下記のURLから利用プランを選択し、登録を完了してください。\n"
                message += "http://127.0.0.1:8000/accounts/signup_login/?id={}&re=0\n\n".format(user.username)
                message += "本メールはhttp://127.0.0.1:8000より自動送信されています。\n"
                message += "心当たりのない場合は破棄をお願いします。\n\n"
                message += "※お問い合わせについては、{}にお送りください。".format(settings.EMAIL_HOST_USER)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)

                return redirect("accounts:signup_step2")
        else:
            messages.error(request, "ユーザ名は半角英数のみ登録できます。")

    else:

        form = SignUpForm()

    d = {
        "mode": 0,
        "step": 1,
        "form": form
        }

    return render(request, "accounts/signup_step1.html", d)


def signup_step2(request):

    d = {
        "mode": 0,
        "step": 2
        }

    return render(request, "accounts/signup_step2.html", d)

# @login_required
# def signup_step3(request):

#     d = {
#         "step": 3,
#         "publick_key": settings.STRIPE_PUBLIC_KEY,
#         "email": request.user.email,
#         }

#     if request.method == "POST":
#         token = request.POST.get("stripeToken")
#         try:
#             # 購入処理
#             charge = stripe.Charge.create(
#                 amount=10000,
#                 currency='jpy',
#                 source=token,
#                 description='メール:{} 書籍名:Imagediff'.format(request.user.email),
#             )
#         except stripe.error.CardError as e:
#             # カード決済不成立
#             message = ""
#             message += "購入手続きが完了しませんでした。\n"
#             message += "クレジットカード情報が正しく入力されていることをご確認ください。"

#             messages.error(request, message)

#         else:
#             # カード決済成立
#             return redirect("signup_step4")

#     return render(request, "accounts/signup_step3.html", d)


@login_required
def signup_step3(request):
    data = MySQL().get_imagediff_config(0, request.user.id)     # 登録確認
    free_view = 1 if len(data) == 0 else 0  # free_view[0: お試しプラン非表示, 1: お試しプラン表示]

    d = {
        "mode"     : 0,
        "step"     : 3,
        "free_view": free_view
        }

    return render(request, "accounts/signup_step3.html", d)

# @csrf_exempt
# def onetime_payment_checkout(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         # domain_url = "http://127.0.0.1:8000/"
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url="http://127.0.0.1:8000/accounts/signup_step4/?session_id={CHECKOUT_SESSION_ID}",
#                 cancel_url="http://127.0.0.1:8000/accounts/signup_step4/",
#                 payment_method_types=["card"],
#                 line_items=[
#                     {
#                         "name": "Pasha photo",
#                         "quantity": "1",
#                         "currency": "jpy",
#                         "amount": "10000",
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error':str(e)})

# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {
#             'publicKey': settings.STRIPE_PUBLIC_KEY,
#             'basePrice': "10000",
#             'currency': "jpy",
#         }
#         return JsonResponse(stripe_config, safe=False)

def signup_step4(request):
    
    if request.user.id is None:
        pass
    else:
        logout(request)

    d = {
        "mode": 0,
        "step": 4,
        "mail": settings.EMAIL_HOST_USER,
        }

    return render(request, "accounts/signup_step4.html", d)

@login_required
def signup_step3_update(request):

    # data = MySQL().get_imagediff_config(0, request.user.id)     # 登録確認
    # free_view = 1 if len(data) == 0 else 0  # free_view[0: お試しプラン非表示, 1: お試しプラン表示]

    d = {
        "mode"     : 1,
        "step"     : 3,
        "free_view": 0
        }

    return render(request, "accounts/signup_step3.html", d)

def signup_step4_update(request):

    if request.user.id is None:
        pass
    else:
        logout(request)

    d = {
        "mode": 1,
        "step": 4,
        "mail": settings.EMAIL_HOST_USER,
        }

    return render(request, "accounts/signup_step4.html", d)


class Signup_Login(View):

    def get(self, request):
        if request.user.id is None:
            pass
        else:
            logout(request)
        d = {
            "form"       : LoginForm(request.GET or None, initial={"username": request.GET.get("id")}),
            "signup_user": request.GET.get("id"),
            }
        return render(request, "accounts/login.html", d)

    def post(self, request):
        d = {
            "form"       : LoginForm(request.POST, initial={"username": request.GET.get("id")}),
            "signup_user": request.GET.get("id"),
            }

        # ユーザー認証
        user = authenticate(username=request.POST.get("signupUser"), password=request.POST.get("password"))
        if user is None:
            messages.error(request, "パスワードに誤りがあります。")
            return render(request, "accounts/login.html", d)

        else:
            auth_login(request, user)

        if request.GET.get("re") == "0":
            return HttpResponseRedirect(reverse("accounts:signup_step3"))
        else:
            return HttpResponseRedirect(reverse("accounts:signup_step3_update"))

# class PasswordChange(PasswordChangeView):
#     form_class = MyPasswordChangeForm
#     success_url = reverse_lazy('register:password_change_done')
#     template_name = 'register/password_change.html'


# class PasswordChangeDone(PasswordChangeDoneView):
#     template_name = 'register/password_change_done.html'