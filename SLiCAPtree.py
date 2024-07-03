#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 22:18:43 2022

@author: anton
"""

from SLiCAP import *
import types
import dis
from copy import deepcopy
import inspect

functions      = {}
classes        = {}
lists          = []
tuples         = []
dicts          = {}
strings        = []
methods        = []
calls          = {}
function_paths = {}
hierarchy      = []
level          = -1
txt            = ""
file_col       = 60
sub_functions  = []

def get_function_calls(func):
    # the used instructions
    ins = list(dis.get_instructions(func))
    # list for storing function names
    names = []
    # go through call stack
    for inst in ins:
        if inst.opname == "LOAD_GLOBAL":
            names.append(inst.argval)
    return list(set(names))

def get_attributes(func):
    # the used instructions
    ins = list(dis.get_instructions(func))
    # list for storing function names
    names = []
    # go through call stack
    for inst in ins:
        if inst.opname == "STORE_ATTR" or inst.opname == "LOAD_ATTR":
            names.append(inst.argval)
    return list(set(names))
    
def get_function_args(func):
    # the used instructions
    ins = list(dis.get_instructions(func))
    # list for storing function names
    names = []
    # go through call stack
    for inst in ins:
        if inst.opname == "LOAD_FAST" or inst.opname == "STORE_FAST":
            names.append(inst.argval)
    return list(set(names))


def get_all():
    global lists, dicts, attributes, classes, tuples, strings, functions, calls
    for obj in dir(SLiCAP):
        T =  getattr(SLiCAP, obj)
        if isinstance(T, list):
            lists.append(obj)
        elif isinstance(T, dict):
            dicts[obj] = T
        elif isinstance(T, type):
            attributes = T.__dict__
            try:
                if attributes['__module__'].split('.')[0] == 'SLiCAP':
                    classes[obj] = T
            except:
                pass
        elif isinstance(T, tuple):
            tuples.append(obj)
        elif isinstance(T, str):
            strings.append(obj)
        elif isinstance(T, types.FunctionType):
            function_path = os.path.relpath(inspect.getfile(T))
            if function_path.split('/')[0] == 'SLiCAP':
                functions[obj] = T
                calls[obj] = get_function_calls(T)
                function_paths[obj] = function_path

def remove_non_SLiCAP():
    global calls
    for func_name in list(calls.keys()):
        slicap_calls = []
        called_functions = calls[func_name]
        for called_function in called_functions:
            if called_function in list(functions.keys()):
                slicap_calls.append(called_function)
        calls[func_name] = slicap_calls

def do_nesting(dict_in):
    global hierarchy, sub_functions
    dict_out = deepcopy(dict_in)
    for key in list(dict_out.keys()):
        if key not in hierarchy:
            hierarchy.append(key)
            called_functions = dict_out[key]
            for i in range(len(called_functions)):
                if isinstance(called_functions[i], str):
                    sub_functions.append(called_functions[i])
                    called_functions[i] = do_nesting({called_functions[i]: calls[called_functions[i]]})
            dict_out[key] = called_functions
            hierarchy.remove(key)
    sub_functions = list(set(sub_functions))
    return dict_out        

def remove_sub_keys(dict_in):
    for key in list(dict_in.keys()):
        if key in sub_functions:
            del dict_in[key]
    return dict_in

def print_nesting(dict_in): 
    global level, txt
    level += 1
    for key in list(dict_in.keys()):
        output = ""
        if level > 0:
            for i in range(level - 1):
                output += '|  '
            add_txt = output + '+--' + key 
        else:
            add_txt = '\n' + key
        spaces = ''
        for i in range(file_col - len(add_txt.strip())):
            spaces += '-'
        try:
            txt += add_txt + spaces + ': ' + function_paths[key] + '\n'
        except:
             txt += add_txt + '()\n'
        for item in dict_in[key]:
            if isinstance(item, dict):
                print_nesting(item)
    level -= 1

def add_classes():
    global calls
    for key in list(classes.keys()):
        attributes  = classes[key].__dict__
        for attribute in list(attributes.keys()):
            if attribute == '__module__':
                file_name = '/'.join(attributes[attribute].split('.')[:-1])
            if isinstance(attributes[attribute], types.FunctionType):
                if attribute != '__init__':
                    items = get_attributes(attributes[attribute])
                    f_calls = get_function_calls(attributes[attribute])
                    for f in f_calls:
                        if f in list(functions.keys()):
                            new_caller = file_name + '.' + key + '.' + attribute
                            if new_caller not in list(calls.keys()):
                                calls[new_caller] = [f]
                            else:
                                calls[new_caller].append(f)

get_all()
remove_non_SLiCAP()
add_classes()                           
nested_calls = do_nesting(calls) 
nested_calls = remove_sub_keys(nested_calls)
print_nesting(nested_calls)
f = open('SLiCAPtree.txt', 'w')
f.write(txt)
f.close()

txt = ""
    
txt += "\nSTRINGS   :\n"
for item in strings:
    if item[0] != '_':
        txt += '           ' + item + '\n'
txt += "\nLISTS     :\n"
for item in lists:
    if item[0] != '_':
        txt += '           ' + item + '\n'
txt += "\nTUPLES    :\n"
for item in tuples:
    if item[0] != '_':
        txt += '           ' + item + '\n'
txt += "\nDICTS     :\n"
for item in dicts:
    if item[0] != '_':
        txt += '           ' + item + '\n'
txt += "\nFUNCTIONS :\n"
for item in functions:
    if item[0] != '_':
        txt += '           ' + item + '\n'
txt += "\nCLASSES   :\n"
for item in classes:
    if item[0] != '_':
        txt += '           ' + item + '\n'
        
txt += "\n======================================================================\n"
txt += "                  Classes in detail\n"
txt += "======================================================================\n\n"
for key in list(classes.keys()):
    attributes  = classes[key].__dict__
    #print('\n', key, method_list)
    txt += '\n' + key 
    for attribute in list(attributes.keys()):
        if attribute == '__module__':
            file_name = '/'.join(attributes[attribute].split('.')[:-1])
        if isinstance(attributes[attribute], types.FunctionType):
            if attribute == '__init__':
                items = get_function_args(attributes[attribute])
                txt += '('
                for item in items:
                    txt += item + ', '
                if len(items) != 0:
                    txt = txt[:-2]
                txt += '): ' + file_name + '\n'
            elif attribute != '__init__':
                txt += " - " + attribute
                items = get_attributes(attributes[attribute])
                txt +=  '('
                for item in items:
                    txt += 'self.' + item + ', '
                if len(items) != 0:
                    txt = txt[:-2]
                txt += ')\n'
                f_calls = get_function_calls(attributes[attribute])
                for f in f_calls:
                    if f in list(functions.keys()):
                        txt += "   - " + f + '\n'
                        new_caller = file_name + '.' + key + '.' + attribute
                        if new_caller not in list(calls.keys()):
                            calls[new_caller] = [f]
                        else:
                            calls[new_caller].append(f)
                            
f = open("SLiCAPsummary.txt", "w")
f.write(txt)
f.close()