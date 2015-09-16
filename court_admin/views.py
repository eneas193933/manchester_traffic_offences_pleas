from django.views.generic import TemplateView
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator

from apps.plea.models import Court, UsageStats


class UsageStatsView(TemplateView):
    template_name = "usage_data.html"

    def _get_formset(self, court, *args, **kwargs):
        usage_formset = modelformset_factory(
            UsageStats,
            fields=("postal_requisitions", "postal_responses",),
            extra=0)

        form_kwargs = {
            "initial": 0,
            "queryset": UsageStats.objects.filter(court=court)
        }

        form_kwargs.update(kwargs)

        return usage_formset(*args, **form_kwargs)

    def get_selected_court(self, court_id=None):
        """
        If superuser, then the user can access any court.

        If admin, then they are restricted to the court on their profile

        """

        #raise HttpResponseForbidden

        if not court_id:
            return Court.objects.all().first()
        else:
            return Court.objects.get(pk=court_id)

    def get(self, request, *args, **kwargs):

        # the following would happen via a cron task to keep the dashboard updated
        # with online data
        court = self.get_selected_court(kwargs.get("court_id", None))
        UsageStats.objects.calculate_weekly_stats(court)

        kwargs["formset"] = self._get_formset(court)
        kwargs["selected_court"] = court

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        court = self.get_selected_court(kwargs.get("court_id", None))

        formset = self._get_formset(court, request.POST)

        if formset.is_valid():
            formset.save()
            messages.info(request, "Court statistics have been updated.")

        kwargs["formset"] = formset
        kwargs["selected_court"] = court

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsageStatsView, self).get_context_data(**kwargs)

        context["courts"] = Court.objects.all()

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UsageStatsView, self).dispatch(*args, **kwargs)

