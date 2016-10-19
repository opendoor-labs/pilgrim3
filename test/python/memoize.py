import inspect
# Private import to format error messages.
# if this changes, no big deal, just remove
from _pytest.fixtures import fail_fixturefunc


cache = {}
# Memoizes the value.
# Works with generator or function.
# has same restrictions on generators as pytest - can only yield once

# I think this is the behavior you want, start up, value, teardown happens once in expected scope.
# The value is memoized.
def memoize(func):
    func_name = func.__name__
    generator_key = func_name + '__generator__memoize__'

    def memoized_func(*args):
        if func_name not in cache:
            value = func(*args)
            if inspect.isgeneratorfunction(func):
                cache[generator_key] = value
                value = next(value)
            cache[func_name] = value

        return cache[func_name]

    def generator_after():
        if generator_key in cache:
            try:
                next(cache[generator_key])
            except StopIteration:
                cache.pop(generator_key)
            else:
                fail_fixturefunc(func, "yield_fixture function has more than one 'yield'")

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
    code = (code % (func_name, arg_string, arg_string, func_name))

    generated = {}
    exec code.strip() in generated

    return generated["binder"](memoized_func, generator_after)

def clear_memoized_cache():
    cache.clear()