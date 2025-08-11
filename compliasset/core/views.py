from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views import generic
from .models import Business, ComplianceTask, Asset, Location
from .forms import SignUpForm, AssetForm
from django.utils import timezone
from django.urls import reverse_lazy

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

class AssetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'core/asset_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Filter locations to the current user's business
        kwargs['instance'] = Asset(location=self.get_locations().first())
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['location'].queryset = self.get_locations()
        return context

    def get_locations(self):
        return Location.objects.filter(business__owner=self.request.user)

@login_required
def dashboard(request):
    """
    Displays the main dashboard for a logged-in user, showing their
    overdue and upcoming compliance tasks.
    """
    context = {'has_business': False}
    try:
        business = Business.objects.select_related('owner').get(owner=request.user)
        today = timezone.now().date()
        
        tasks_base_query = ComplianceTask.objects.filter(
            asset__location__business=business,
            is_completed=False
        ).select_related('asset')

        overdue_tasks = tasks_base_query.filter(next_due_date__lt=today).order_by('next_due_date')
        upcoming_tasks = tasks_base_query.filter(next_due_date__gte=today).order_by('next_due_date')

        context = {
            'business': business,
            'upcoming_tasks': upcoming_tasks,
            'overdue_tasks': overdue_tasks,
            'has_business': True
        }
    except Business.DoesNotExist:
        pass
        
    return render(request, 'core/dashboard.html', context)
