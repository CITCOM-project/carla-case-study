from causal_testing.specification.causal_dag import CausalDAG
from causal_testing.specification.metamorphic_relation import (
    generate_metamorphic_relations,
)
import json

dag = CausalDAG("dag.dot")
relations = generate_metamorphic_relations(dag)
tests = {"tests": [relation.to_json_stub() for relation in relations]}

with open("causal_tests.json", 'w') as f:
    json.dump(tests, f, indent=2)
