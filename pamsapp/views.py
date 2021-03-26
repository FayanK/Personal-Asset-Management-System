from django.dispatch.dispatcher import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
from django.db.models import Q
import json

#accounts app
from accounts.models import CustomUser
from accounts.forms import CustomUserForm, EmployeeUserForm, CustomUserSuperForm
#pamsapp
from .models import Designation, Profile, Messsage
from .forms import ProfileForm, DesignationForm
#immovable app
from immovable_app.models import *
from immovable_app.forms import *
#movable app
from movable_app.models import *
from movable_app.forms import *

User = get_user_model()

# Create your views here.
@login_required
def index_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    notification = notification_func(request)
    context = {'user': request.user, 'profile':profile, 'notification':notification}
    return render(request, 'pamsapp/index.html', context)

def profile_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    notification = notification_func(request)
    context = {'user':request.user, 'profile':profile,'notification':notification}
    return render(request, 'pamsapp/profile.html', context)

def profile_show_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    #immovable
    lands = Land.objects.filter(user_id = request.user.id)
    buildings = Building.objects.filter(user_id = request.user.id)
    homesteads = Homestead.objects.filter(user_id = request.user.id)
    businessFirms = BusinessFirm.objects.filter(user_id = request.user.id)
    others = Other.objects.filter(user_id = request.user.id)
    ornaments = Ornaments.objects.filter(user_id = request.user.id)
    #movable
    ornaments = Ornaments.objects.filter(user_id = request.user.id)
    stocks = Stocks.objects.filter(user_id = request.user.id)
    shares = Share.objects.filter(user_id = request.user.id)
    insurences = Insurance.objects.filter(user_id = request.user.id)
    cash_or_bankvalues = Cash_or_bankvalue.objects.filter(user_id = request.user.id)
    vehicles = Vehicles.objects.filter(user_id = request.user.id)
    electronics = Electronics.objects.filter(user_id = request.user.id)
    others_m = Other_m.objects.filter(user_id = request.user.id)
    notification = notification_func(request)
    context = {
        'user':request.user, 
        'profile':profile,
        'lands': lands,
        'buildings':buildings,
        'homesteads':homesteads,
        'businessFirms':businessFirms,
        'others':others,
        'ornaments':ornaments,
        'stocks':stocks,
        'shares':shares,
        'insurences':insurences,
        'cash_or_bankvalues':cash_or_bankvalues,
        'vehicles':vehicles,
        'electronics':electronics,
        'others_m':others_m,
        'notification':notification}
    return render(request, 'pamsapp/profile_show.html', context)

@login_required
def profile_edit_view(request, user_id):
    user = get_object_or_404(CustomUser, pk = user_id)
    profile = Profile.objects.get(user_id = user.id)
    user_form = EmployeeUserForm(instance = user)
    profile_form = ProfileForm(instance = profile)
    if request.method == 'POST':
        user_form = EmployeeUserForm(request.POST, instance = user)
        profile_form = ProfileForm(request.POST,  request.FILES, instance = profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('pamsapp:profile'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'user_form': user_form, 
        'profile':profile, 
        'profile_form':profile_form,
        'notification':notification
        }
    return render(request, 'pamsapp/profile_edit.html', context)         

@login_required
def all_user_view(request):
    all_user = CustomUser.objects.all()
    profile = Profile.objects.get(user_id = request.user.id)
    search_value = request.GET.get('search_value')
    if search_value:
        all_user = all_user.filter(
            Q(email__icontains = search_value)|
            Q(name__icontains = search_value)|
            Q(phone_no = search_value)
        )
    notification = notification_func(request)
    context = {'users':all_user, 'profile':profile,'notification':notification}
    return render(request, 'pamsapp/all_user.html', context)


@login_required
def edit_user_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    user = request.user
    e_user = CustomUser.objects.get(pk = id)
    e_user_profile = Profile.objects.get(user_id = e_user.id)
    if user.user_type == '2':
        user_form = CustomUserForm(instance = e_user)  
        profile_form =  ProfileForm(instance = e_user_profile)
        if request.method == 'POST':
            user_form = CustomUserForm(request.POST, instance = user)
            profile_form = ProfileForm(request.POST,  request.FILES, instance = e_user_profile)
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('pamsapp:all-user'))  
    elif user.user_type == '1':
        user_form = CustomUserSuperForm(instance = e_user)  
        profile_form =  ProfileForm(instance = e_user_profile)
        if request.method == 'POST':
            user_form = CustomUserSuperForm(request.POST, instance = e_user)
            profile_form = ProfileForm(request.POST,  request.FILES, instance = e_user_profile)
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('pamsapp:all-user'))  
    notification = notification_func(request)
    context = {
        'user':request.user, 
        'e_user':e_user, 
        'profile':profile, 
        'user_form': user_form, 
        'profile_form':profile_form,
        'notification':notification}
    return render(request, 'pamsapp/edit_user.html', context)

