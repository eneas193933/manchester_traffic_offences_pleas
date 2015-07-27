from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from form_states import PleaStates

@never_cache
def state_view(request, stage=None):
    if stage is None:
            stage = "case_stage"

    data = request.session.get("state_data", {})
    plea = PleaStates(state_data=data)
    data["form"] = plea.state.form
    ctxt = RequestContext(request, data)
    template = loader.get_template(plea.state.template)

    return HttpResponse(template.render(ctxt))

