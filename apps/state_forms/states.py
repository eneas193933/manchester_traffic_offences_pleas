class BaseState(object):
    """
    Represents each individual state of the machine.

    exit_states:
        a list of strings representing allowed transitions from this state

    entry_action(exited_state, model):
        a function to run on entry into the state.

    exit action(target_state, model):
        a function to run on exit from the state, must return
        FSM_TransitionNotAllowed if conditions for the transition are not
        met.

    """
    name = ""
    exit_states = []
    entry_action = None
    exit_action = None
    creation_counter = 0

    def __init__(self, label=None, exits_to=None,
                 entry_action=None, exit_action=None, **kwargs):
        self.label = label
        self.exit_states = exits_to or []
        self.entry_action = entry_action
        self.exit_action = exit_action
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.creation_counter = BaseState.creation_counter
        BaseState.creation_counter += 1

    def __unicode__(self):
        if self.label:
            return self.label
        return self.name

    def init(self, **kwargs):
        pass

    def exit(self, target_state, *args, **kwargs):
        """
        Checks states and exits if possible, if not possible it raises FSM_TransitionNotAllowed

        """
        if self.exit_action:
            if hasattr(self.exit_action, '__iter__'):
                for action in self.exit_action:
                    action(target_state, *args, **kwargs)
            else:
                self.exit_action(target_state, *args, **kwargs)

    def enter(self, exited_state, *args, **kwargs):
        """
        Runs an entry action if it is set
        """
        if self.entry_action:
            if hasattr(self.entry_action, '__iter__'):
                for action in self.entry_action:
                    action(exited_state, *args, **kwargs)
            else:
                self.entry_action(exited_state, *args, **kwargs)


class StateWithForm(BaseState):
    form_class = None
    template = None

    @property
    def my_data(self):
        return self.all_data.get(self.name, {})

    def verify(self):
        if self.form_class is not None:
            my_data = self.my_data
            self.form = self.form_class(data=my_data)
            if self.form.is_valid():
                my_data["valid"] = True
                return True
            else:
                self.form = self.form_class(initial=my_data)

        return True

    def load(self):
        """
        Loads the state, returns a form with initial set to the data
        stored in the key in self.data for this state. If form_class
        is None then None is returned.

        :return: form
        """
        if self.form_class is not None:
            self.form = self.form_class(initial=self.my_data)

    def save(self, post_data=None):
        """
        Validates the form with post_data and returns the data with
        valid=True set.

        :param post_data: a dict containing values to validate
        :return: the validated data or None if invalid
        """
        if post_data is None: post_data = {}
        save_data = {"valid": False}

        if self.form_class is not None:
            self.form = self.form_class(data=post_data)

            if self.form.is_valid():
                save_data = self.form.cleaned_data
                save_data["valid"] = True
        else:
            save_data = {"valid": True}

        return save_data
