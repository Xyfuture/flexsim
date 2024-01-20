import torch
import torch.fx as fx

# Sample module
class M(torch.nn.Module):
    def forward(self, x, y):
        return torch.add(x, y)

def transform(m: torch.nn.Module,
              tracer_class : type = fx.Tracer) -> torch.nn.Module:
    graph : fx.Graph = tracer_class().trace(m)
    # FX represents its Graph as an ordered list of
    # nodes, so we can iterate through them.
    for node in graph.nodes:
        # Checks if we're calling a function (i.e:
        # torch.add)
        if node.op == 'call_function' and node.target == torch.add:
            # The target attribute is the function
            # that call_function calls.
            with graph.inserting_after(node):
                # Insert a new `call_function` node calling `torch.relu`
                new_node = graph.call_function(
                    torch.relu, args=(node,))

                # We want all places that used the value of `node` to
                # now use that value after the `relu` call we've added.
                # We use the `replace_all_uses_with` API to do this.
                node.replace_all_uses_with(new_node)

    graph.lint() # Does some checks to make sure the
                 # Graph is well-formed.

    return fx.GraphModule(m, graph)

transform(M())