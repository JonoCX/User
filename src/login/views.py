from django.shortcuts import render, render_to_response
from .forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def register(request):
    # Request the context
    context = RequestContext(request)

    # boolean value for telling the template whether the registration
    # was successful or not
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()

            # Hash the password with set_password then update user object
            user.set_password(user.password)
            user.save()

            # Update registered to say it was successful
            registered = True

        # Invalid form
        else:
            print (user_form.errors)

    # Not a post request, render the form so it is blank
    else:
        user_form = UserForm()

    return render_to_response(
                                'register.html',
                                {'user_form': user_form, 'registered': registered},
                                context
                            )

def user_login(request):
    # Request context
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/login/')
            else:
                return HttpRedirect("Account is disabled")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.htm', {}, context)
