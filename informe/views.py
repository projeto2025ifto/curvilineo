# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Link, Banner
from .forms import LinkForm, BannerForm

# Informes page view
def informes(request):
    banners = Banner.objects.all()
    links = Link.objects.all()
    return render(request, 'informes.html', {'banners': banners, 'links': links})

#------------------------------------------------------------
# Link views
def link_list(request):
    links = Link.objects.all().order_by('-created_at')
    return render(request, 'links/link_list.html', {'links': links})

def link_create(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = LinkForm()
    return render(request, 'links/link_form.html', {'form': form})

def link_detail(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    return render(request, 'link_detail.html', {'link': link})

def link_update(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    if request.method == "POST":
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = LinkForm(instance=link)
    return render(request, 'links/link_form.html', {'form': form})

def link_delete(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    if request.method == "POST":
        link.delete()
        return redirect('informes')
    return render(request, 'links/link_confirm_delete.html', {'link': link})

#------------------------------------------------------------
# Banner views
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'banners/banner_list.html', {'banners': banners})

def banner_create(request):
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = BannerForm()
    return render(request, 'banners/banner_form.html', {'form': form})

def banner_update(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('informes')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'banners/banner_form.html', {'form': form})

def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        banner.delete()
        return redirect('informes')
    return render(request, 'banners/banner_confirm_delete.html', {'banner': banner})
