from django.shortcuts import render

# @login_required
def show_att(request):
    
    context = {
    }

    return render(request, "att.html", context)


# def user_login(request):
#     form = AuthenticationForm()
    
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             response = HttpResponseRedirect(reverse("main:show_att"))
#             response.set_cookie('last_login', str(datetime.datetime.now()))
#             return response
#         else:
#             messages.error(request, "Invalid username or password. Please try again.") 

#     context = {'form': form}
#     return render(request, 'login.html', context)


# def search_instance(request):
#     return render(request, "search_instance.html", )

