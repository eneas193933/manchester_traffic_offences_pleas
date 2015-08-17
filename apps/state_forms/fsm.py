from collections import OrderedDict
from copy import deepcopy
from operator import eq
import re

from states import BaseState
from . import ex


RE_STATE_CONDITION = re.compile('(.*)\[(.*)\]')


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
    def __init__(self, verify_on_execute=True, initial_state=None):
        self.states = deepcopy(self.base_states)

        try:
            self.__state = self.states.keys()[0]
        except IndexError:
            self.__state = ''

        self.dbg = None
        self.verify_on_execute = verify_on_execute

        if initial_state is not None:
            self.set_initial_state(initial_state)

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


class ConditionalFSM(BaseFSM):
    __metaclass__ = DeclarativeStatesMetaclass

    def __init__(self, state_data, *args, **kwargs):
        super(ConditionalFSM, self).__init__(*args, **kwargs)

        def make_condition(operator, operands):
            c = [operator, ] + operands
            return c

        self.state_data = state_data

        self.exit_state_conditions = {}
        for name, state in self.states.items():
            for idx, exit_state in enumerate(state.exit_states):
                matches = RE_STATE_CONDITION.match(exit_state)
                if matches is not None:
                    e_state, condition = matches.groups()
                    state.exit_states[idx] = e_state

                    if "=" in condition:
                        terms = make_condition("eq", condition.split("="))

                    if state.name not in self.exit_state_conditions:
                        self.exit_state_conditions[state.name] = [{e_state: terms}]
                    else:
                        self.exit_state_conditions[state.name].append({e_state: terms})

        self.state.load(self.state_data)

    def invalidate_data(self):
        for key, value in self.state_data.items():
            value["valid"] = False

    def move_to_best(self):
        """
        Starts at the beginning of the journey and
        :return:
        """
        self.__BaseFSM__state = self.states[0]
        self.invalidate_data()

        while(self.move_to_next()):
            pass

    def move_to_next(self):
        next_state = None

        # Check if the data meets any of our conditions
        for condition in self.exit_state_conditions.get(self.state.name, {}):
            exit_state, [operator, op1, op2] = condition.items()[0]
            data = self.state_data.get(self.state.name, {}).get(op1)
            if operator == "eq" and eq(data, op2):
                next_state = exit_state
                break

        # If the data doesn't meet any conditions choose the first unconditional
        # exit state
        if next_state is None:
            conditional_states = [s.keys()[0] for s in self.exit_state_conditions.get(self.state.name, {})]
            available_states = list(set(self.state.exit_states) - set(conditional_states))

            if available_states:
                next_state = available_states[0]


        if next_state is not None:
            self.state.load(self.state_data)
            updated_state_data = self.state.save()

            self.change(next_state)

            if updated_state_data is not None:
                self.state_data = updated_state_data
            else:
                return False

            return True
