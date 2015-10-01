from collections import OrderedDict
from copy import deepcopy
from operator import eq

from states import BaseState
from . import ex


def get_declared_states(bases, attrs, with_base_states=True, state_type=None):
    """
    *Taken pretty much verbatim from django.forms*

    Create a list of State instances from the passed in 'attrs', plus any
    similar states on the base classes (in 'bases').

    If 'with_base_states' is True, all states from the bases are used.
    Otherwise, only states in the 'declared_states' attribute on the bases are
    used.

    """
    if state_type is None:
        states = [(state_name, attrs.pop(state_name))
                  for state_name, obj in attrs.items()
                      if isinstance(obj, BaseState)]
    else:
        states = [(state_name, attrs.pop(state_name))
                  for state_name, obj in attrs.items()
                      if isinstance(obj, state_type)]

    for name, state in states:
        state.name = name
    states.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another StateMachine, add that
    # Note that we loop over the bases in *reverse*. This is necessary in
    # order to preserve the correct order of states.
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
    Simple FSM implementation with a declarative approach in-keeping with
    the Django style.
    """
    def __init__(self, verify_on_execute=True, initial_state=None, **kwargs):
        self.states = deepcopy(self.base_states)

        try:
            self.__state = self.states.keys()[0]
        except IndexError:
            self.__state = ''

        self.dbg = None
        self.verify_on_execute = verify_on_execute

        if initial_state is not None:
            self.set_initial_state(initial_state, **kwargs)

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
        Sets the initial state
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

    def change(self, new_state=None, *args, **kwargs):
        """
        Transitions the machine to its new state, assuming it is a
        valid exit state and that entry and exit functions allow it.

        All provided arguments are passed to the relevant exit and entry
        functions as well as the current state.
        """

        if new_state is None:
            pass

        if self.verify_on_execute:
            self.verify()

        if new_state not in self.states:
            raise ex.StateDoesNotExist(new_state)

        exiting_state = self.state

        if new_state not in exiting_state.exit_states:
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


class FormBasedFSM(BaseFSM):
    __metaclass__ = DeclarativeStatesMetaclass

    def __init__(self, state_data, *args, **kwargs):
        super(FormBasedFSM, self).__init__(*args, **kwargs)

        self.state_data = state_data
        self.state.all_data = state_data

    def _get_next_state(self):
        next_state = self.state.get_next()
        return self.states.get(next_state)

    def _invalidate_states_data(self):
        for key, value in self.state_data.items():
            value["valid"] = False

    def change(self, new_state=None, *args, **kwargs):
        super(FormBasedFSM, self).change(new_state, *args, **kwargs)
        self.state.all_data = self.state_data

    def init(self, state=None, index=None):
        """
        Starts at the beginning of the journey and moves through
        all the states until it finds an invalid one or arrives at
        the requested_state
        :return:
        """
        current = self.states.keys()[0]

        # If we're already where we need to be then return
        if state == current:
            return

        # Invalidate all the states and move to the start
        self._invalidate_states_data()

        while(True):
            next = self._get_next_state()
            verified = self.state.validate()
            if current == state or not verified:
                break

            self.change(next.name)
            current = next.name

    def move(self, new_data=None):
        data = self.state.save(new_data)
        if data["valid"] is False:
            return data
        else:
            self.state_data[self.state.name] = data

        next = self._get_next_state()

        if next is not None and next.name != self.state.name:
            self.change(next.name)

        return data