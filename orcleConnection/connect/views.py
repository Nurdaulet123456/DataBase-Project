from django.shortcuts import *
from django.db import connection
# Create your views here.
from .models import *
from django.contrib import messages

def index(request):
    context = {
        'banks': Bank_card.objects.all(),
        'discounts': Discounts.objects.all(),
    }
    if request.method =="POST":
        searched_name = request.POST['name']
        consultants = Consultants.objects.filter(name__icontains=searched_name)
        context['consultants'] = consultants
        context['searched_name'] = searched_name
    return render(request, 'index.html', context)

def edit_discounts(request,):
    d_id = request.POST.get("id")
    discount = Discounts.objects.get(discount_id=d_id)
    discount.discount_id = request.POST.get("id")
    discount.percent = request.POST.get("percent")
    discount.starter_sum = request.POST.get("starter_sum")
    discount.save()
    return redirect('index')

def change_consultant(request, name):
    cons = Consultants.objects.get(name=name)
    if request.POST.get('deleteButton'):
        cons.delete()
    else:
        cons.name = request.POST['name']
        cons.surname = request.POST['surname']
        cons.sales_sum = request.POST['sales_sum']
        cons.save()
        messages.success(request, f"{cons.name} is updated successfully!")
    return redirect('index')

def search(request):
    context = {
        'products': Product_Types.objects.all(),
    }
    if request.method == "POST":
        searched_article = request.POST['article']
        type_id = request.POST['types']
        context['searched_article'] = searched_article
        # if type_id:
        #     try:
        #         product = Product_Types.objects.get(id=type_id)
        #         context['product'] = product
        #     except Product_Types.DoesNotExist:
        #         context['product']=None
        # else:
        #
        try:
            article = Articles.objects.get(article=searched_article)
            product = Product_Types.objects.get(id=article.type_id)
            context['a_product']=product
        except Articles.DoesNotExist:
            article = None
        context['article'] = article

    return render(request, 'search.html', context)



def search_const(request):
    if request.method == "POST":
        searched_name = request.POST['name']
        consultant = connection.cursor().callfunc('search_consultants', [searched_name])


def delete_consult(request):
    if request.GET['deleteButton']:
        id = request.GET['id']
        connection.cursor().callproc('delete_consultants', [id])


def edit_consult(request):
    if request.GET['editButton']:
        searched_name = request.POST['name']
        connection.cursor().callproc('edit_consultants', [id, searched_name])


def edit_discount(request, discount_id):
    discount = Discounts.objects.get(id=discount_id)
    connection.cursor().callproc('edit_discount',[discount_id])
    discount.save()
