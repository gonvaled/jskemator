"""
Take JSON data and generate a skeleton for the JSON schema which represents it

Usage:
  jskemator.py [-f|--filename <filename>] [-s|--schema <schema>] [-h|--help]

"""
import simplejson as json
import pprint
import sys
import getopt

pp = pprint.PrettyPrinter(indent=4)

class Jskemator:
    def __init__(self):
        self.obj = None
        self.s = None
    def load(self, json_str):
        self.obj = json.loads(json_str)
    def schema(self, schema_str):
        self.s = json.loads(schema_str)
    def set_defaults (self, s):
        default = { }
        if s != None:
            default['description'] = s['description']
            default['additionalProperties'] = s['additionalProperties']
            default['required'] = s['required']
        else:
            default['description'] = 'Dummy description'
            default['additionalProperties'] = False
            default['required'] = True
        return default
    def _skemateDict(self, d, s):
        #print "_skemateDict"
        skema=self.set_defaults(s)
        skema['type'] = 'object'
        skema['properties'] = { }
        for key, value in list(d.items ()):
            #print "key > ", key
            if s == None:
                new_s = None
            else:
                new_s = s['properties'][key]
            skema['properties'][key] = self._skemate(value, new_s)
        return skema
    def _skemateList(self, l, s):
        #print "_skemateList"
        skema=self.set_defaults(s)
        skema['type'] = 'array'
        skema['properties'] = [ ]
        for value in l:
            skema['properties'].append(self._skemate(value)) 
        return skema
    def _skemateStr(self, str, s):
        #print "_skemateStr"
        res=self.set_defaults(s)
        res['type'] = 'string'
        res['pattern'] = ''
        res['value'] = str
        return res
    def _skemateInt(self, i, s):
        #print "_skemateInt"
        res=self.set_defaults(s)
        res['type'] = 'integer'
        res['pattern'] = ''
        res['value'] = i
        return res
    def _skemateFloat(self, f, s):
        print("_skemateFloat")
        res=self.set_defaults(s)
        res['type'] = 'float'
        res['pattern'] = ''
        res['value'] = f
        return res
    def _skemate(self, o, s=None):
        if isinstance(o, (list, tuple)):
            return self._skemateList(o, s)
        elif isinstance(o, dict):
            return self._skemateDict(o, s)
        elif isinstance(o, str):
            return self._skemateStr(o, s)
        elif isinstance(o, str):
            return self._skemateStr(o, s)
        elif isinstance(o, int):
            return self._skemateInt(o, s)
        elif isinstance(o, int):
            return self._skemateLong(o, s)
        elif isinstance(o, float):
            return self._skemateFloat(o, s)
        elif o == None:
            return self._skemateNone(o, s)
        elif o == False:
            return self._skemateFalse(o, s)
        elif o == True:
            return self._skemateTrue(o, s)
    def skemate(self):
        return self._skemate(self.obj, self.s)
        
def usage():
    print(__doc__)
    
def process_options(argv):
  filename = None
  schema = None
  h = False
  try:
    opts, args = getopt.getopt(argv[1:], "f:s:h", ['filename=', 'schema', 'help'])
  except getopt.GetoptError as err:
    # print help information and exit:
    print(str(err))
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-f", "--filename"):
      filename = a
    elif o in ("-s", "--schema"):
      schema = a
    elif o in ("-h", "--help"):
      h = True
  return filename, schema, h

def main():
    filename, schema, h = process_options(sys.argv)
    if h or filename == None:
        usage ()
        sys.exit(0)
    jskemator = Jskemator()
    try:
        h = open(filename)
    except:
        print("File %s can not be opened for reading" % (filename))
        sys.exit(0)
    json_str = h.read()
    h.close()
    if schema != None:
        try:
            h = open(schema)
        except:
            print("Schema %s can not be opened for reading" % (schema))
            sys.exit(0)
        schema_str = h.read()
        jskemator.schema(schema_str)
    jskemator.load(json_str)
    #pp.pprint(jskemator.obj)
    skema = jskemator.skemate()
    #pp.pprint(skema)
    print(json.dumps(skema, indent=4))
    
if __name__ == '__main__':
  main()

