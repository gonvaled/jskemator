This tool takes as input json data and produces an skeleton of a corresponding json schema.
Most parameters are necessarily arbitrary, since they can not be inferred from the json data.

## Use

jskemator.py -f examples/example.json > schema

Now you can edit the schema, to fill in the generated skeleton with real data.

If you modify the original json data (examples/example.json), you can reuse the schema by doing:
jskemator.py -f examples/example.json -s schema

This allows for iterative development: json_data -> schema ; refine data -> refine schema ; ...