def delete_user_view(request, id):
    user = CustomUser.objects.get(pk = id)
    user.delete()
    return HttpResponseRedirect(reverse('pamsapp:all-user'))    

@login_required
def all_designations_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            form = DesignationForm()
    else:
        form = DesignationForm()
    designations = Designation.objects.all()  
    notification = notification_func(request)      
    context = {
        'user':request.user,
        'profile':profile, 
        'designations': designations, 
        'form':form,
        'notification':notification
        }
    return render(request, 'pamsapp/all_designations.html', context)

@login_required
def designation_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)  
    if request.method == 'POST': 
        pi = Designation.objects.get(pk = id)
        form = DesignationForm(request.POST, instance = pi)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pamsapp:designations_list'))
    else:
        pi = Designation.objects.get(pk = id)
        form = DesignationForm(instance = pi)
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form,'notification':notification}
    return render(request, 'pamsapp/designation_edit.html', context)

@login_required
def delete_designation_view(request, id):
    if request.method == "POST":
        designation = Designation.objects.get(pk = id)
        designation.delete()
        return HttpResponseRedirect(reverse('pamsapp:designations_list'))  

#start immovable property views
@login_required    
def immovable_properties_view(request):
    profile = Profile.objects.get(user_id = request.user.id) 
    notification = notification_func(request)   
    context = {'user': request.user, 'profile':profile,'notification':notification}
    return render(request, 'immovable/immovable_property.html', context)

@login_required    
def land_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form = LandForm()
    # note_form_factory = modelformset_factory(NoteField, fields = ('notefield', ), extra = 10, form = LandNoteForm)
    if request.method == 'POST':
        form = LandForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(land = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:immovable-property'))
    # note_form = note_form_factory(queryset = NoteField.objects.none())
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form,'notification':notification}        
    return render(request, 'immovable/land_add.html', context)

@login_required   
def land_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Land.objects.get(pk = id)
    form = LandForm(instance = pi)
    if request.method == 'POST':
        form = LandForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField_im.objects.filter(land_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(land = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'land':pi,
        'notification':notification
        }
    return render(request, 'immovable/land_edit.html', context)

@login_required   
def view_land_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Land.objects.get(pk = id)
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'land':pi,
        'notification':notification
        }
    return render(request, 'immovable/view_land.html', context)

@login_required
def land_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Land.objects.get(pk = id)
    form = LandSuperForm(instance = pi)
    if request.method == 'POST':
        form = LandSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'land':pi,
        'notification':notification
        }
    return render(request, 'immovable/land_edit_admin.html', context)

@login_required
def land_delete_admin(request, land_id):
    land = Land.objects.get(pk = land_id)
    land.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list-pending')) 

@login_required    
def building_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form = BuildingForm()
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(building = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:immovable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form,'notification':notification} 
    return render(request, 'immovable/building_add.html', context)  

@login_required()
def building_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Building.objects.get(pk = id)
    form = BuildingForm(instance = pi)
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField_im.objects.filter(building_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(building = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form,'notification':notification}
    return render(request, 'immovable/building_edit.html', context)

@login_required   
def view_building_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Building.objects.get(pk = id)
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'building':pi,
        'notification':notification
        }
    return render(request, 'immovable/view_building.html', context)

@login_required
def building_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Building.objects.get(pk = id)
    form = BuildingSuperForm(instance = pi)
    if request.method == 'POST':
        form = BuildingSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'building':pi, 
        'notification':notification
        }
    return render(request, 'immovable/building_edit_admin.html', context)

@login_required
def building_delete_admin(request, building_id):
    building = Building.objects.get(pk = building_id)
    building.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list-pending')) 

@login_required    
def homestead_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form = HomesteadForm()
    if request.method == 'POST':
        form = HomesteadForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(homestead = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:immovable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification} 
    return render(request, 'immovable/homestead_add.html', context)

