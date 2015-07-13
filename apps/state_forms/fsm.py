from collections import OrderedDict
from copy import deepcopy

from states import BaseState
import ex


def get_declared_states(bases, attrs, with_base_states=True):
    """
    *Taken pretty much verbatim from django.forms*

    Create a list of State instances from the passed in 'attrs', plus any
    similar states on the base classes (in 'bases').

    If 'with_base_states' is True, all states from the bases are used.
    Otherwise, only states in the 'declared_states' attribute on the bases are
    used.

    """
    states = [(state_name, attrs.pop(state_name))
              for state_name, obj in attrs.items()
              if isinstance(obj, BaseState)]
    for name, state in states:
        state.name = name
    states.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another StateMachine, add that
    # Note that we loop over the bases in *reverse*. This is necessary in
    # order to preserve the correct order of statess.
    # order of statess.
    if with_base_states:
        for base in bases:
            if hasattr(base, 'base_states'):
                states = base.base_states.items() + states
    else:
        for base in bases:
            if hasattr(base, 'declared_states'):
                states = base.declared_states.items() + states

    return OrderedDict(states)


class DeclarativeStatesMetaclass(type):
    """
    *Taken pretty much verbatim from django.forms*

    Metaclass that converts State attributes to a dictionary called
    'base_states', taking into account parent class 'base_states' as well.

    """
    def __new__(mcs, name, bases, attrs):
        attrs['base_states'] = get_declared_states(bases, attrs)
        new_class = super(
            DeclarativeStatesMetaclass,
            mcs
        ).__new__(mcs, name, bases, attrs)
        return new_class


class BaseFSM(object):
    """
    Simple FSM implementation. Takes a declarative approach to
    defining states, and their interactions and capabilities.


    """
    def __init__(self, verify_on_execute=True):
        self.states = deepcopy(self.base_states)
        try:
            self.__state = self.states.keys()[0]
        except IndexError:
            self.__state = ''
        self.dbg = None
        self.verify_on_execute = verify_on_execute

        for s in self.states.values():
            if '*' in s.exit_states:
                s.exit_states = [key for key in self.states.keys() if key != s.name]

    def __unicode__(self):
        return self.__state

    def getstate(self):
        if self.__state and self.__state in self.states:
            return self.states[self.__state]

    def setstate(self, value):
        raise ex.TransitionNotAllowed("State is read only, use change() instead.")
    state = property(getstate, setstate)

    def set_initial_state(self, state):
        """
        Sets the initial state of the FSM, should only be used when
        restoring a FSM into a state that has been previously attained
        from the initial state.
        """
        if state in self.states:
            self.__state = state
        else:
            self.__state = self.states.keys()[0]

    def available_states(self):
        """Returns a list containing the available exit states from
        the current state

        """
        return [self.states[s] for s in self.state.exit_states]

    def verify(self):
        """
        Check that all the states named in exit_states exist.

        If any named states are missing verify() throws a
        FSM_VerificationError which contains a list of the bad states.
        """
        bad_states = []
        state_names = set(self.states.keys())
        for state in self.states.values():
            bad_states.extend(set(state.exit_states) - state_names)

        if len(bad_states):
            raise ex.VerificationError("Invalid exit state(s)", bad_states)

    def change(self, new_state, *args, **kwargs):
        """
        Transitions the machine to its new state, assuming it is a
        valid exit state and that entry and exit functions allow it.

        All provided arguments are passed to the relevant exit and entry
        functions as well as the current state.
        """
        if self.verify_on_execute:
            self.verify()

        if not new_state in self.states:
            raise ex.StateDoesNotExist(new_state)

        exiting_state = self.state

        if not new_state in exiting_state.exit_states:
            raise ex.TransitionNotAllowed("%s -> %s" % (exiting_state.name, new_state))

        entering_state = self.states[new_state]

        # run the exit state functions, checking for cancellation or redirection
        try:
            exiting_state.exit(entering_state, *args, **kwargs)
        except ex.CancelTransition:
            return self.state
        except ex.RedirectTransition as e:
            return self.change(e.state.name, *args, **kwargs)

        # run the enter state functions, checking for cancellation or redirection
        try:
            entering_state.enter(exiting_state, *args, **kwargs)
        except ex.CancelTransition:
            return self.state
        except ex.RedirectTransition as e:
            return self.change(e.state.name, *args, **kwargs)

        # safe to change the state if we get this far
        self.__state = new_state

        return self.state


class FSM(BaseFSM):
    __metaclass__ = DeclarativeStatesMetaclass