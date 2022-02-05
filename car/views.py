from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q
from .models import Car, Brand, Repair, Employee
from .forms import AddCarForm, BrandForm, RepairForm
import datetime

def employee_repair_view(request, pk):

    employee = get_object_or_404(Employee, id=pk)
    context = {'employee': employee}
    if request.method == "POST":
        start_date = request.POST.get('from_date')
        end_date = request.POST.get('to_date') 
        list_repair = Repair.objects.filter(
            Q(workman__id=employee.id) &
            Q(created__range=(start_date, end_date)) 
            )
        context['list_repair'] = list_repair
        context['start_date'] = start_date
        context['end_date'] = end_date
        return render(request, 'car/employee_repair.html', context)
    else:
        list_repair = employee.repair_set.all()
        context['list_repair'] = list_repair 
        return render(request, 'car/employee_repair.html', context)



def list_repair(request):

    context = {}
    def get_n_last_month(month=1):
        today = datetime.datetime.now()
        first_day_month = today.replace(day=1)
        circle = list(range(0, month))
        for _ in circle:
            result = first_day_month - datetime.timedelta(days=1)
            first_day_month = result.replace(day=1)
        return result
    
    if request.method == "POST":
        start_date = request.POST.get('from_date')
        end_date = request.POST.get('to_date')
        repair = Repair.objects.filter(created__range=(start_date, end_date))
        context['repair_from_date'] = repair
        context['start_date'] = start_date
        context['end_date'] = end_date
        return render(request, 'car/list_repair.html', context)

    repairs = Repair.objects.all()

    context['repairs'] = repairs

    return render(request, 'car/list_repair.html', context)


def edit_repair(request, pk):
    rep_obj = Repair.objects.get(id=pk)
    forms = RepairForm(request.POST or None, instance=rep_obj) 
    if forms.is_valid():
        forms.save()
        return redirect('detail_car', rep_obj.car.id)
    context = {
            'obj': rep_obj, 
            'forms': forms,
            }
    return render(request, 'car/edit_repair.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    

    cars = Car.objects.filter(
            Q(reg_num__icontains=q) |
            Q(vin_num__icontains=q) |
            Q(brand__name__icontains=q)
            )

    objects_progress = Repair.progress.all()
    context = {'list_car': cars}

    brands = Brand.objects.all()
    context['brands'] = brands

    if objects_progress:
        context['objects_progress'] = objects_progress
    else:
        context['msg'] = 'Not car repair in progess'
    if not cars:
        context['msg_car_search'] = f'Car whit "{q}" is not fount!'

    return render(request, 'car/home.html', context)

def add_car(request):
    if request.method == 'POST':
        car_form = AddCarForm(data=request.POST)
        if car_form.is_valid():
            car_form.save()
            return redirect('list_car')

    else:
        car_form = AddCarForm()
    return render(request, 'car/add_car.html', {'form': car_form})

def add_brand(request):
    if request.method == 'POST':
        brand_form = BrandForm(data=request.POST)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('add_car')
    else:
        brand_form = BrandForm()
    return render(request, 'car/add_brand.html', {'form': brand_form})

def list_car(request):
    objects_list = Car.objects.all()
    return render(request, 'car/list_car.html', {'obj': objects_list})

def detail_car(request, pk):
    car_obj = get_object_or_404(Car, id=pk)
    rep_car = car_obj.repair.all()
    context = {
            'obj': car_obj,
            'repair': rep_car,
            }
    if request.method == "GET":
        if request.GET.get('add_repair', ):
            context['add_repair'] = True
        if request.GET.get('edit_repair'):
            context['edit_repair'] = True

    new_repair = None
    if request.method == "POST":
        repair_form = RepairForm(data=request.POST)
        if repair_form.is_valid():
            new_repair = repair_form.save(commit=False)
            new_repair.car = car_obj
            new_repair.created = request.POST["created"]
            new_repair.save()
            redirect('detail_car', car_obj.id)
    else:
        repair_form = RepairForm()

    context['repair_form'] = repair_form

    return render(request, 'car/detail_car.html', context)

