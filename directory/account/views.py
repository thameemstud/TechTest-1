import csv, io
from zipfile import ZipFile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.forms import ValidationError
from django.contrib import messages
from django.core.files import File

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .utils import EmailValidatorMixin
from .models import Teacher,Subject
from .forms import BulkUploadForm



class Home(ListView):
  model = Teacher
  template_name = 'directory/home.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["filter_lastname"] = self.request.GET.get('filter_lastname', "")
    context["filter_subject"] = self.request.GET.get('filter_subject', "")
    return context

  def get_queryset(self):
    qs = self.model.objects.all()
    filter_lastname = self.request.GET.get('filter_lastname', "")
    filter_subject = self.request.GET.get('filter_subject', "")
    if filter_lastname:
        qs = qs.filter(lastName__istartswith=filter_lastname.strip()[:2])
    if filter_subject:
        qs = qs.filter(subject__title__istartswith=filter_subject.strip()[:2])
    
    return qs

class TeacherDetailView(DetailView):
  model = Teacher
  template_name = 'directory/detail.html'



class TeacherCreateView(EmailValidatorMixin, LoginRequiredMixin, View):

    form = BulkUploadForm
    model = Teacher
    template_name = "directory/create.html"
    subjet_count = 5
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
            context = {'form': self.form()}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            
            try:
                csv_file = form.cleaned_data["csv_file"]
                file_obj = csv_file.read().decode('utf-8')
                csv_data = csv.reader(io.StringIO(file_obj), delimiter=',')

                zip_file = form.cleaned_data["zip_file"]
                zipfile_obj = ZipFile(zip_file, 'r')
                
        
                columns = next(csv_data)
                for row in csv_data:
                    email = row[3].strip()
                    
                    if self.validate_email(email=email):
                        if not self.model.objects.filter(
                                            email__iexact=email
                                        ).exists():
                            teacher_obj = self.model()
                            teacher_obj.firstName = row[0]
                            teacher_obj.lastName = row[1]
                            teacher_obj.email = email
                            teacher_obj.save()
                            subject_list = row[6].strip().split(",")
                            subject_list = [item.strip().upper() for item  in subject_list if item.strip()]
                            teacher_subject_list = subject_list[:self.subjet_count]
                            for subj in teacher_subject_list:
                                sobj, created = Subject.objects.get_or_create(
                                                        title=subj
                                                    )
                                teacher_obj.subject.add(sobj)
                            pic_name = row[4].strip()
                            if pic_name in zipfile_obj.namelist():
                                file_obj = File(zipfile_obj.open(pic_name, 'r'))
                                teacher_obj.profilePicture.save(pic_name, file_obj, save=True)
                
                return HttpResponseRedirect(self.get_success_url())    
            
            except Exception as e:
                messages.error(request, e)
            
            
            
        return render(request, self.template_name, {'form': form})


    def get_success_url(self):
        return reverse_lazy("dir-home")
