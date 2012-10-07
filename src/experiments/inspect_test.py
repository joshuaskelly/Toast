import toast
import inspect
import sys

for mod_name, mod_obj in inspect.getmembers(sys.modules[__name__], lambda x: x == 'toast'):
    print inspect.ismodule(mod_obj)
    for class_name, obj in inspect.getmembers(mod_obj):
        print class_name, inspect.isclass(obj)