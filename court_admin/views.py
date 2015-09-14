from django.views.generic import TemplateView
from django.forms.models import modelformset_factory
from django.contrib import messages

from apps.plea.models import Court, UsageStats


class UsageStatsView(TemplateView):
    template_name = "usage_data.html"

    def _get_formset(self):
        return modelformset_factory(UsageStats,
                                    fields=("postal_requisitions", "postal_responses",),
                                    extra=0)

    def get_selected_court(self, request):
        """
        If superuser, then the user can access any court.

        If admin, then they are restricted to the court on their profile

        """

        return Court.objects.all()[0]

    def get(self, request, *args, **kwargs):

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        formset = self._get_formset()(request.POST, initial=0)

        if formset.is_valid():
            formset.save()
            messages.info(request, "Court statistics have been updated.")

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsageStatsView, self).get_context_data(**kwargs)

        context["selected_court"] = Court.objects.all()[0]
        context["formset"] = self._get_formset()
        context["courts"] = Court.objects.all()

        return context

