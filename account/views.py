from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import AccountUser, WorkPlace
from .forms import AdminUserForm, SingleUserForm, AccountAuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives, EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.workplace_id:
            return redirect('account:index', workplace=request.user.workplace_id)
        else:
            return redirect('account:single-index')
    return render(request, 'home.html')

def signup(request):
    context = {}
    
    if request.method == 'POST':
        adminform = AdminUserForm(request.POST or None)
        userform = SingleUserForm(request.POST or None)
        if adminform.is_valid():

            adminform.save()
            email = adminform.cleaned_data.get('email')
            raw_password = adminform.cleaned_data.get('password1')
            # workplace = adminform.cleaned_data.get('workplace')
            # adminuser = authenticate(email=email, password=raw_password)
            # login(request, adminuser)
            # return redirect('account:index', workplace=workplace)
            if email:
                htmly = get_template('account/activate_email.html')
                subject = "Test Activation email"
                d = {
                    'email': email,
                    'url': reverse('account:activate', kwargs={"email":email})
                }
        
                from_email = settings.EMAIL_HOST_USER
                html_content = htmly.render(d)   
                msg = EmailMessage(subject, html_content, from_email, [email])
                msg.content_subtype = "html" 
                try:
                    
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, "An Activation email has been sent to your address, check your email to activate!")
                return redirect('account:sent-email')
            return redirect('account:activate-email', email=email)
        elif userform.is_valid():
            userform.save()
            email = adminform.cleaned_data.get('email')
            raw_password = adminform.cleaned_data.get('password1')
          
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('account:single-index')
        else:
            context['adminform'] = adminform
            context['userform'] = userform
         
    else:
        adminform = AdminUserForm()
        userform = SingleUserForm()
        context['adminform'] = adminform
        context['userform'] = userform
     
    return render(request, 'account/signup.html', context)

def signup_workplace(request, workplace, email):
    workplace_id = get_object_or_404(WorkPlace, name=workplace)
    context = {'workplace': workplace_id.name,
               'email': email}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if first_name and last_name and username and password1 and password2:
            if password1 != password2:
                messages.error(request, "Password do not match")
                return render(request, 'account/signup_workplace.html', context)
            
            AccountUser.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                workplace_id = workplace_id,
                password = make_password(password1),
                is_staff = True,
                is_active = True
                # password2 = make_password(password2),
            )
            # account = authenticate(email=account_user.email, password=account_user.password)
            # login(request, account)
            messages.success(request, "You have successfully signed up to this workplace!")
            return redirect('account:login')
                
    
    return render(request, 'account/signup_workplace.html', context)

def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:

        if user.workplace_id:
            return redirect('account:index', workplace=user.workplace_id)
        else:
            return redirect('account:single-index')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user and user.workplace_id:
                login(request, user)
                return redirect('account:index', workplace=user.workplace_id)
            elif user and not user.workplace_id:
                login(request, user)
                return redirect('account:single-index')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form

    return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('account:home')

@login_required
def index(request, workplace):
    workplace = request.user.workplace_id.name
    # context = {'users': users,
    #            'users_count': users_count}
    return render(request, 'project/welcome.html', {'workplace':workplace})

@login_required
def manage_users(request, workplace):
    workplace_id = get_object_or_404(WorkPlace, name=workplace)
    # user_workplace = AccountUser.objects.exclude(email=request.user.email)
    users = AccountUser.objects.filter(workplace_id=workplace_id)
    users_count = len(users)
    
    context = {'users': users,
               'users_count': users_count}
    return render(request, 'project/manage_users.html', context)

@login_required
def user_detail(request, slug, workplace=None):
    context = {}
    if workplace:
        workplace_id = get_object_or_404(WorkPlace, name=workplace)
        user = get_object_or_404(AccountUser, workplace_id=workplace_id, slug=slug)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            role = request.POST.get('role')

            if first_name or last_name or username or role:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                if role:
                    user.role = role
                else:
                    user.role = user.role
                user.save()
                messages.info(request, "The account details for this user has been updated")
                return redirect('account:user-detail', slug=slug, workplace=workplace)
        context['user'] = user
    else:
        user = get_object_or_404(AccountUser, slug=slug)
        context['user'] = user
    return render(request, 'account/user_detail.html', context)

def single_user_index(request):
    return render(request, 'project/single_user_index.html')

def activate_email(request, email):
    user = get_object_or_404(AccountUser, email=email)
    # user.is_active = True
    # user.save()
    context = {
        'user': user,
        'url': reverse('account:activate', kwargs={"email":user.email})
    }
    return render(request, 'account/activate_email.html', context)

def activate(request, email):
    # print(email)
    user = get_object_or_404(AccountUser, email=email)
    print(user)
    if user.is_active is False:
        user.is_active = True
        user.save()
        messages.info(request, "Your account has been activated!")
        return redirect('account:login')
    else:
        messages.info(request, "Your account has been activated already")
        return redirect('account:login')

def sent_mail(request):
    return render(request, 'account/sent_email.html')

@login_required
def invite_users(request, workplace):
    workplace_id = request.user.workplace_id.name
    if request.method == 'POST':
        get_emails = request.POST.get('emails')
        emails = get_emails.split()
        print(emails)
        from_email = request.user.email
        subject = "{} is inviting you to join its workplace".format(workplace_id)
        htmly = get_template('account/invite.html')
        
        for i in range(len(emails)):
            email = emails[i]
            print(email)
            d = {
                    'email': email,
                    'url': reverse('account:signup-workplace', kwargs={"workplace":workplace_id,
                    'email':email})
                }
            html_content = htmly.render(d)
            msg = EmailMessage(subject, html_content, from_email, [email])
            msg.content_subtype = "html" 
            msg.send()
            # try:
            # send_mail(subject, get_mssg, from_email, [email], fail_silently = False)
                    
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            messages.success(request, "You have sent an invite to {}!".format(email))
        return redirect('account:manage_users', workplace=workplace_id)
    return render(request, 'account/add_user_form.html')
 