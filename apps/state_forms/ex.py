class StateDoesNotExist(Exception):
    """
    Raised when a change to a non-existent state is requested.
    """
    def __init__(self, state):
        super(StateDoesNotExist, self).__init__()
        self.state = state

    def __str__(self):
        return  "%s does not exist" % self.state.name


class TransitionNotAllowed(Exception):
    pass


class CancelTransition(Exception):
    """
    Raise in enter or exit state action to cancel the transition
    """


class RedirectTransition(Exception):
    """
    Raise in enter state action to redirect to an alternate state
    """
    def __init__(self, state, message=None):
        super(RedirectTransition, self).__init__()
        self.state = state
        self.message = message or ""


class VerificationError(Exception):
    """Verification error, raised when FSM.verify() fails, should
    contain a list of failed states.

    """
    def __init__(self, message, states=None):
        super(VerificationError, self).__init__()
        self.message = message
        self.states = states

    def __str__(self):
        if self.states:
            return "{}:\n    {}".format(self.message, "\n    ".join(self.states))
        else:
            return self.message
