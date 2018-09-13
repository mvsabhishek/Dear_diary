from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Diary, User
from drdiary.forms import SignUpForm, EntriesForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class index_view(LoginRequiredMixin ,ListView):
    model = Diary
    paginate_by = 10
    template_name = 'home.html'

    def get_queryset(self):
        try:
            term = self.request.GET.get('term',)
            created =self.request.GET.get('dc',)
            from_date = self.request.GET.get('dc1',)
            to_date = self.request.GET.get('dc2',)

        except KeyError:
            term = None
            from_date = None
            to_date = None
            created = None

        if term and not(from_date or to_date or created):
            entry_list = Diary.objects.all().filter(
                title__icontains=term,
                user=self.request.user.id
            ).order_by('-created_at')

        elif created and term and not (from_date or to_date):
            console.log(datetime.strptime(created, "%Y-%m-%d").date())
            entry_list = Diary.objects.all().filter(
                title__icontains=term,
                user=self.request.user.id,
                created_at = created
            ).order_by('-created_at')

        elif created and not (term or from_date or to_date) :
             entry_list = Diary.objects.all().filter(
                title__icontains=term,
                user=self.request.user.id,
                created_at = created
            ).order_by('-created_at')

        elif term and from_date and to_date:
            entry_list = Diary.objects.all().filter(
                title__icontains=term,
                user=self.request.user.id,
                created_at__range=(from_date, to_date)
            ).order_by('-created_at')

        elif not term and (from_date and to_date):
            entry_list = Diary.objects.all().filter(
                user=self.request.user.id,
                created_at__range=(from_date, to_date)
            ).order_by('-created_at')

        else:
            entry_list = Diary.objects.all().filter(user=self.request.user.id).order_by('-created_at')
        return entry_list

    def dispatch(self, *args, **kwargs):
        return super(index_view, self).dispatch(*args, **kwargs)


class signup(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        message = render_to_string('active_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your Dear Diary account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return super(signup, self).form_valid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'email_conf.html',{'conf_message':'Thank you for the email confirmation. Please login. :)'})
    else:
        return render(request, 'email_conf.html',{'conf_message':'Sorry, activation link is invalid!'})

class new_entry(LoginRequiredMixin, CreateView):
    form_class = EntriesForm
    template_name='new.html'
    login_url = '/'
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        entry = form.save(commit=False)
        temp = entry.title
        entry.title = temp.title()
        entry.created_at = timezone.now()
        entry.user = self.request.user
        entry.save()
        return super(new_entry, self).form_valid(form)


class delete_entry(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Diary
    login_url = '/'
    success_url = reverse_lazy('index_view')

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            messages.success(self.request,'Successfully Deleted!')
            return redirect('/')
        else:
            messages.error(self.request, 'Deletion Unsuccessful. You cannot delete what you do not own. :)')
            return redirect('/')



class view_entry(LoginRequiredMixin, DetailView):
    model = Diary
    template_name = 'entry.html'
    login_url = '/'

    def get_object(self, queryset=None):
        obj = super(view_entry, self).get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj


class Update(LoginRequiredMixin, UpdateView):
    model = Diary
    form_class = EntriesForm
    template_name = 'new.html'
    login_url = '/'
    success_url = '/'

def error_404(request):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)