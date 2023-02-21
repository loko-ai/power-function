import importlib
import json
from pathlib import Path

from flask import Flask, request, jsonify, make_response
from frozendict import frozendict
from loguru import logger
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, save_extensions, Arg

from utils.compile_utils import compile_fun
import numpy as np

app = Flask("power functions")

description = """
A component that allows the execution of python code. Additional libraries can be configured in the 'imports.json' file where you can specify the name associated to the import.
The library has to be specified in the requirements.txt file too.
"""
modules = {}
imports_file = Path("../imports.json")
if imports_file.exists():
    with imports_file.open() as o:
        imports = json.load(o)
        for name, m in imports.items():
            try:
                module = importlib.import_module(m)
                modules[name] = module

            except Exception as e:
                logger.exception(e)

modules = frozendict(modules)

c = Component("Power Function", args=[Arg("code", type="code")], description=description)

save_extensions([c])

logger.debug("Imported modules")
logger.debug(modules)


def json_response(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    else:
        return o


@app.route("/", methods=["POST"])
@extract_value_args(_request=request)
def execute(value, args):
    code = args.get("code")
    f = compile_fun(code, g=modules)
    return jsonify(json_response(f(value, args)))


@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(e)
    response = make_response(f"Error {e}", 500)
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