@login_required
def homestead_edit_view(request, id): 
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Homestead.objects.get(pk = id)
    form = HomesteadForm(instance = pi)
    if request.method == 'POST':
        form = HomesteadForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField_im.objects.filter(homestead_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(homestead = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'immovable/homestead_edit.html', context) 

@login_required   
def view_homestead_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Homestead.objects.get(pk = id)
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'homestead':pi,
        'notification':notification
        }
    return render(request, 'immovable/view_homestead.html', context)

@login_required
def homestead_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Homestead.objects.get(pk = id)
    form = HomesteadSuperForm(instance = pi)
    if request.method == 'POST':
        form = HomesteadSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'homestead':pi, 
        'notification':notification
        }
    return render(request, 'immovable/homestead_edit_admin.html', context)

@login_required
def homestead_delete_admin(request, homestead_id):
    homestead = Homestead.objects.get(pk = homestead_id)
    homestead.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list-pending')) 

@login_required    
def businessFirm_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form = BusinessFirmForm()
    if request.method == 'POST':
        form = BusinessFirmForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(businessFirm = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:immovable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification} 
    return render(request, 'immovable/businessfirm_add.html', context)   

@login_required
def businessFirm_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = BusinessFirm.objects.get(pk = id)
    form = BusinessFirmForm(instance = pi)
    if request.method == 'POST':
        form = BusinessFirmForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField_im.objects.filter(businessFirm_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(businessFirm = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'immovable/businessfirm_edit.html', context)

@login_required   
def view_businessfirm_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = BusinessFirm.objects.get(pk = id)
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'businessfirm':pi,
        'notification':notification
        }
    return render(request, 'immovable/view_businessfirm.html', context)

@login_required
def businessFirm_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = BusinessFirm.objects.get(pk = id)
    form = BusinessFirmSuperForm(instance = pi)
    if request.method == 'POST':
        form = BusinessFirmSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)        
    context = {
        'user':request.user,
        'profile':profile,
        'form':form, 
        'businessfirm':pi,
        'notification':notification
        }
    return render(request, 'immovable/businessfirm_edit_admin.html', context)

@login_required
def businessFirm_delete_admin(request, businessfirm_id):
    businessfirm = BusinessFirm.objects.get(pk = businessfirm_id)
    businessfirm.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list-pending')) 

@login_required    
def other_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =OtherForm()
    if request.method == 'POST':
        form = OtherForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(other = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'immovable/other_add.html', context)   

@login_required
def other_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Other.objects.get(pk = id)
    form = OtherForm(instance = pi)
    if request.method == 'POST':
        form = OtherForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField_im.objects.filter(other_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField_im(other = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'immovable/other_edit.html', context) 

@login_required   
def view_other_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Other.objects.get(pk = id)
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'other':pi,
        'notification':notification
        }
    return render(request, 'immovable/view_other.html', context)

@login_required
def other_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Other.objects.get(pk = id)
    form = OtherSuperForm(instance = pi)
    if request.method == 'POST':
        form = OtherSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'other':pi,
        'notification':notification
        }
    return render(request, 'immovable/other_edit_admin.html', context)

@login_required
def other_delete_admin(request, other_id):
    other = Other.objects.get(pk = other_id)
    other.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))     

# start movable property views
@login_required    
def movable_properties_view(request):
    profile = Profile.objects.get(user_id = request.user.id) 
    notification = notification_func(request)   
    context = {'user': request.user, 'profile':profile,'notification':notification}
    return render(request, 'movable/movable_property.html', context)

