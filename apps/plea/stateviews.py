from django.utils.decorators import method_decorator
from django.template import RequestContext, loader
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect

from form_states import PleaStates

@never_cache
def state_view(request, state=None, index=None):
    # Run forwards through journey and if the best state isn't the one
    # we're currently on then redirect to it.
    data = request.session.get("state_data", {})
    sm = PleaStates(state_data=data)
    sm.init(state, index=index)

    if sm.state.name != state:
        return HttpResponseRedirect(sm.state.get_url())

    if request.method == "POST":
        data = sm.move(request.POST)
        if data["valid"] == True:
            request.session["state_data"] = sm.state_data
            return HttpResponseRedirect(sm.state.get_url())
        else:
            form = sm.state.form
    else:
        sm.state.load()
        form = sm.state.form

    data["form"] = form
    ctxt = RequestContext(request, data)
    template = loader.get_template(sm.state.template)
    return HttpResponse(template.render(ctxt))