from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Permission

from apps.plea.models import Court, UsageStats
from court_admin.decorators import court_staff_user_required, court_admin_user_required
from court_admin.forms import InviteUserForm, EmailNotAvailable, RegistrationForm, PersonalDetailsForm


class PersonalDetailsView(FormView):
    template_name = "settings/personal_details.html"
    form_class = PersonalDetailsForm

    @method_decorator(court_staff_user_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonalDetailsView, self).dispatch(*args, **kwargs)


class DashboardView(TemplateView):
    template_name = "dashboard/overview.html"

    def _get_formset(self, court, *args, **kwargs):
        usage_formset = modelformset_factory(
            UsageStats,
            fields=("postal_requisitions", "postal_guilty_pleas", "postal_not_guilty_pleas"),
            extra=0)

        form_kwargs = {
            "initial": 0,
            "queryset": UsageStats.objects.filter(court=court)
        }

        form_kwargs.update(kwargs)

        return usage_formset(*args, **form_kwargs)

    def _get_totals(self, court):
        stats = UsageStats.objects.filter(court=court)
        totals = stats.aggregate(Sum("postal_responses"),
                                 Sum("postal_guilty_pleas"),
                                 Sum("postal_not_guilty_pleas"),
                                 Sum("online_submissions"),
                                 Sum("online_guilty_pleas"),
                                 Sum("online_not_guilty_pleas"))

        data = {"by_post": {"submissions": totals["postal_responses__sum"] or 0,
                            "guilty": totals["postal_guilty_pleas__sum"] or 0,
                            "not_guilty": totals["postal_not_guilty_pleas__sum"] or 0},
                "online": {"submissions": totals["online_submissions__sum"] or 0,
                           "guilty": totals["online_guilty_pleas__sum"] or 0,
                           "not_guilty": totals["online_not_guilty_pleas__sum"] or 0}}

        data.update({"totals": {"submissions": data["online"]["submissions"] + data["by_post"]["submissions"],
                                "guilty": data["online"]["guilty"] + data["by_post"]["guilty"],
                                "not_guilty": data["online"]["not_guilty"] + data["by_post"]["not_guilty"]}})

        return data

    def get_selected_court(self, court_id=None):

        user = self.request.user

        user_court, selected_court = None, None

        is_court_admin = user.has_perm("plea.court_staff_admin") or user.is_superuser

        try:
            user_court = user.courtadminprofile.court
        except AttributeError:
            if not is_court_admin:
                raise PermissionDenied

        if court_id:
            selected_court = Court.objects.get(pk=court_id)

        if is_court_admin:
            return selected_court or user_court or Court.objects.all().first()
        else:
            return user_court

    def get(self, request, *args, **kwargs):

        # the following would happen via a cron task to keep the dashboard updated
        # with online data
        court = self.get_selected_court(kwargs.get("court_id", None))
        UsageStats.objects.calculate_weekly_stats(court)

        kwargs["formset"] = self._get_formset(court)
        kwargs["selected_court"] = court
        kwargs["totals"] = self._get_totals(court)

        return super(DashboardView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        court = self.get_selected_court(kwargs.get("court_id", None))

        formset = self._get_formset(court, request.POST)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Court statistics have been updated.")

        kwargs["formset"] = formset
        kwargs["selected_court"] = court
        kwargs["totals"] = self._get_totals(court)

        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context["courts"] = Court.objects.all()

        return context

    @method_decorator(court_staff_user_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)


class InviteUserView(FormView):
    template_name = "users/invite_user.html"
    form_class = InviteUserForm

    def form_valid(self, form):

        try:
            user = form.create_user_from_form(form)
        except EmailNotAvailable:
            messages.error(self.request, "A user with that email already exists.")

            return self.render_to_response(self.get_context_data(form=form))

        else:

            context = {
                "host": self.request.get_host(),
                "use_https": self.request.is_secure()
            }
            form.send_invite_email(user, **context)
            messages.success(self.request, "An invitation has been sent to {}".format(user.email))

        self.success_url = self.request.path

        return super(InviteUserView, self).form_valid(form)

    @method_decorator(court_admin_user_required)
    def dispatch(self, *args, **kwargs):
        return super(InviteUserView, self).dispatch(*args, **kwargs)


class RegisterView(TemplateView):
    template_name = "profile/register.html"

    def get(self, request, *args, **kwargs):

        uid64 = kwargs["uidb64"]
        token = kwargs["token"]

        valid_token, user = RegistrationForm.verify_token(uid64, token)

        if not valid_token:
            messages.error(request, "This registration request is invalid. "
                                    "It may have expired or it may have already been used.")

            return super(RegisterView, self).get(request, *args, **kwargs)

        context = {
            "user": user,
            "form": RegistrationForm(initial={"first_name": user.first_name, "last_name": user.last_name})
        }

        kwargs.update(context)

        return super(RegisterView, self).get(request, *args, **kwargs)

    #@method_decorator(sensitive_post_parameters)
    def post(self, request, *args, **kwargs):

        uid64 = kwargs["uidb64"]
        token = kwargs["token"]

        valid_token, user = RegistrationForm.verify_token(uid64, token)

        if not valid_token:
            messages.error(request, "This registration request is invalid. "
                                    "It may have expired or it may have already been used.")

            return super(RegisterView, self).get(request, *args, **kwargs)

        form = RegistrationForm(request.POST)

        kwargs["user"] = user
        kwargs["form"] = form

        if form.is_valid():
            form.activate_user(user)

            return redirect("register_done")
        else:
            return super(RegisterView, self).get(request, *args, **kwargs)


class UsersView(TemplateView):
    template_name = "users/users.html"

    def _get_users(self):

        court_staff_perm = Permission.objects.get(codename="court_staff_user")

        return User.objects.filter(user_permissions=court_staff_perm)

    def _can_modify_user(self, user):

        return self.request.user.has_perm("plea.court_staff_admin") and \
               not user.is_superuser and \
               not user.is_staff #and \
               #user.has_perm("plea.court_staff_user")

    def get(self, request, *args, **kwargs):

        kwargs["users"] = self._get_users()

        return super(UsersView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        kwargs["users"] = self._get_users()

        action = request.POST.get("action", None)
        id = request.POST.get("id", None)

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return redirect(request.path)

        if action == "resend":
            if self._can_modify_user(user): # TODO: Check the user is an invite - need to add an user.is_invite() method
                context = {
                    "host": self.request.get_host(),
                    "use_https": self.request.is_secure()
                }
                InviteUserForm.send_invite_email(user, **context)
                messages.info(request, "Invite resent")

            return redirect(request.path)

        elif action == "delete":
            if self._can_modify_user(user):
                user.delete()
                messages.info(request, "Delete")

            return redirect(request.path)

        return super(UsersView, self).get(request, *args, **kwargs)

    @method_decorator(court_admin_user_required)
    def dispatch(self, *args, **kwargs):
        return super(UsersView, self).dispatch(*args, **kwargs)
