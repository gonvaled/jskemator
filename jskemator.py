#!/usr/bin/env python
"""
Take JSON data and generate a skeleton for the JSON schema which represents it

Usage:
  jskemator.py
      [-f|--filename  <filename>]
      [-2|--filename2 <filename2>]
      [-s|--schema <schema>]
      [-a|--action <action>]
      [--url1      <url1>]
      [--url2      <url2>]
      [-h|--help]

  <action> can be:
      - show-skeleton
      - tabulate
      - compare
      - download-and-compare: download from url1, url2 and compare

"""
import simplejson as json
import pprint
import sys
import getopt
import os

from   wav.config.tree import TMP_DIR

pp = pprint.PrettyPrinter(indent=4)

class Jskemator:
    def __init__(self):
        self.obj = None
        self.s = None
    def load_schema(self, filename):
        try:
            h = open(filename)
        except:
            print "Schema %s can not be opened for reading" % (filename)
            return
        schema_str = h.read()
        self.schema(schema_str)
    def load(self, json_str):
        self.obj = json.loads(json_str)
    def schema(self, schema_str):
        self.s = json.loads(schema_str)
    def set_defaults(self, s):
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
        for key, value in d.items():
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
        #print "_skemateFloat"
        res=self.set_defaults(s)
        res['type'] = 'float'
        res['pattern'] = ''
        res['value'] = f
        return res
    def _skemateNone(self, f, s):
        #print "_skemateFloat"
        res=self.set_defaults(s)
        res['type'] = 'none'
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
        elif isinstance(o, long):
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
    def skemate_from_file(self, filename):
        try:
            h = open(filename)
        except:
            print "File %s can not be opened for reading" % (filename)
            return None
        json_str = h.read()
        h.close()
        self.load(json_str)
        return self.skemate()
    def compare(self, skema1, skema2):
        fmt = "|%-30s|%-10s|%-10s|%-10s|%-40s|%-40s|"
        for key in skema1['properties']:
            type1  = skema1['properties'][key]['type']
            value1 = skema1['properties'][key]['value']
            if key in skema2['properties']:
                present = 'BOTH'
                type2  = skema2['properties'][key]['type']
                value2 = skema2['properties'][key]['value']
                if type1 != type2:
                    typeB = type2
                else:
                    typeB = '-'
            else:
                present = 'FIRST'
                types   = type1
                typeB   = '(none)'
                value2  = '(none)'
            print fmt % (key, present, type1, typeB, value1, value2)
        for key in skema2['properties']:
            type2 = skema2['properties'][key]['type']
            if key not in skema1['properties']:
                typeA   = '(none)'
                value1  = '(none)'
                present = 'SECOND'
                if skema2['properties'][key]['type'] == 'array' or skema2['properties'][key]['type'] == 'object' :
                    value2 = '(recurse)'
                else:
                    value2  = skema2['properties'][key]['value']
                print fmt % (key, present, typeA, type2, value1, value2)

def usage():
    print __doc__

def process_options(argv):
  options = {
      'action'    : 'show-skeleton',
      'filename'  : None,
      'filename2' : None,
      'schema'    : None,
      'url1'      : None,
      'url2'      : None,
      'help'      : False,
      }
  try:
    opts, args = getopt.getopt(argv[1:], "a:f:s:2:h", ['action=', 'filename=', 'schema', 'filename2=', 'url1=', 'url2=', 'help'])
  except getopt.GetoptError, err:
    # print help information and exit:
    print str(err)
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-f", "--filename"):
      options['filename'] = a
    elif o in ("-2", "--filename2"):
      options['filename2'] = a
    elif o in ("-s", "--schema"):
      options['schema'] = a
    elif o in ("-a", "--action"):
      options['action'] = a
    elif o in ("-h", "--help"):
      options['help'] = True
    elif o in ("--url1"):
      options['url1'] = a
    elif o in ("--url2"):
      options['url2'] = a
  return options

def main():
    options = process_options(sys.argv)
    if options['help']:
        usage()
        sys.exit(0)
    jskemator = Jskemator()
    if options['schema'] != None:
        jskemator.load_schema(options['schema'])
    if options['action'] != 'download-and-compare':
        skema1 = jskemator.skemate_from_file(options['filename'])
        # pp.pprint(jskemator.obj)
        # pp.pprint(skema1)
    if options['action'] == 'download-and-compare':
        from wav.curl_support import CurlSupport
        curl = CurlSupport(TMP_DIR)
        url1 = options['url1']
        url2 = options['url2']
        filename1 = 'url1'
        filename2 = 'url2'
        urls = [(url1, filename1), (url2, filename2)]
        curl.add_to_queue(urls)
        curl.download()
        skema1 = jskemator.skemate_from_file(os.path.join(TMP_DIR, filename1))
        skema2 = jskemator.skemate_from_file(os.path.join(TMP_DIR, filename2))
        jskemator.compare(skema1, skema2)
    elif options['action'] == 'show-skeleton':
        print json.dumps(skema1, indent=4)
    elif options['action'] == 'tabulate':
        fmt = "%-30s %s"
        for key in skema1['properties']:
            print fmt % (key, skema1['properties'][key]['type'])
    elif options['action'] == 'compare':
        skema2 = jskemator.skemate_from_file(options['filename2'])
        jskemator.compare(skema1, skema2)

if __name__ == '__main__':
  main()
