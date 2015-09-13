from django.shortcuts import render
from django.views.generic import TemplateView
from django.forms.models import modelformset_factory

from apps.plea.models import Court, UsageStats


class UsageStatsView(TemplateView):
    template_name = "usage_data.html"

    def _get_formset(self):
        return modelformset_factory(UsageStats, exclude=("start_date", "court",))

    def get(self, request, *args, **kwargs):

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        return super(UsageStatsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsageStatsView, self).get_context_data(**kwargs)

        context['formset'] = self._get_formset()
        context['courts'] = Court.objects.all()

        return context

