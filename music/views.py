from django.core import paginator
from django.shortcuts import render,redirect, HttpResponse
from music.models import Song, Favourites, History, Profile
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, When
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from music.models import Song
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import stripe
from django.views.generic import ListView, DetailView, View
import datetime
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailConfirmed
from django.shortcuts import get_object_or_404


stripe.api_key = "sk_test_51JicMwE0KuM0o8WdCeGXQNvegVcFAN2qV5X8a6ojZtaLZkihUxi9x9GsOAZUqCVwYxTBdSYHJ6NxAEEMObZUFzND00ao6job8B"





def email_confirm(request, activation_key):
    user= get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed=True
        user.save()

        myuser=User.objects.get(email=user)
        myuser.is_active=True
        myuser.save()
        first_name = myuser.first_name
        last_name = myuser.last_name
        condict = {'first_name':first_name, 'last_name':last_name}
        return render(request, 'music/registration_complete.html', condict)


def index(request):
    song = Song.objects.all()
    paginator=Paginator(song,6)
    page=request.GET.get('page')
    paged_song=paginator.get_page(page)
    song_count=song.count()
    context={
        'song': song,
        'song': paged_song,
        'song_count':song_count,

    }
    return render(request, 'music/home.html',context)


def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/music/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'music/history.html', {"history": song})


def favourites(request):
    if request.method == "POST":
        user = request.user
        fav_id = request.POST['fav_id']

        fav = Favourites.objects.filter(user=user)
        
        for i in fav:
            if fav_id == i.fav_id:
                message = "Your Song is Already Added"
                break
        else:
            favourites = Favourites(user=user, fav_id=fav_id)
            favourites.save()
            message = "Your Song is Succesfully Added"

        song = Song.objects.filter(song_id=fav_id).first()
        return render(request, f"music/songpost.html", {'song': song, "message": message})

    wl = Favourites.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.fav_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "music/favourite.html", {'song': song})


def search(request):
    context={}
    if request.GET:
        query=request.GET['query']
        queries = query.split(' ')
    queryset = []
    try:
        for q in queries:
            song = Song.objects.filter(
                Q(name__icontains=q) |
                Q(singer__icontains=q) |
                Q(album__icontains=q)
            )
        for pro in list(set(song)):
            queryset.append(pro)
        
        #if query exist
        if list(set(queryset)):
            context = {
            'query': list(set(queryset)),
            'query_str':str(query)
        }
        #if query don't exist
        else:
            context = {
            'notfound':True,
            'query_str':str(query),
        }
            
    except:
        #any exception during search
        context = {
         'notfound':True,
        'query_str':str(query),
        }
        
    return render(request, 'music/search.html', context)


def songs(request):
    song = Song.objects.all()
    paginator=Paginator(song,6)
    page=request.GET.get('page')
    paged_song=paginator.get_page(page)
    song_count=song.count()
    context={
        'song': song,
        'song': paged_song,
        'song_count':song_count,

    }
    return render(request, 'music/songs.html',context)


@login_required(login_url='login')
def songpost(request, id):
    song = Song.objects.filter(song_id = id).first()

    check_my_pr = None
    if Profile.objects.filter(user=request.user):
        check_my_pr = Profile.objects.get(user=request.user)

    return render(request, 'music/songpost.html', {'song': song, 'check_my_pr':check_my_pr})


def signup(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('signup')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('signup')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.is_active = False
          user.save()
          myuser = user

          # send mail
          user_email_confirmed = EmailConfirmed.objects.get(user=myuser)
          print(user_email_confirmed)
          site = get_current_site(request)
          print(site)

          email = myuser.email
          first_name = myuser.first_name
          last_name = myuser.last_name
          print(email, first_name, last_name)

          sub_of_email = "Activation Email From RyzicMix."
          email_body = render_to_string(
              'music/verify_email.html',
              {
                  'first_name': first_name,
                  'last_name': last_name,
                  'email': email,
                  'domain': site.domain,
                  'activation_key': user_email_confirmed.activation_key
              }
          )

          send_mail(
              sub_of_email,  # Subject of message
              email_body,  # Message
              '',  # From Email
              [email],  # To Email
              fail_silently=True
          )


          # messages.success(request, 'You are now registered and can log in')
          messages.success(request, 'An Activation Email Has been Sent to Your Email!!')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('signup')
  else:
    return render(request, 'music/signup.html')




def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)

      messages.success(request, 'You are now logged in')
      return redirect('index')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'music/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect("/")

