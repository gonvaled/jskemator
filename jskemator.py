"""
Take JSON data and generate a skeleton for the JSON schema which represents it

Usage:
  jskemator.py [-f|--filename <filename>] [-h|--help]

"""
import simplejson as json
import pprint
import sys
import getopt

pp = pprint.PrettyPrinter(indent=4)

class Jskemator:
    def __ini__(self):
        pass
    def load(self, json_str):
        self.obj = json.loads(json_str)
    def skemateDict(self, d):
        skema = { }
        skema['description'] = 'Dummy description'
        skema['type'] = 'object'
        skema['properties'] = { }
        for key, value in d.items ():
            skema['properties'][key] = self.skemate(value)
        skema['additionalProperties'] = False
        return skema
    def skemateList(self, l):
        skema = { } 
        skema['description'] = 'Dummy list description'
        skema['type'] = 'array'
        skema['properties'] = [ ]
        for value in l:
            skema['properties'].append(self.skemate(value)) 
        skema['additionalProperties'] = False
        return skema
    def skemateStr(self, str):
        res = {}
        res['description'] = 'Dummy string description'
        res['type'] = 'string'
        res['required'] = True
        res['pattern'] = ''
        res['value'] = str
        return res
    def skemateInt(self, i):
        res = {}
        res['description'] = 'Dummy int description'
        res['type'] = 'integer'
        res['required'] = True
        res['pattern'] = ''
        res['value'] = i
        return res
    def skemateFloat(self, f):
        res = {}
        res['description'] = 'Dummy float description'
        res['type'] = 'float'
        res['required'] = True
        res['pattern'] = ''
        res['value'] = f
        return res
    def _skemate(self, o):
        if isinstance(o, (list, tuple)):
            return self.skemateList(o)
        elif isinstance(o, dict):
            return self.skemateDict(o)
        elif isinstance(o, str):
            return self.skemateStr(o)
        elif isinstance(o, str):
            return self.skemateStr(o)
        elif isinstance(o, int):
            return self.skemateInt(o)
        elif isinstance(o, long):
            return self.skemateLong(o)
        elif isinstance(o, float):
            return self.skemateFloat(o)
        elif o == None:
            return self.skemateNone(o)
        elif o == False:
            return self.skemateFalse(o)
        elif o == True:
            return self.skemateTrue(o)
    def skemate(self):
        return self._skemate(self.obj)
        
def usage():
    print __doc__
    
def process_options(argv):
  filename = None
  h = False
  try:
    opts, args = getopt.getopt(argv[1:], "f:h", ['filename=', 'help'])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err)
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-f", "--filename"):
      filename = a
    elif o in ("-h", "--help"):
      h = True
  return filename, h

def main():
    filename, h = process_options(sys.argv)
    if h or filename == None:
        usage ()
        sys.exit(0)
    jskemator = Jskemator()
    try:
        h = open(filename)
    except:
        print "File %s can not be opened for reading" % (filename)
        sys.exit(0)
    json_str = h.read()
    h.close()
    jskemator.load(json_str)
    #pp.pprint(jskemator.obj)
    skema = jskemator.skemate()
    #pp.pprint(skema)
    print json.dumps(skema, indent=4)
    
if __name__ == '__main__':
  main()