@login_required    
def ornaments_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =OrnamentsForm()
    if request.method == 'POST':
        form = OrnamentsForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(ornament = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/ornaments_add.html', context) 

@login_required
def ornaments_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Ornaments.objects.get(pk = id)
    form = OrnamentsForm(instance = pi)
    if request.method == 'POST':
        form = OrnamentsForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(ornament_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(ornament = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/ornaments_edit.html', context)

@login_required
def ornaments_edit_admin(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Ornaments.objects.get(pk = id)
    form = OrnamentsSuperForm(instance = pi)
    if request.method == 'POST':
        form = OrnamentsSuperForm(request.POST, request.FILES, instance = pi)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('pamsapp:assets-list-pending'))
    notification = notification_func(request)
    context = {
        'user':request.user,
        'profile':profile, 
        'form':form, 
        'ornament':pi,
        'notification':notification
        }
    return render(request, 'movable/ornaments_edit_admin.html', context)

@login_required
def ornaments_delete_admin(request, ornament_id):
    form = Ornaments.objects.get(pk = ornament_id)
    form.delete()
    return HttpResponseRedirect(reverse('pamsapp:assets-list')) 

@login_required    
def stocks_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =StocksForm()
    if request.method == 'POST':
        form = StocksForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(stock = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/stocks_add.html', context)

@login_required
def stocks_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Stocks.objects.get(pk = id)
    form = StocksForm(instance = pi)
    if request.method == 'POST':
        form = StocksForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(stock_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(stock = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/stocks_edit.html', context)

@login_required    
def shares_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =ShareForm()
    if request.method == 'POST':
        form = ShareForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(share = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/share_add.html', context)

@login_required
def shares_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Share.objects.get(pk = id)
    form = ShareForm(instance = pi)
    if request.method == 'POST':
        form = ShareForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(share_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(share = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/share_edit.html', context)

@login_required    
def insurances_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =InsuranceForm()
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(insurance = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/insurance_add.html', context)

@login_required
def insurances_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Insurance.objects.get(pk = id)
    form = InsuranceForm(instance = pi)
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(insurance_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(insurance = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/insurance_edit.html', context)

@login_required    
def cash_or_bankvalue_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =Cash_or_bankvalueForm()
    if request.method == 'POST':
        form = Cash_or_bankvalueForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(cash_or_bankvalue = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/cash_or_bankvalue_add.html', context)

@login_required
def cash_or_bankvalue_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Cash_or_bankvalue.objects.get(pk = id)
    form = Cash_or_bankvalueForm(instance = pi)
    if request.method == 'POST':
        form = Cash_or_bankvalueForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(cash_or_bankvalue_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(cash_or_bankvalue = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/cash_or_bankvalue_edit.html', context)

@login_required    
def vehicles_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =VehiclesForm()
    if request.method == 'POST':
        form = VehiclesForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(vehicles = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/vehicles_add.html', context)

@login_required
def vehicles_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Vehicles.objects.get(pk = id)
    form = VehiclesForm(instance = pi)
    if request.method == 'POST':
        form = VehiclesForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(vehicles_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(vehicles = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/vehicles_edit.html', context)

@login_required    
def electronics_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =ElectronicsForm()
    if request.method == 'POST':
        form = ElectronicsForm(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(electronic = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/electronics_add.html', context)

@login_required
def electronics_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Electronics.objects.get(pk = id)
    form = ElectronicsForm(instance = pi)
    if request.method == 'POST':
        form = ElectronicsForm(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(electronic_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(electronic = instance, notefield = file_path)
                    all_docs.save()
                    
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/electronics_edit.html', context)

@login_required    
def other_m_add_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    form =Other_m_Form()
    if request.method == 'POST':
        form = Other_m_Form(request.POST, request.FILES)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = request.user
            instance.save()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(other_m = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:movable-property'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/other_m_add.html', context)

@login_required
def other_m_edit_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    pi = Other_m.objects.get(pk = id)
    form = Other_m_Form(instance = pi)
    if request.method == 'POST':
        form = Other_m_Form(request.POST, request.FILES, instance = pi)
        docs = request.FILES.getlist("file[]")
        if form.is_valid():
            instance = form.save()
            note_obj = NoteField.objects.filter(other_m_id = pi.id)
            if note_obj.exists():
                note_obj.delete()
            for doc in docs:
                try:
                    fs = FileSystemStorage()
                    file_path = fs.save(doc.name, doc)
                    all_docs =NoteField(other_m = instance, notefield = file_path)
                    all_docs.save()
                except:
                    break
            return HttpResponseRedirect(reverse('pamsapp:show-properties'))
    notification = notification_func(request)
    context = {'user':request.user,'profile':profile, 'form':form, 'notification':notification}
    return render(request, 'movable/other_m_edit.html', context)

@login_required
def show_properties_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    #immovable
    lands = Land.objects.filter(user_id = request.user.id)
    buildings = Building.objects.filter(user_id = request.user.id)
    homesteads = Homestead.objects.filter(user_id = request.user.id)
    businessFirms = BusinessFirm.objects.filter(user_id = request.user.id)
    others = Other.objects.filter(user_id = request.user.id)
    ornaments = Ornaments.objects.filter(user_id = request.user.id)
    #movable
    ornaments = Ornaments.objects.filter(user_id = request.user.id)
    stocks = Stocks.objects.filter(user_id = request.user.id)
    shares = Share.objects.filter(user_id = request.user.id)
    insurences = Insurance.objects.filter(user_id = request.user.id)
    cash_or_bankvalues = Cash_or_bankvalue.objects.filter(user_id = request.user.id)
    vehicles = Vehicles.objects.filter(user_id = request.user.id)
    electronics = Electronics.objects.filter(user_id = request.user.id)
    others_m = Other_m.objects.filter(user_id = request.user.id)

    notification = notification_func(request) 
    context = {
        'user': request.user, 
        'profile':profile,
        'lands': lands,
        'buildings':buildings,
        'homesteads':homesteads,
        'businessFirms':businessFirms,
        'others':others,
        'ornaments':ornaments,
        'stocks':stocks,
        'shares':shares,
        'insurences':insurences,
        'cash_or_bankvalues':cash_or_bankvalues,
        'vehicles':vehicles,
        'electronics':electronics,
        'others_m':others_m,
        'notification':notification,
        }
    return render(request, 'pamsapp/show_properties.html', context)

@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user_id = request.user.id)

    totall_user = CustomUser.objects.all().count()
    unregistered_user = CustomUser.objects.filter(is_active = False).count()
    #immovable
    totall_lands = Land.objects.all().count()
    totall_buildings = Building.objects.all().count()
    totall_homesteads = Homestead.objects.all().count()
    totall_businessfirms = BusinessFirm.objects.all().count()
    totall_others = Other.objects.all().count()
    totall1 = totall_lands + totall_buildings + totall_homesteads + totall_businessfirms + totall_others
    #movable
    all_ornaments = Ornaments.objects.all().count()
    all_stocks = Stocks.objects.all().count()
    all_shares = Share.objects.all().count()
    all_insurences = Insurance.objects.all().count()
    all_cash_or_bankvalue = Cash_or_bankvalue.objects.all().count()
    all_vehicles = Vehicles.objects.all().count()
    all_electronics = Electronics.objects.all().count()
    all_others_m = Other_m.objects.all().count()
    totall2 = all_ornaments + all_stocks + all_shares + all_insurences + all_cash_or_bankvalue + all_vehicles + all_electronics +all_others_m

    totall = totall1+totall2
    #immovable
    confirm_lands = Land.objects.filter(is_confirm = True).count()
    confirm_buildings = Building.objects.filter(is_confirm = True).count()
    confirm_homesteads = Homestead.objects.filter(is_confirm = True).count()
    confirm_businessFirms = BusinessFirm.objects.filter(is_confirm = True).count()
    confirm_others = Other.objects.filter(is_confirm = True).count()
    totall_confirm1 = confirm_lands+confirm_buildings+confirm_homesteads+confirm_businessFirms+confirm_others
    #movable
    confirm_ornaments = Ornaments.objects.filter(is_confirm = True).count()
    confirm_stocks = Stocks.objects.filter(is_confirm = True).count()
    confirm_shares = Share.objects.filter(is_confirm = True).count()
    confirm_insurences = Insurance.objects.filter(is_confirm = True).count()
    confirm_cash_or_bankvalue = Cash_or_bankvalue.objects.filter(is_confirm = True).count()
    confirm_vehicles = Vehicles.objects.filter(is_confirm = True).count()
    confirm_electronics = Electronics.objects.filter(is_confirm = True).count()
    confirm_others_m = Other_m.objects.filter(is_confirm = True).count()
    totall_confirm2 = confirm_ornaments+confirm_stocks+confirm_shares+confirm_insurences+confirm_cash_or_bankvalue+confirm_vehicles+confirm_electronics+confirm_others_m

    totall_confirms = totall_confirm1+totall_confirm2

    totall_pendings = totall - totall_confirms
    notification = notification_func(request)    

    context = {
            'totall_user': totall_user,
            'unregistered_user': unregistered_user,
            'totall':totall,
            'totall_confirms':totall_confirms,
            'totall_pendings':totall_pendings,
            'profile':profile,
            'user': request.user,
            'notification':notification
            }
    return render(request, 'pamsapp/dashboard.html', context)

@login_required
def assets_list_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    search_value = request.GET.get('search_value')
    if search_value:
        #immovable
        all_lands = Land.objects.filter(user__email = search_value)
        all_buildings = Building.objects.filter(user__email = search_value)
        all_homesteads = Homestead.objects.filter(user__email = search_value)
        all_businessfirms = BusinessFirm.objects.filter(user__email = search_value)
        all_others = Other.objects.filter(user__email = search_value)
        #movable
        all_ornaments = Ornaments.objects.filter(user__email = search_value)
        all_stocks = Stocks.objects.filter(user__email = search_value)
        all_shares = Share.objects.filter(user__email = search_value)
        all_insurences = Insurance.objects.filter(user__email = search_value)
        all_cash_or_bankvalue = Cash_or_bankvalue.objects.filter(user__email = search_value)
        all_vehicles = Vehicles.objects.filter(user__email = search_value)
        all_electronics = Electronics.objects.filter(user__email = search_value)
        all_others_m = Other_m.objects.filter(user__email = search_value)
    else:
        #immovable
        all_lands = Land.objects.all()
        all_buildings = Building.objects.all()
        all_homesteads = Homestead.objects.all()
        all_businessfirms = BusinessFirm.objects.all()
        all_others = Other.objects.all()
        #movable
        all_ornaments = Ornaments.objects.all()
        all_stocks = Stocks.objects.all()
        all_shares = Share.objects.all()
        all_insurences = Insurance.objects.all()
        all_cash_or_bankvalue = Cash_or_bankvalue.objects.all()
        all_vehicles = Vehicles.objects.all()
        all_electronics = Electronics.objects.all()
        all_others_m = Other_m.objects.all()
    notification = notification_func(request)    

    context = {
        'user': request.user,
        'profile' : profile,
        #immovable
        'all_lands' : all_lands,
        'all_buildings' : all_buildings,
        'all_homesteads' : all_homesteads,
        'all_businessfirms' : all_businessfirms,
        'all_others' : all_others,
        #movable
        'all_ornaments':all_ornaments,
        'all_stocks':all_stocks,
        'all_shares':all_shares,
        'all_insurences':all_insurences,
        'all_cash_or_bankvalue':all_cash_or_bankvalue,
        'all_vehicles':all_vehicles,
        'all_electronics':all_electronics,
        'all_others_m':all_others_m,
        'notification':notification
    }
    return render(request, 'pamsapp/assets_list.html', context)

@login_required
def assets_list_pending_view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    #immovable
    all_lands = Land.objects.filter(is_confirm = False)
    all_buildings = Building.objects.filter(is_confirm = False)
    all_homesteads = Homestead.objects.filter(is_confirm = False)
    all_businessfirms = BusinessFirm.objects.filter(is_confirm = False)
    all_others = Other.objects.filter(is_confirm = False)
    #movable
    all_ornaments = Ornaments.objects.filter(is_confirm = False)
    all_stocks = Stocks.objects.filter(is_confirm = False)
    all_shares = Share.objects.filter(is_confirm = False)
    all_insurences = Insurance.objects.filter(is_confirm = False)
    all_cash_or_bankvalue = Cash_or_bankvalue.objects.filter(is_confirm = False)
    all_vehicles = Vehicles.objects.filter(is_confirm = False)
    all_electronics = Electronics.objects.filter(is_confirm = False)
    all_others_m = Other_m.objects.filter(is_confirm = False)

    notification = notification_func(request)
    message = 'pending Assets'
    context = {
        'profile' : profile,
        #immovable
        'all_lands' : all_lands,
        'all_buildings' : all_buildings,
        'all_homesteads' : all_homesteads,
        'all_businessfirms' : all_businessfirms,
        'all_others' : all_others,
        #movable
        'all_ornaments':all_ornaments,
        'all_stocks':all_stocks,
        'all_shares':all_shares,
        'all_insurences':all_insurences,
        'all_cash_or_bankvalue':all_cash_or_bankvalue,
        'all_vehicles':all_vehicles,
        'all_electronics':all_electronics,
        'all_others_m':all_others_m,

        'message': message,
        'notification':notification
    }
    return render(request, 'pamsapp/assets_list.html', context)

@login_required
def notification_func(request):
    #immovable
    count_pending_lands =  Land.objects.filter(is_confirm = False).count()
    count_pending_building =  Building.objects.filter(is_confirm = False).count()
    count_pending_homestead =  Homestead.objects.filter(is_confirm = False).count()
    count_pending_businessfirm =  BusinessFirm.objects.filter(is_confirm = False).count()
    count_pending_other =  Other.objects.filter(is_confirm = False).count()
    notification1 = count_pending_lands+count_pending_building+count_pending_homestead+count_pending_businessfirm+count_pending_other
    #movable
    count_pending_ornaments = Ornaments.objects.filter(is_confirm = False).count()
    count_pending_stocks = Stocks.objects.filter(is_confirm = False).count()
    count_pending_shares = Share.objects.filter(is_confirm = False).count()
    count_pending_insurences = Insurance.objects.filter(is_confirm = False).count()
    acount_pending_cash_or_bankvalue = Cash_or_bankvalue.objects.filter(is_confirm = False).count()
    acount_pending_vehicles = Vehicles.objects.filter(is_confirm = False).count()
    count_pending_electronics = Electronics.objects.filter(is_confirm = False).count()
    count_pending_others_m = Other_m.objects.filter(is_confirm = False).count()
    notification2 = count_pending_ornaments+count_pending_stocks+count_pending_shares+count_pending_insurences+acount_pending_cash_or_bankvalue+acount_pending_vehicles+count_pending_electronics+count_pending_others_m
    
    notification = notification1+notification2

    return notification

@login_required
def view_user_view(request, id):
    profile = Profile.objects.get(user_id = request.user.id)
    e_user = CustomUser.objects.get(pk = id)
    e_profile = Profile.objects.get(user = e_user)

    #immovable
    lands = Land.objects.filter(user = e_user)
    buildings = Building.objects.filter(user = e_user)
    homesteads = Homestead.objects.filter(user = e_user)
    businessFirms = BusinessFirm.objects.filter(user = e_user)
    others = Other.objects.filter(user = e_user)
    ornaments = Ornaments.objects.filter(user = e_user)
    #movable
    ornaments = Ornaments.objects.filter(user = e_user)
    stocks = Stocks.objects.filter(user = e_user)
    shares = Share.objects.filter(user = e_user)
    insurences = Insurance.objects.filter(user = e_user)
    cash_or_bankvalues = Cash_or_bankvalue.objects.filter(user = e_user)
    vehicles = Vehicles.objects.filter(user = e_user)
    electronics = Electronics.objects.filter(user = e_user)
    others_m = Other_m.objects.filter(user = e_user)

    notification = notification_func(request)
    context = {
        'user': request.user,
        'profile':profile,
        'e_user':e_user,
        'e_profile':e_profile,
        'notification':notification,
        #immovable
        'lands': lands,
        'buildings':buildings,
        'homesteads':homesteads,
        'businessFirms':businessFirms,
        'others':others,
        #movable
        'ornaments':ornaments,
        'stocks':stocks,
        'shares':shares,
        'insurences':insurences,
        'cash_or_bankvalues':cash_or_bankvalues,
        'vehicles':vehicles,
        'electronics':electronics,
        'others_m':others_m,

    }
    return render(request,'pamsapp/user_view.html', context)

@login_required
def view_user_immovable_view(request, user_id):
    profile = Profile.objects.get(user_id = request.user.id)
    e_user = CustomUser.objects.get(pk = user_id)
    e_profile = Profile.objects.get(user = e_user)

    #immovable
    lands = Land.objects.filter(user = e_user)
    buildings = Building.objects.filter(user = e_user)
    homesteads = Homestead.objects.filter(user = e_user)
    businessFirms = BusinessFirm.objects.filter(user = e_user)
    others = Other.objects.filter(user = e_user)
    
    notification = notification_func(request)
    context = {
        'user': request.user,
        'profile':profile,
        'e_user':e_user,
        'e_profile':e_profile,
        'notification':notification,
        'lands': lands,
        'buildings':buildings,
        'homesteads':homesteads,
        'businessFirms':businessFirms,
        'others':others,
    }
    return render(request,'pamsapp/user_immovable.html', context)

@login_required
def view_user_movable_view(request, user_id):
    profile = Profile.objects.get(user_id = request.user.id)
    e_user = CustomUser.objects.get(pk = user_id)
    e_profile = Profile.objects.get(user = e_user)

    #movable
    ornaments = Ornaments.objects.filter(user = e_user)
    stocks = Stocks.objects.filter(user = e_user)
    shares = Share.objects.filter(user = e_user)
    insurences = Insurance.objects.filter(user = e_user)
    cash_or_bankvalues = Cash_or_bankvalue.objects.filter(user = e_user)
    vehicles = Vehicles.objects.filter(user = e_user)
    electronics = Electronics.objects.filter(user = e_user)
    others_m = Other_m.objects.filter(user = e_user)

    notification = notification_func(request)
    context = {
        'user': request.user,
        'profile':profile,
        'e_user':e_user,
        'e_profile':e_profile,
        'notification':notification,
        #movable
        'ornaments':ornaments,
        'stocks':stocks,
        'shares':shares,
        'insurences':insurences,
        'cash_or_bankvalues':cash_or_bankvalues,
        'vehicles':vehicles,
        'electronics':electronics,
        'others_m':others_m,

    }
    return render(request,'pamsapp/user_movable.html', context)

@login_required
def user_all_assets_view(request, user_id):
    profile = Profile.objects.get(user_id = request.user.id)
    e_user = CustomUser.objects.get(pk = user_id)
    e_profile = Profile.objects.get(user = e_user)

    #immovable
    lands = Land.objects.filter(user = e_user)
    buildings = Building.objects.filter(user = e_user)
    homesteads = Homestead.objects.filter(user = e_user)
    businessFirms = BusinessFirm.objects.filter(user = e_user)
    others = Other.objects.filter(user = e_user)
    ornaments = Ornaments.objects.filter(user = e_user)
    #movable
    ornaments = Ornaments.objects.filter(user = e_user)
    stocks = Stocks.objects.filter(user = e_user)
    shares = Share.objects.filter(user = e_user)
    insurences = Insurance.objects.filter(user = e_user)
    cash_or_bankvalues = Cash_or_bankvalue.objects.filter(user = e_user)
    vehicles = Vehicles.objects.filter(user = e_user)
    electronics = Electronics.objects.filter(user = e_user)
    others_m = Other_m.objects.filter(user = e_user)

    notification = notification_func(request)
    context = {
        'user': request.user,
        'profile':profile,
        'e_user':e_user,
        'e_profile':e_profile,
        'notification':notification,
        #immovable
        'lands': lands,
        'buildings':buildings,
        'homesteads':homesteads,
        'businessFirms':businessFirms,
        'others':others,
        #movable
        'ornaments':ornaments,
        'stocks':stocks,
        'shares':shares,
        'insurences':insurences,
        'cash_or_bankvalues':cash_or_bankvalues,
        'vehicles':vehicles,
        'electronics':electronics,
        'others_m':others_m,

    }
    return render(request,'pamsapp/user_all_assets.html', context)

# @login_required
# def chatroom_view(request, pk:int):
#     profile = Profile.objects.get(user_id = request.user.id)
#     other_user = get_object_or_404(CustomUser, pk = pk)
#     messages = Messsage.objects.filter(
#         Q(receiver = request.user , sender = other_user)
#     )
#     messages.update(seen = True)
#     messages = messages | Messsage.objects.filter(Q(receiver = other_user, sender = request.user))
#     notification = notification_func(request)
#     context = {
#         'user': request.user,
#         'profile':profile,
#         'other_user': other_user,
#         'messages':messages,
#         'notification':notification,
#     }
#     return render(request, 'pamsapp/chatroom.html', context)

# @login_required
# def ajax_load_message(request, pk):
#     other_user = get_object_or_404(CustomUser, pk=pk)
#     messages = Messsage.objects.filter(seen = False).filter(
#         Q(receiver = request.user , sender = other_user)
#     )
#     message_list = [{
#         'sender': message.sender.email,
#         'message': message.message,
#         'sent': message.sender == request.user
#     }for message in messages]
#     messages.update(seen = True)
#     if request.method == "POST":
#         message = json.loads(request.body)
#         m = Messsage.objects.create(receiver= other_user, sender = request.user, message=message)
#         message_list.append({
#             'sender': request.user.email,
#             'message': m.message,
#             'sent' : True
#         })
#     return JsonResponse(message_list, safe=False)


@login_required
def chatroom(request, pk:int):
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Messsage.objects.filter(
        Q(receiver=request.user, sender=other_user)
    )
    messages.update(seen=True)
    messages = messages | Messsage.objects.filter(Q(receiver=other_user, sender=request.user) )
    return render(request, "pamsapp/chatroom.html", {"other_user": other_user, "messages": messages})


@login_required
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(CustomUser, pk=pk)
    # messages = Messsage.objects.filter(seen=False).filter(
    #     Q(receiver_id=request.user.id, sender_id=other_user.id)
    # )
    messages = Messsage.objects.filter(receiver=request.user, sender=other_user)

    message_list = [{
        "sender": message.sender.email,
        "message": message.message,
        "sent": message.sender == request.user
    } for message in messages]
    messages.update(seen=True)
    print('This is massage')
    print(messages)
    if request.method == "POST":
        message = json.loads(request.body)
        m = Messsage.objects.create(receiver=other_user, sender=request.user, message=message)
        message_list.append({
            "sender": request.user.email,
            "message": m.message,
            "sent": True,
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)









