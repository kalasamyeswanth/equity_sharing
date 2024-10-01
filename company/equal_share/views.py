from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Startup, Investor, Investment
from .forms import InvestmentForm


# Create your views here.
class StartupListView(ListView):
    model = Startup
    template_name = 'startup_list.html'
    context_object_name = 'startups'
    paginate_by = 10  # You can paginate if there are many startups


class StartupDetailView(DetailView):
    model = Startup
    template_name = 'startup_detail.html'
    context_object_name = 'startup'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_form'] = InvestmentForm()
        return context


@login_required
def invest_in_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)

    if not hasattr(request.user, 'investor'):
        messages.error(request, "Only investors can make investments.")
        return redirect('startup_detail', pk=startup.pk)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.startup = startup
            investment.investor = request.user.investor

            total_equity_invested = sum(i.equity_taken for i in Investment.objects.filter(startup=startup))
            if total_equity_invested + investment.equity_taken > startup.equity_offered:
                messages.error(request, "Not enough equity remaining for this investment.")
                return redirect('startup_detail', pk=startup.pk)

            investment.save()
            messages.success(request, "Investment successful!")
            return redirect('startup_detail', pk=startup.pk)
    else:
        form = InvestmentForm()

    return render(request, 'invest_in_startup.html', {'form': form, 'startup': startup})



@login_required
def my_investments(request):
    try:
        investor = Investor.objects.get(user=request.user)
        investments = investor.investment_set.all()
    except Investor.DoesNotExist:
        investments = None

    context = {
        'investments': investments,
    }
    return render(request, 'my_investments.html', context)