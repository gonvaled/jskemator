This tool takes as input json data and produces an skeleton of a corresponding json schema.
Most parameters are necessarily arbitrary, since they can not be inferred from the json data.

## Usage

Python2
```bash
python2 jskemator.py -f examples/example.json > schema.json
```
Python3
```bash
python3 jskemator3.py -f examples/example.json > schema.json
```
## Example Ouput

```json
{
    "description": "Dummy description",
    "additionalProperties": false,
    "required": true,
    "type": "object",
    "properties": {
        "foo": {
            "description": "Dummy description",
            "additionalProperties": false,
            "required": true,
            "type": "string",
            "pattern": "",
            "value": "lorem"
        },
        "bar": {
            "description": "Dummy description",
            "additionalProperties": false,
            "required": true,
            "type": "string",
            "pattern": "",
            "value": "ipsum"
        }
    }
}
```

Now you can edit the schema, to fill in the generated skeleton with real data.

If you modify the original json data (examples/example.json), you can reuse the schema by doing:
jskemator.py -f examples/example.json -s schema

This allows for iterative development: json_data -> schema ; refine data -> refine schema ; ...
