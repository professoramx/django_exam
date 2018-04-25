from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.quotes.models import *
import bcrypt
import datetime

# for all logged in pages, if no user id is stored in session user is redirected to main page

# redirects to main page
def index(request):
    return redirect('/main')

# redirects to dashboard if already logged in, otherwise displays login/registration template
def main(request):
    if 'id' in request.session:
        return redirect('/quotes')
    return render(request, "quotes/index.html")

# processes registration -- redirects to dashboard if successful, othewise redirects to main page
def register(request):
    if request.method == 'GET':
        return redirect ('/main')
    newUser = User.objects.validate(request.POST)
    if newUser[0] == False:
        for each in newUser[1]:
            messages.error(request, each) 
        return redirect('/main')
    if newUser[0] == True:
        messages.success(request, 'User registered successfully.')
        request.session['id'] = newUser[1].id
        return redirect('/quotes')

# processes login -- redirects to dashboard if successful, otherwise redirects to main page
def login(request):
    if 'id' in request.session:
        return redirect('/quotes')
    else:
        user = User.objects.login(request.POST)
        if user[0] == False:
            for each in user[1]:
                messages.error(request, each)
            return redirect('/main')
        if user[0] == True:
            messages.success(request, 'Logged in successfully.')
            request.session['id'] = user[1].id
            return redirect('/quotes')

# processes logout and redirects to main page
def logout(request):
    if 'id' not in request.session:
        return redirect('/main')
    del request.session['id']
    return redirect('/main')

# dashboard page -- displays contributed quotes, favorited quotes, and form to contribute new quotes
def quotes(request):
    if 'id' not in request.session:
        return redirect ("/main")
    context = {
        "user": User.objects.get(id=request.session['id']),
        "quotes": Quote.objects.all().exclude(users__id=request.session['id']),
        "favorites": Quote.objects.all().filter(users__id=request.session['id'])
    }
    return render(request, "quotes/quotes.html", context)

# processes quote contributions
def contributeQuote(request):
    if 'id' not in request.session:
        return redirect ('/main')
    if request.method == 'GET':
        return redirect ('/quotes')
    newQuote = Quote.objects.validate(request.POST, request.session['id'])
    if newQuote[0] == False:
        for each in newQuote[1]:
            messages.error(request, each) 
        return redirect('/quotes')
    if newQuote[0] == True:
        messages.success(request, 'Quote posted successfully.')
        return redirect('/quotes')

# adds a quote to logged in user's favorites
def addQuote(request, id):
    if 'id' not in request.session:
        return redirect ('/main')
    user = User.objects.get(id=request.session['id'])
    try:
        selectedQuote = Quote.objects.get(id=id)
    except:
        messages.error(request, 'Could not add quote to your favorites: Quote not found.')
        return redirect('/quotes')
    user.favorite_quotes.add(selectedQuote)
    messages.success(request, 'Quote by ' + selectedQuote.quoted_by + ' added to your favorites successfully.')
    return redirect('/quotes')

# removes a quote from logged in user's favorites
def removeQuote(request, id):
    if 'id' not in request.session:
        return redirect ('/main')
    user = User.objects.get(id=request.session['id'])
    try:
        selectedQuote = Quote.objects.get(id=id)
    except:
        messages.error(request, 'Could not remove quote from your favorites: Quote not found.')
        return redirect('/quotes')
    user.favorite_quotes.remove(selectedQuote)
    messages.warning(request, 'Quote by ' + selectedQuote.quoted_by + ' removed from your favorites.')
    return redirect('/quotes')

# displays user's profile with contributed quotes
def profile(request, id):
    if 'id' not in request.session:
        return redirect ("/main")
    context = {
        "user": User.objects.get(id=request.session['id']),
        "profile": User.objects.get(id=id),
        "quotes": Quote.objects.all().filter(posted_by__id=id)
    }
    return render(request, "quotes/profile.html", context)
