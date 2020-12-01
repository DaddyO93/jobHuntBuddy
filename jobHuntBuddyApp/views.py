from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from .models import User, Company, Position, ContactPerson, FollowUpDate
from django.contrib import messages
import bcrypt

# Pages
def index(request):
    return render(request, 'index.html')

def main (request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in!")
        return redirect ('/')
    else:
        user = User.objects.filter(id=request.session["user_id"])[0]
        context = {
            "all_positions": Position.objects.all(),
            "user": user,
        }
        return render(request, "main.html", context)

def position_details (request, position_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in!")
        return redirect ('/')
    else:
        user = User.objects.filter(id=request.session["user_id"])[0]
        position = Position.objects.filter(id=position_id)[0]
        # contacts = ContactPerson.objects.all()
        contacts = ContactPerson.objects.filter(position=position)
        followUp = position.follow_up_date.all()
        context = {
            "user": user,
            "position": position,
            "all_contacts": contacts,
            "all_dates": followUp
        }
        return render(request, "position_details.html", context)
    

# User functions
def log_out (request):
    request.session.clear()
    return redirect ('/')

def register (request):
    if request.method =='POST':
        errors = User.objects.loginValidator(request.POST) 
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password = request.POST['user_password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name=request.POST['user_first_name'], last_name=request.POST['user_last_name'], email=request.POST['user_email'], password=pw_hash)
            request.session['user_id'] = new_user.id
            return redirect ("/success")
    else:
        return redirect ('/')

def login (request):
    if request.method == 'GET':
        return redirect ('/')
    elif request.method == 'POST':
        user = User.objects.filter(email=request.POST['login_email'])
        if len(user)>0:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect ('/success')
            else:
                messages.error(request, "Your Email or Password are incorrect!")
                return redirect ('/')
        else:
            messages.error(request, "You must register first!")
            return redirect ('/')
        

# Position functions
def add_position (request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, "You must be logged in!")
            return redirect ('/')
        else:
            user = User.objects.filter(id=request.session["user_id"])[0]
            if len(request.POST['date_applied'])>1:
                date_applied = request.POST['date_applied']
            else:
                date_applied = None
            # Create new instance of Company, if does not already exist
            company_applied_at = Company.objects.filter(name=request.POST['company'])
            if len(company_applied_at)==0:
                company = company_applied_at.create(name=request.POST['company'])
            else:
                company = company_applied_at[0]
            new_position = Position.objects.create(user=user, date_applied=date_applied, position_applied_for=request.POST['position'], company=company)
            messages.error(request, f"{new_position.position_applied_for} entered!")
            new_position.save()
    return redirect("/success")

    

# Contact Functions
def add_contact_to_position (request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, "You must be logged in!")
            return redirect ('/')
        else:
            user = User.objects.filter(id=request.session["user_id"])[0]
            # Check to see if company has been added, if not add it
            company_applied_at = Company.objects.filter(name=request.POST['contact_company'])
            if len(company_applied_at)==0:
                company_name = Company.objects.create(name=request.POST['contact_company'])
            else:
                company_name = company_applied_at[0]   
            # Check to see if contact has been added, if not add them
            position_contact = ContactPerson.objects.filter(contact_person=request.POST['contact_name'])
            if len(position_contact)==0:
                new_contact = ContactPerson.objects.create(contact_person = request.POST['contact_name'], contact_email=request.POST['contact_email'], company=company_name, position=request.POST['contact_company'], note=request.POST['contact_note'])
                new_contact.save()
            else:
                new_contact = position_contact
                Position.contact_person = new_contact
                # Position.save()
            messages.error(request, f"New contact, {new_contact.contact_person}, added")
    return redirect ('/success')

def remove_contact (request, position_id, contact_id):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, "You must be logged in!")
            return redirect ('/')
        else:
            user = User.objects.filter(id=request.session["user_id"])[0]
            position = Position.objects.filter(id=position_id)
            contact = ContactPerson.objects.filter(id=contact_id)
            position.contact_person.remove()
            print(position.contact_person.all())
    return redirect('/success')
            