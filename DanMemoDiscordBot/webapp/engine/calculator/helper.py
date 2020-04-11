import inspect
import pprint
import base64
import hashlib

pp = pprint.PrettyPrinter(indent=4)

def pretty(d, indent=4):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

class AutoInit(type):
  def __new__(meta, classname, supers, classdict):
    classdict['__init__'] = meta.autoInitDecorator(classdict['__init__'])
    return type.__new__(meta, classname, supers, classdict)
  def autoInitDecorator(toDecoreFunction):
    def wrapper(*args, **kargs):
      allArgs, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(toDecoreFunction)

      objref = args[0]

      for i in range(1,len(args)):
        setattr(objref, allArgs[i], args[i])
      if defaults != None:
          for i in range(len(defaults)):
            setattr(objref, allArgs[len(args)+i], defaults[i])
      for attribute in kargs:
        setattr(objref, attribute, kargs[attribute])

    return wrapper

class Helper(metaclass=AutoInit):
  def __init__(self):
    pass
  def __repr__(self):
    return pprint.pformat(self.__dict__,indent=4)
    #return str(self.__dict__)

def hashAll(*args):
    md5 = hashlib.md5()
    h = ""
    for arg in args:
        '''if isinstance(arg, list):
            continue
        if isinstance(arg, dict):
            continue'''
        s = str(arg)
        #print(s)
        md5.update(s.encode('utf-8'))
        #h = hash((h,arg))
        #print(h)
    h = md5.digest()
    h = base64.b32encode(h)
    return h