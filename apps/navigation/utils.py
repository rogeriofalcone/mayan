from __future__ import absolute_import

import logging

from django.template import (VariableDoesNotExist, Variable)
from django.utils.text import unescape_string_literal

logger = logging.getLogger(__name__)


def get_navigation_objects(context):
    objects = {}

    try:
        indirect_reference_list = Variable('navigation_object_list').resolve(context)
    except VariableDoesNotExist:
        pass
    else:
        logger.debug('found: navigation_object_list')
        for indirect_reference in indirect_reference_list:
            try:
                resolved_object = Variable(indirect_reference['object']).resolve(context)
            except VariableDoesNotExist:
                resolved_object = None
            else:
                objects.setdefault(resolved_object, {})
                objects[resolved_object]['label'] = indirect_reference.get('object_name')

    try:
        indirect_reference = Variable('navigation_object_name').resolve(context)
    except VariableDoesNotExist:
        pass
    else:
        logger.debug('found: navigation_object_name')
        try:
            object_label = Variable('object_name').resolve(context)
        except VariableDoesNotExist:
            object_label = None
        finally:
            try:
                resolved_object = Variable(indirect_reference).resolve(context)
            except VariableDoesNotExist:
                resolved_object = None

            objects.setdefault(resolved_object, {})
            objects[resolved_object]['label'] = object_label

    try:
        indirect_reference = Variable('list_object_variable_name').resolve(context)
    except VariableDoesNotExist:
        pass
    else:
        logger.debug('found renamed list object')
        try:
            object_label = Variable('object_name').resolve(context)
        except VariableDoesNotExist:
            object_label = None
        finally:
            try:
                resolved_object = Variable(indirect_reference).resolve(context)
            except VariableDoesNotExist:
                resolved_object = None
            else:
                objects.setdefault(resolved_object, {})
                objects[resolved_object]['label'] = object_label

    try:
        resolved_object = Variable('object').resolve(context)
    except VariableDoesNotExist:
        pass
    else:
        logger.debug('found single object')
        try:
            object_label = Variable('object_name').resolve(context)
        except VariableDoesNotExist:
            object_label = None
        finally:
            objects.setdefault(resolved_object, {})
            objects[resolved_object]['label'] = object_label

    #logger.debug('objects: %s' % objects)
    return objects


def resolve_template_variable(context, name):
    try:
        return unescape_string_literal(name)
    except ValueError:
        #return Variable(name).resolve(context)
        #TODO: Research if should return always as a str
        return str(Variable(name).resolve(context))
    except TypeError:
        return name


def resolve_arguments(context, src_args):
    args = []
    kwargs = {}
    
    if type(src_args) == type([]):
        for i in src_args:
            try:
                # Try to execute as a function
                val = i(context=context)
            except TypeError:
                val = resolve_template_variable(context, i)
                if val:
                    args.append(val)
            else:
                args.append(val)
    elif type(src_args) == type({}):
        for key, value in src_args.items():
            try:
                # Try to execute as a function
                val = i(context=context)
            except TypeError:            
                val = resolve_template_variable(context, value)
                if val:
                    kwargs[key] = val
            else:
                kwargs[key] = val
    else:
        val = resolve_template_variable(context, src_args)
        if val:
            args.append(val)

    return args, kwargs