def subscription(request):
    print('subscription')
    return render(request, "music/subscription.html")




def payment_page(request):
    if request.method == "GET":
        subscription_type = request.GET.get('subscription_type')
        if subscription_type == 'monthly':
            money = 12
            type = 'Monthly Subscription'
        elif subscription_type == 'yearly':
            money = 110
            type = 'Yearly Subscription'
        context = {'money':money, 'type':type}
        return render(request, "music/payment_page.html", context)
    else:
        money_amount_and_type = request.POST.get('money_amount')
        x = money_amount_and_type.split(",")

        subs_name=None
        money_amount=None
        tkn=None

        len = 0
        for i in x:
            len = len + 1
            if len == 1:
                money_amount = i
            elif len == 2:
                subs_name = i
            else:
                tkn = i

        if subs_name == 'Monthly Subscription':
            subscription_type = 'MONTHLY'
            start_date = datetime.date.today()
            expire_date = start_date + relativedelta(months=1)
        elif subs_name == 'Yearly Subscription':
            subscription_type = 'YEARLY'
            start_date = datetime.date.today()
            expire_date = start_date + relativedelta(months=12)

        try:
            customer = stripe.Customer.create(
                email=request.user.email,
                description=request.user.username,
                source=tkn
            )
            print('step2')
            amount = int(money_amount)
            print(amount)
            charge = stripe.Charge.create(
                amount=(amount * 100),
                currency="usd",
                customer=customer,
                description="Payment for Music online",
            )

            if Profile.objects.filter(user=request.user):
                my_pro = Profile.objects.get(user=request.user)
                my_pro.is_premium=True
                my_pro.premium_Start_date = start_date
                my_pro.premium_expiry_date = expire_date
                my_pro.subscription_type=subscription_type
                my_pro.save()

            else:
                new_Profile = Profile(user=request.user, is_premium=True, premium_Start_date=start_date, premium_expiry_date=expire_date, subscription_type=subscription_type)
                new_Profile.save()


            messages.success(request, f'{request.user.username}, Your Payment was Successfull !! Now You are Premium Member Untill {expire_date}. Now Enjoy !!')
            return redirect('index')

        except stripe.error.CardError as e:
            messages.info(request, f"{e.error.message}")
            return redirect('index')

        except stripe.error.RateLimitError as e:
            messages.info(request, f"{e.error.message}")
            return redirect('index')
        except stripe.error.InvalidRequestError as e:
            messages.info(request, "Invalid Request !")
            return redirect('index')
        except stripe.error.AuthenticationError as e:
            messages.info(request, "Authentication Error !!")
            return redirect('index')
        except stripe.error.APIConnectionError as e:
            messages.info(request, "Check Your Connection !")
            return redirect('index')
        except stripe.error.StripeError as e:
            messages.info(request, "There was an error please try again !")
            return redirect('index')
        except Exception as e:
            messages.info(request, "A serious error occured we were notified !")
            return redirect('index')



@csrf_exempt
def check_member(request):
    if Profile.objects.filter(user=request.user):
        chk_pr = Profile.objects.get(user=request.user)
        if chk_pr.is_premium:
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        return HttpResponse(False)


def remove_fav_song(request, pk):
    rmve_fav_song = Favourites.objects.get(user=request.user, fav_id=pk)
    rmve_fav_song.delete()
    return redirect('favourites')


def cancel_membership(request):
    if Profile.objects.filter(user=request.user):
        my_pro = Profile.objects.get(user=request.user)
        my_pro.is_premium = False
        my_pro.premium_Start_date = None
        my_pro.premium_expiry_date = None
        my_pro.subscription_type = 'FREE'
        my_pro.save()
    return redirect('index')
