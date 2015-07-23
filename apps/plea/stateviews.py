from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, FormView

from form_states import PleaStates


class StateViews(TemplateView):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(StateViews, self).dispatch(*args, **kwargs)

    def get(self, request, stage=None):
        if not stage:
            stage = "case_stage"

        data = request.session["state_data"]

        p = PleaStates(state_data=data)

        p.render()
