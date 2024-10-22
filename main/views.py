from django.shortcuts import render

def show_att(request):
    
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "att.html", context)

# def search_instance(request):
#     return render(request, "search_instance.html", )

