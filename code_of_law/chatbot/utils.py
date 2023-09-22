import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
import smtpd
import smtplib

def sendotp(request):
    totp=pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp=totp.now()
    request.session['otp_secret_key']=totp.secret
    valid_date=datetime.now()+timedelta(minutes=5)
    request.session['otp_valid_date']=str(valid_date)
    send_mail('OTP Verification',f'Your one time password is {otp}',request.session['src-mail'],[request.session['dest-mail'],])
    print(f"Your one time password is {otp}")