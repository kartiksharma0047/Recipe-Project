from django.shortcuts import render, redirect
from .models import Receipe

def receipes(request):
    if request.method == "POST":
        receipe_name = request.POST.get('receipe_name')
        receipe_description = request.POST.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        # Here Page will get redirected and dosen't hold data of previous form
        return redirect('receipes')

    queryset = Receipe.objects.all()
    return render(request, 'Pages/recepies.html', {'receipes': queryset})

def receipes_list(request):
    context = {'context': Receipe.objects.all()}
    return render(request, 'Pages/recepies_List.html', context=context)

def delete_receipe(request, id):
    querySet=Receipe.objects.get(id=id)
    querySet.delete()
    return redirect('/recepies_list')