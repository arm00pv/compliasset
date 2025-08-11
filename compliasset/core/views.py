from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views import generic
from .models import Business, ComplianceTask
from .forms import SignUpForm
from django.utils import timezone

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    
    def get_success_url(self):
        return redirect('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

@login_required
def dashboard(request):
    """
    Displays the main dashboard for a logged-in user, showing their
    overdue and upcoming compliance tasks.
    """
    context = {'has_business': False}
    try:
        business = Business.objects.get(owner=request.user)
        tasks = ComplianceTask.objects.filter(
            asset__location__business=business, 
            is_completed=False
        ).order_by('next_due_date')
        
        today = timezone.now().date()
        
        overdue_tasks = tasks.filter(next_due_date__lt=today)
        upcoming_tasks = tasks.filter(next_due_date__gte=today)

        context = {
            'business': business,
            'upcoming_tasks': upcoming_tasks,
            'overdue_tasks': overdue_tasks,
            'has_business': True
        }
    except Business.DoesNotExist:
        pass
        
    return render(request, 'core/dashboard.html', context)
