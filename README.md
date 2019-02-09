# dag_longest_path

Calculate the longest path in a directed acyclic graph in terms of node weights (Python)

Use this class to get (one of) the paths with the largest sum of node weights
in a directed acyclic graph (DAG). After constructing the empty object,
use `add_node(label, weight)` and `add_edge(label1, label2)` to build the graph, 
and then call `longest_path` to retrieve the path and the sum of the weights.
This latter operation is destructive and will delete the graph.

## Sample

```python
    dag = DAGLongestPath()
    for i in range(6): dag.add_node(i, i)
    dag.add_edge(3, 5)
    dag.add_edge(2, 5)
    dag.add_edge(2, 4)
    dag.add_edge(1, 2)
    print(dag.longest_path())
```
