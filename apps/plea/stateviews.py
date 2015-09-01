from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from form_states import PleaStates

@never_cache
def state_view(request, stage=None):
    if stage is None:
            stage = "case"

    # Run forwards through journey and if the best state isn't the one
    # we're currently on then redirect to it.
    data = request.session.get("state_data", {})
    plea = PleaStates(state_data=data)
    plea.move_to_best()

    if plea.state.name != stage:
        return HttpResponseRedirect(reverse("state_form_step", kwargs={"stage": plea.state.name}))

    if request.method == "POST":
        if plea.move_to_next(request.POST):
            return HttpResponseRedirect('/')

    data["form"] = plea.state.form
    ctxt = RequestContext(request, data)
    template = loader.get_template(plea.state.template)
    return HttpResponse(template.render(ctxt))

