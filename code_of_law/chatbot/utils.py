import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
import smtpd
import smtplib
import spacy
import re
import jinja2
import pdfkit
from datetime import *
import os

def sendotp(request):
    totp=pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp=totp.now()
    request.session['otp_secret_key']=totp.secret
    valid_date=datetime.now()+timedelta(minutes=5)
    request.session['otp_valid_date']=str(valid_date)
    send_mail('OTP Verification',f'Your one time password is {otp}',request.session['src-mail'],[request.session['dest-mail'],])
    print(f"Your one time password is {otp}")






def duration(from_date, to_date):
    month_to_number = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    
    froms = from_date.split()
    tos = to_date.split()
    
    month1 = month_to_number.get(froms[1])
    month2 = month_to_number.get(tos[1])
    year1 = int(froms[2])
    year2 = int(tos[2])
    
    if year2 > year1 or (year2 == year1 and month2 >= month1):
        dur_month = month2 - month1
        dur_year = year2 - year1
        return dur_month + dur_year * 12
    else:
        dur_month = 12 - (month1 - month2)
        dur_year = year2 - year1 - 1
        return dur_month + dur_year * 12

    # if int(tos[2]) - int(froms[2]) < 2:
    #     if num1 == num2:
    #         return int(tos[2]) - int(froms[2]) * 12
    #     elif num1 > num2:
    #         return 12 - (num1 - num2-1)
    #     else:
    #         return num2 - num1
    # else:
    #     if num1 == num2:
    #         return 12 + (int(froms[2]) - int(tos[2]) * 12)
    #     elif num1 > num2:
    #         return (12 - (num1 - num2-1)) + 12
    #     else:
    #         return 12 + (num2 - num1)



def nlpwork():
    file_path = 'D:/Languages/SIH/Code-of-Law/code_of_law/chatbot/Prompt.txt'
    nlp = spacy.load('en_core_web_lg')
    with open(file_path, "r") as file:
        prompt = file.read()

    #
    # prompt = 'Draft a rent agreement between Mr. Ayush and Mr. Kartik for a tenure of 12 months wherein he will pay a monthly rent of Rs 12000 and a security deposit of Rs 35000 one time. This will be effective from 23rd September 2023 till 1st March 2024'
    # prompt = 'Draft a lease agreement which is executed on 22nd September 2023 with Mr. Sharma acting as lessor and Mr. Ravishankar acting as the lessee. Mr. Ravishankar wants to rent Flat No 23 in Gokuldham Society for  residential purpose. The lease would start from 30th September 2023 and will last till 30th September 2024 for the fixed monthly rent of Rs 30000 and a fixed deposit of Rs 15000'
    doc = nlp(prompt)
    dates = []
    names = []
    rates = []
    rent_amount = 0
    security_deposit = 0
    lessor = ''
    lesse = ''


    for ent in doc.ents:

        if ent.label == 380:
            if ent.text not in names:
                names.append(ent.text)
                
        elif ent.label == 391:
            if ent.text not in dates:
                dates.append(ent.text)
        elif ent.label == 394:
            if ent.text not in rates:
                rates.append(ent.text)


    rent_amount = min(rates)
    security_deposit = max(rates)
    words = prompt.split()
    tokens = prompt.split('.')
    lessor = names[0]
    lesse = names[1]
    # print(names)
    # print(lessor)
    # print(lesse)
    # print(rent_amount)
    # print(security_deposit)

    # print(names,rates,dates)
    from_date = ''
    to_date = ''
    for date in dates:
        for i in range(1,len(words)-2):
            if words[i-1] + ' ' + words[i] + ' ' + words[i+1] == date:
                if i>=2 and i<=len(words)-2:
                    if words[i-2] == 'from':
                        from_date = date
                    elif words[i-2] == 'to' or words[i-2] == 'till':
                        to_date = date
    # time_duration = duration(from_date,to_date)
    #print(from_date,to_date)
    # Removing monthly or yearly words
    for tareek in dates:
        if tareek == 'monthly' or tareek == 'yearly':
            #print("Removing: ", tareek)
            dates.remove(tareek)
    for tareek in dates:
        count = len(tareek.split())
        if count == 2:
            time_duration = tareek
            #print("Removing: ", tareek)
            dates.remove(tareek)
        if count == 3:
            from_date = dates[0]
            to_date = dates[1]


    #time_duration = 16

    today_date = datetime.today().strftime("%d %b, %Y")

    context = {'today_date':today_date, 'lessor':lessor, 'lesse':lesse, 'rent': rent_amount, 'duration': time_duration, 'from_date':from_date,'end_date':to_date}

    template_loader =  jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    agreement_path='D:/Languages/SIH/Code-of-Law/code_of_law/chatbot/Agreement.html'
    template = template_env.get_template('rD:/Languages/SIH/Code-of-Law/code_of_law/chatbot/templates/chatbot/Agreement.html')
    output = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output, 'Rent_Agreement.pdf', configuration=config)
    print(dates, names, rates)
    print(from_date,to_date, time_duration)
    return "PDF created succesfully"
            