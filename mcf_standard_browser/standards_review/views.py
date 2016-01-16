from django.shortcuts import render
from models import Standard
# Create your views here.

def home_page(request):
    return render(request,'mcf_standards_browse/home_page.html',)

def StandardAdduct_detail(request,dataset_pk, standard_pk, adduct_pk):
    print 'standard - yo'
    print dataset_pk, standard_pk, adduct_pk
    return True

def Dataset_detail(request):
    print 'dataset detail - yo'
    return True

def Dataset_list(request):
    print 'dataset - yo'
    return True


def MCFStandard_list(request):
    standards = Standard.objects.all()
    return  render(request,'mcf_standards_browse/mcf_standard_list.html',{'standards':standards})

def MCFStandard_detail(request):
    return True

def MCFStandard_add(request):
    return render(request,'mcf_standards_browse/mcf_standard_add.html')