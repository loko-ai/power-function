from flask import Flask, request, jsonify
from frozendict import frozendict
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, save_extensions, Arg

from utils.compile_utils import compile_fun

app = Flask("power functions")

c = Component("Power Function", args=[Arg("code", type="code")])

save_extensions([c])
import pandas as pd
import numpy as np


@app.route("/", methods=["POST"])
@extract_value_args(_request=request)
def execute(value, args):
    code = args.get("code")
    f = compile_fun(code, g=frozendict(pd=pd, np=np))
    return jsonify(f(value, args))


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
