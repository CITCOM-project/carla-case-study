from causal_testing.specification.causal_dag import CausalDAG
from causal_testing.specification.metamorphic_relation import (
    generate_metamorphic_relations,
)
import json

dag = CausalDAG("dag.dot")
relations = generate_metamorphic_relations(dag)
tests = [
    relation.to_json_stub(skip=False)
    for relation in relations
    if len(list(dag.graph.predecessors(relation.output_var))) > 0
]
print(len(tests), "tests")

with open("causal_tests.json", "w") as f:
    json.dump({"tests": tests}, f, indent=2)
