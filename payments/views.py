import stripe
import json
import datetime
import os
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import logout
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from dateutil.relativedelta import relativedelta
from imagediff.models import Config

class HomePageView(TemplateView):
    template_name = 'payments/home.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        amount_dict = {
            "1 Month": ["12000", "1", "ITEM01"],
            "1 Year" : ["132000", "12", "ITEM02"],
            "3 Years": ["360000", "36", "ITEM03"],
            }
        data = json.loads(request.body)
        # domain_url = 'http://localhost:8000/'
        domain_url = os.getenv("DOMAIN")
        # item_name = "Imagediff {} Membership".format(data["item_name"])
        price = os.getenv(amount_dict.get(data["item_name"])[2])
        if int(data["mode"]) == 0:
            success_url = domain_url + "accounts/signup_step4/?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = domain_url + "accounts/signup_login/?id={}&re=0".format(request.user.username)
        else:
            success_url = domain_url + "accounts/signup_step4_update/?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = domain_url + "accounts/signup_login/?id={}&re=1".format(request.user.username)
        stripe.api_key = settings.STRIPE_SECRET_KEY
            
        try:
            if request.user.is_authenticated:
                client_reference_id = "{}_{}_{}".format(request.user.id, request.user.email, amount_dict.get(data["item_name"])[1])
                email = request.user.email
            else:
                return JsonResponse({'error': "ユーザーのログインが確認できませんでした。"})    
            if request.user.id is None:
                pass
            else:
                logout(request)
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=client_reference_id,
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=email,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': price,
                        # 'name': item_name,
                        'quantity': 1,
                        # 'currency': os.getenv("CURRENCY"),
                        # 'amount': amount_dict.get(data["item_name"])[0],
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # print("Payment was successful.")
        # print(event["data"]["object"]["client_reference_id"])
        if event["data"]["object"]["client_reference_id"] is None:
            pass
        else:
            item_list = event["data"]["object"]["client_reference_id"].split("_")
            today = datetime.date.today()
            try:
                obj = Config.objects.get(user_id=item_list[0])
                if obj.expiration_date > today:
                    value = obj.expiration_date + relativedelta(months=int(item_list[2]))
                else:
                    value = today + relativedelta(months=int(item_list[2]))
                setattr(obj, "expiration_date", value)
                setattr(obj, "frequency_limit", None)
                obj.save()
            except Config.DoesNotExist:
                obj = Config(
                    user_id=item_list[0],
                    alert_id=item_list[0],
                    email=item_list[1],
                    expiration_date=today + relativedelta(months=int(item_list[2]))
                    )
                obj.save()

    return HttpResponse(status=200)


def free(request):
    if request.method == "POST":
        try:
            obj = Config.objects.get(user_id=request.user.id)
        except Config.DoesNotExist:
            obj = Config(
                user_id=request.user.id,
                alert_id=request.user.id,
                email=request.user.email,
                expiration_date=datetime.date.today() + relativedelta(months=1),
                frequency_limit=50
                )
            obj.save()
    return redirect("accounts:signup_step4")