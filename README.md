# AmaZ - Simple Python Obfuscator

_AmaZ_ is a source code obfuscator, written in Python.

Then main idea was to keep the original code and not change it at all (or the least possible) to ensure it will have the same behavior.

# Install

First, you need a recent python3, tested with python 3.7, 3.8 and 3.9, on Ubuntu:LTS, Debian:10 and Debian:11.

> This project uses [Poetry](https://python-poetry.org) as build system, ensure you have _Poetry_ installed

```sh
$ pip3 install --user -U poetry
$ poetry --version
```

You can install _AmaZ_ either after building the package or directly in a _virtualenv_

## Build and install

You can build the _Wheel_ package like any _CI_ job would do to publish it on _Pypi_ for example.

```sh
$ git clone https://github.com/essembeh/AmaZ
$ cd AmaZ

# build the python package of the app
$ poetry build

# install the app for your user
$ pip3 install dist/AmaZ-0.1.0-py3-none-any.whl

# run the app
$ amaz --help
```

## Install in a _virtualenv_

```sh
$ git clone https://github.com/essembeh/AmaZ
$ cd AmaZ

# create the virtualenv containing the app and its dependencies
$ poetry install

# run the app in its virtualenv
$ poetry run amaz --help

# or activate the virtualenv and run the app
$ poetry shell
(.venv) $ amaz --help

# to run the tests:
$ poetry run pytest tests/
# or using tox
$ pip3 install tox
$ tox
```

> Note: unit tests will ensure the clean code and obfuscated code will have the same behavior for all obfuscation option you can use.

# How it works

_AmaZ_ only support python source code obfuscation for now.

Each python function in the given module is replaced by a dummy one that does nothing by default, for example:

```py
@static_method
def my_function(*args, **kwargs):
    pass
```

> For every function from the clean code, a dummy function with the exact same name will be created in the obfuscated code, so that you can use the obfuscated code as a library the same way you use the non obfuscated code.

You can edit the generated file to write some code instead of the `pass` instruction to let others think your function does something else (see example below when using encryption key from _env_ variable).

Note the `@static_method` annotation in the code snippet above, this will dynamically change the function behavior at the runtime and execute the original code instead of the code written in the obfuscated file. The annotation `@static_method` is very similar to the `@staticmethod` and may not be noticed at the first time.

The obfuscated module will also have a _loader_ that will read the original source code from a encoded/encrypted string so the the annotation could execute the original code.

> Note: as the _loader_ is only executed once, there will be a slight longer loading time for the obfuscated module, but the execution will have quite the same performance as the original code.

# Command line interface

_AmaZ_ tool takes a `.py` file, a python module, as input with `--input <FILE>` and outputs an obfuscated python module, you can save the obfuscated code with `--output <FILE>`

```sh
# basic usage
$ amaz -i samples/clean.py -o obfuscated.py
```

This will transform `samples/clean.py`:

```py
def hello_world():
    """
    some documentation here
    """
    return "Hello World =)"


def my_function(a: int, b: int, c: int):
    """
    simple addition
    """
    return a + b + c + 42


def test():
    """
    all in one test
    """
    print(hello_world(), my_function(1, 2, 3))
```

to an obfuscated module `obfuscated.py`:

```py
"""
WMyU`Xk~0{Z(nzBa%^NMDLM)uARr(jA|eVPARr)fZ*65DWN%}2ZDnqBVRUJ4ZXjr7a%Bo2ARr(jA|eVPARr)eWps6NZXhB^Wo&G3AXjg4Y-AukDIy9A3S?zwAZ>YHW_503bZKvHC}BDvX>N2ZAYwWoX>N2ZAY(cpX>N2WItm~lARr<lA_^cNARu#TZE$R5AYo)=X>@6CZVDhEARr<lA_^cNARuyObairWAYmXYAYvdZAY&jaAT%-x3JPRpW*~HBb95*vItm~lARr<lA_^cNARu9EY#?cFAa8DEAarGObP6CKARr<lA_^cNARusZX>N2VXk~0{Z(nzBa%^NMDJ&pud0%FAZew(5Z*C|tEFdy0ATuc`3I
"""
import base64
exec(base64.b85decode(b'X>D+Ca&#bJb94$?PE#N~AbWiZbaHt*3LqdLAYmXqAYx&2Wi~V}VmLKqWn*t-Whh@?WN%|%Ut2LcEiqj#a%FIAVPj<|B3y1FEFvN)DGDGUARu8NJs@FobS`jVa&u)UVJQkAARr)Rcx7WKV{dJ6X>4UEVJsjbJYjQmJ|Zk2B4v1GV<IUmAX-jSDGFtHV`Xr3Itm~lARusIb8`x0Wo96AbYXO9V_$7$bZBp6C}wqTV<|ccARr(hWMyU`cXDBHaAk5RDq$=jDk@=NDLM)uARr(hARr)eWps6NZXjAtQ(I<rZeuQAUv6P-WnW)iC@NtrASx<hVJRSKW*}yDZeuQAUv6P-WnW()X>K4|PE#OdY;$EGW_503C@NtrASx<hVJQkAARr)eWps6NZXkDZVQ_F|as'))

@static_method
def hello_world(*args, **kwargs):
    pass

@static_method
def my_function(*args, **kwargs):
    pass

@static_method
def test(*args, **kwargs):
    pass
```

You can test that both files have the same behavior:

```sh
$ python3 -c 'import samples.clean as m; m.test()'
Hello World =) 48

$ python3 -c 'import obfuscated as m; m.test()'
Hello World =) 48
```

You have some options to obfuscate the code.

## Encode the source code

The original source code will be encoded in the file `__doc__` like

```py
"""
WMyU`Xk~0{Z(nzBa%^NMDLM)uARr(jA|eVPARr)fZ*65DWN%}2ZDnqBVRUJ4ZXjr7a%Bo2ARr(jA|eVPARr)eWps6NZXhB^Wo&G3AXjg4Y-AukDIy9A3S?zwAZ>YHW_503bZKvHC}BDvX>N2ZAYwWoX>N2ZAY(cpX>N2WItm~lARr<lA_^cNARu#TZE$R5AYo)=X>@6CZVDhEARr<lA_^cNARuyObairWAYmXYAYvdZAY&jaAT%-x3JPRpW*~HBb95*vItm~lARr<lA_^cNARu9EY#?cFAa8DEAarGObP6CKARr<lA_^cNARusZX>N2VXk~0{Z(nzBa%^NMDJ&pud0%FAZew(5Z*C|tEFdy0ATuc`3I
"""
```

You can encode the source code using one of the function:

- _base85_ using `--encode-source b85`
- _base64_ using `--encode-source b64`
- _base32_ using `--encode-source b32`
- _base16_ using `--encode-source b16`

> Default is _base85_ because it reduces the size of encoded code.

## Encrypt the source code

You can also encrypt the source code using a `xor` function with a key. The key can be:

- hardcoded using `--key MYKEY`: the key will be obfuscated as bytes in the loader
- the 3 bytes of the [UTF-8 BOM](https://en.wikipedia.org/wiki/Byte_order_mark) which are hidden by editors (and only visible using hexa editor), so that is will be harder for someone to decrypt the code if they don't know this UTF8 feature.
- a environment variable using `--env MYVAR=myvalue`: the key won't be written in the output file, the original code will only run if the environment variable has the correct value when running the code, if not, the dummy code is executed.

> Note that when you use an environment variable, if the variable at the runtime does not allow to decrypt the code (it is different from the value used to encrypt the payload), the _dummy_ code will be executed instead of the original code.

For example, let's say we have a function `getRandomNumber` which returns 4

```sh
# original source code
$ cat test.py
def getRandomNumber():
    return 4

# test it
$ python3 -c 'import test as m; print(m.getRandomNumber())'
4

# obfuscate the code
$ amaz -i test.py -o test2.py --env LANG=fr_FR.UTF-8

# edit the obfuscated code to return 42 in the dummy function
$ cat test2.py
"""
0v9=EHA^7|CqrBb9}zP@OfV*H1OjYQe`a!AFd#EuRz^lu
"""
import base64
exec(base64.b85decode(b'X>D+Ca&#bJb94%6ZE$aLbRchY3TbU{Z*p`XX>?_BbZ>8La|&8cQy@JcdwmLYa(OxmARr(hVIVyqVqtS-HZ(3`I5lKtV{c?-C|_S>Z)0CyTQNE<F<mZlWpHd^V`V5JTy7#PA|fd%3LqdLAYmXqAR;0zYHw+7C}U`HC}AL8AYv&XW^ZyJVJskGAZczOdTDSdVJskNbY*gMZ*OdKE@OFPY-K2Kb1r9PbY*UKC?`xoPDdvxE@f_GZ)9aCDJdx_3LqdLAYmXqAYpTKE^uLTb7d%DDGDGUARuLUWn(B~Z*6dCY-K26EFdC0VRLjoA}k;xWq4&{A}K5&T250b3T1d>WpH#l3LqdLAaG%Ga|&c-W*~EPVRUI@Uu|V{Xm4aFW_503DLM)uARr)QWo96Ea$#_AWpXGgVJsjjDq&$MItm~lARr(hARuyObairWAX-jSTV{1`V=iA`ZeeX@Ute7)Dq$=jDk@=NDIjTPAZB%LV=iA`ZeeX@Utb_;ZXjAtQy^t*b7dfAb#7xQDq$=jDk@=NDGDGUARuyObairWAa`<MaByXE'))

@static_method
def getRandomNumber(*args, **kwargs):
    return 42

# see how the output changes depending of the runtime environment
$ LANG=en_EN.UTF-8 python -c 'import test2 as m; print(m.getRandomNumber())'
42
$ LANG=fr_FR.UTF-8 python -c 'import test2 as m; print(m.getRandomNumber())'
4
```

## Tweak the original python code

Use `--tweak-ast` to tweak the original python code to harden the retro engineering of the obfuscated code.

Using this option, all variables names, and string will be encrypted using `rot13` and decrypted by the _loader_.

for example:

```py
def hello_world():
    return 'Hello World =)'
```

will be encoded as

```py
def hello_world():
    return 'Uryyb Jbeyq =)'
```

> Note: as this will alter the original source code, this option is disabled by default

## Encode the loader

To dynamically decode and decrypt the original code, a _loader_ will run when the module is loaded.
To make it harder to understand how the code is obfuscated, the loader can also be encoded using one of the function:

- _base85_ using `--encode-loader b85`
- _base64_ using `--encode-loader b64`
- _base32_ using `--encode-loader b32`
- _base16_ using `--encode-loader b16`
- using `--encode-loader none` won't encode the loader

Here is an example of the loader without encoding

```py
import base64
import itertools
ZNS = {}
try:
    exec("".join(chr(a ^ b) for a, b in zip(base64.b85decode(__doc__[1:-1].replace("\n","")), itertools.cycle([0o146,0o157,0o157]))), ZNS)
except:
    pass
def static_method(func):
    def wrapper(*a, **aa):
        return ZNS[func.__name__](*a, **aa) if func.__name__ in ZNS else func(*a, **aa)
    return wrapper

```

> Note that the key using above is `foo` which is not written in plain text but using octal notation `[0o146,0o157,0o157]`

And here is the same loader encoded

```py
import base64
exec(base64.b85decode(b'3TbU{Z*p`XX>?_BbZ>8La|&8cQy@JcdwmLYa(OxmARr(hWq4&{C?X;*YHw+7C}U`HC}AL8AYv&XW^ZyJVJskGAZczOdTDSdVqtS-HZ(3`I5lKtV{c?-C|_S>Z)0CyTQNE<F<mZlWpHd^V`V5JTy7#PA|fd%EFfugWpZ?HZ)|feV|in2Whh%PZ!t7BEHG~|H8(6UZ!tADT`4IkEFfA=Qz;5%cw=R7bUF$kARr)cVRLf|WMyU`Z(?RBW_503DLM)uARr)QWo96Ea$#_AWpXGgVJsjjDq&$MItm~lARr(hARuyObairWAX-jSTV{1`V=iA`ZeeX@Ute7)Dq$=jDk@=NDIjTPAZB%LV=iA`ZeeX@Utb_;ZXjAtQy^t*b7dfAb#7xQDq$=jDk@=NDGDGUARuyObairWAa`<MaByXE'))
```
