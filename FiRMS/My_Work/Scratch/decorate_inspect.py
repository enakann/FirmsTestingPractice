
def audit_action(action):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            # Invoke the wrapped function first
            retval = func(*args, **kwargs)
            # Now do something here with retval and/or action
            print 'In wrapper_func, handling action {!r} after wrapped function returned {!r}'.format(action, retval)
            return retval
        return wrapper_func
    return decorator_func

@audit_action(action='did something')
def do_something(*args, **kwargs):
    if args[0] == 'foo':
        return 'bar'
    else:
        return 'baz'
print(do_something('foo'))