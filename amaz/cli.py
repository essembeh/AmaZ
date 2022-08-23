"""
command line interface
"""
import base64
from argparse import ArgumentParser
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from . import __name__ as appname, ast_utils
from .utils import encode_exec, iter_functions, tweak_ast, xor

ENC_FUNCTIONS = {
    "b16": (base64.b16encode, base64.b16decode),
    "b32": (base64.b32encode, base64.b32decode),
    "b64": (base64.b64encode, base64.b64decode),
    "b85": (base64.b85encode, base64.b85decode),
}

BOM = "\ufeff"


def envvar(value: str):
    """
    simple parsing function for env var string "key=value" to tuple (key, value)
    """
    i = value.index("=")
    assert i > 0
    return (value[0:i], value[i + 1 :])


def run(args=None):
    parser = ArgumentParser(description="simple python code obfuscator")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        metavar="MY_MODULE.PY",
        help="python file to read",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        metavar="MY_MODULE.PY",
        help="generated python file",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="overwrite output file if it exists"
    )
    parser.add_argument(
        "-a",
        "--tweak-ast",
        action="store_true",
        help="change constants in ast before encoding it",
    )
    parser.add_argument(
        "-s",
        "--encode-source",
        choices=ENC_FUNCTIONS.keys(),
        default="b85",
        help="choose the function to encode the module code",
    )
    parser.add_argument(
        "-l",
        "--encode-loader",
        choices=["none"] + list(ENC_FUNCTIONS.keys()),
        default="b85",
        help="choose the function to encode the loader",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-k", "--key", metavar="VALUE", help="the key for xor rotation")
    group.add_argument(
        "-e",
        "--env",
        metavar="KEY=VALUE",
        type=envvar,
        help="the env value to test at runtime",
    )
    group.add_argument("--bom", action="store_true", help="use bom as xor key")

    # parse args
    args = parser.parse_args(args)

    # check output file does not exists, of force mode
    if args.output and args.output.exists() and not args.force:
        raise ValueError(f"File {args.output} already exists")

    # get the encode/decode funtion
    encode_fnc, decode_fnc = ENC_FUNCTIONS[args.encode_source]

    # manage the key for both encoding and decoding
    key = key_str = None
    imports = []
    if args.env:
        key = args.env[1]
        key_str = f"os.getenv('{args.env[0]}').encode()"
        imports += ["os", "itertools"]
    elif args.key:
        key = args.key
        key_str = f"'{key}'"
        key_str = f"[{','.join(map(oct, map(ord, key)))}]"
        imports += ["itertools"]
    elif args.bom:
        key = BOM
        key_str = 'open(__file__,"rb").read(0b11)'
        imports += ["itertools"]

    # read the source code and obfuscate it
    text = args.input.read_text()
    # tweak ast
    ast_extra_code = None
    if args.tweak_ast:
        text = tweak_ast(text)
        ast_extra_code = Path(ast_utils.__file__).read_text()
        if args.encode_loader in ENC_FUNCTIONS:
            loader_encode_fnc, loader_decode_fnc = ENC_FUNCTIONS[args.encode_loader]
            ast_extra_code = encode_exec(
                ast_extra_code,
                loader_encode_fnc,
                loader_decode_fnc,
            )

    # if key is defined, encrypt data
    data = text.encode()
    if key:
        data = xor(data, key)
    # encode data
    obfuscated_code = encode_fnc(data).decode()

    # use the template to generate the obfuscated content
    env = Environment(loader=PackageLoader(appname), autoescape=select_autoescape())

    # generate the loader code
    template_loader = env.get_template("loader.template")
    loader = template_loader.render(
        private_key=key_str,
        imports=imports,
        decode_fnc=decode_fnc.__name__,
        tweak_ast=args.tweak_ast,
    )
    # encode the loader
    if args.encode_loader in ENC_FUNCTIONS:
        loader_encode_fnc, loader_decode_fnc = ENC_FUNCTIONS[args.encode_loader]
        loader = encode_exec(loader, loader_encode_fnc, loader_decode_fnc)

    # generate the obfuscated source code
    template_src = env.get_template("src.template")
    obfuscated_source_code = template_src.render(
        obfuscated_code=obfuscated_code,
        ast_extra_code=ast_extra_code,
        loader=loader,
        functions=iter_functions(text),
    )
    # if bom key, make sure to include the bom
    if args.bom:
        obfuscated_source_code = BOM + obfuscated_source_code

    # write obfuscated content to file or stdout
    if args.output:
        args.output.write_text(obfuscated_source_code)
    else:
        print(obfuscated_source_code)
