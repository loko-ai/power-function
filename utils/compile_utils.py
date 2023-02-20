import functools

from frozendict import frozendict


@functools.cache
def compile_fun(s_code, g=None):
    f = "secret_function_name"
    temp = ["def %s(data,args):" % f] + ["\t" + x for x in s_code.split("\n")]
    try:
        code = compile("\n".join(temp), "<string>", "exec")
        g = dict(g) if g else {}
        exec(code, g)
        return g[f]
    except Exception as e:
        if hasattr(e, 'lineno'):
            e.lineno = e.lineno - 1
        raise e


if __name__ == '__main__':
    import pandas as pd

    g = dict(pd=pd)
    import numpy as np

    f = compile_fun("""
    for i in range(10):
        print("Data",data,args)
    """, g=frozendict(pd=pd))

    print(f("Ciao", {}))
