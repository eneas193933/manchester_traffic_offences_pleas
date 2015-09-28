import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<state class path>'
    help = 'Generates a png named the same as the class path in the root of the project'

    def handle(self, args, **options):
        (module, cls) = args.rsplit('.', 1)
        tmp = __import__(module, fromlist=[cls])
        stateclass = getattr(tmp, cls)
        graph_states = stateclass({"case":{"number_of_charges": 2}})

        dot_gen = "digraph finite_state_machine {\n" \
                  "\trankdir=LR;\n" \
                  "\tnode [shape = doublecircle]; case defendant_complete company_complete;\n" \
                  "\tnode [shape = circle];\n"
        state_list = graph_states.states.items()
        for name, state in state_list:
            for exits_to in state.exit_states:
                name = getattr(state, "name", name)
                exit_name = getattr(graph_states.states[exits_to], "name", exits_to)
                if name in graph_states.exit_state_conditions:
                    printed = False
                    for condition in graph_states.exit_state_conditions[name]:
                        if condition.keys()[0] == exit_name:
                            c_values = condition.values()[0]
                            if c_values[0] == "eq":
                                node = "{1} is {2}".format(*c_values)
                            dot_gen += '\t{0} -> {1} [ label = "{2}" ];\n'.format(name, exit_name, node.replace("_", " "))
                            printed = True
                            break

                    if not printed:
                        dot_gen += '\t%s -> %s;\n' % (name, exit_name)
                else:
                    dot_gen += '\t%s -> %s;\n' % (name, exit_name)

        dot_gen += "}\n"

        print dot_gen, cls

        proc = subprocess.Popen(["dot", "-Tpng", "-o", "%s.png" % cls],
                                stdin=subprocess.PIPE)
        proc.communicate(dot_gen)