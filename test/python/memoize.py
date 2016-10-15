import inspect


# Memoizes the value.
# Works with generator or function.
# has same restrictions on generators as pytest - can only yield once

# I think this is the behavior you want, start up, value, teardown happens once in expected scope.
# The value is memoized.
def memoize(func):
    cache = {}

    def memoized_func(*args):
        if 'value' not in cache:
            value = func(*args)
            if inspect.isgeneratorfunction(func):
                cache['generator'] = value
                value = next(value)
            cache['value'] = value

        return cache['value']

    def generator_after():
        if 'generator' in cache:
            try:
                next(cache['generator'])
            except StopIteration:
                cache.pop('generator')

    arg_string = ",".join(inspect.getargspec(func)[0])

    # We create a wrapper method to be able to bind the generated method (which mirrors the fixture method exactly)
    # to the memoized_func and after handler
    code = '''
        def binder(mem_func, after):
            def %s(%s):
                try:
                    yield mem_func(%s)
                finally:
                    after()
            return %s
    '''
    code = (code % (func.__name__, arg_string, arg_string, func.__name__))

    generated = {}
    exec code.strip() in generated

    return generated["binder"](memoized_func, generator_after)
