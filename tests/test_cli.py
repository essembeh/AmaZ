import os
import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from amaz import cli

SRC = Path(__file__).parent.parent / "samples" / "clean.py"
assert SRC.exists()


def exec_assert(pyfile: Path, env: dict = None):
    if env:
        env.update(os.environ)
    return subprocess.run(
        shlex.split(
            f"python3 -c 'import {pyfile.stem} as m; assert m.my_function(1,2,3) == 48'",
        ),
        cwd=str(pyfile.parent),
        env=env,
        check=False,
    ).returncode


def test_gen():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        output.unlink()
        assert not output.exists()
        cli.run(shlex.split(f"-i {SRC}"))
        assert not output.exists()
        cli.run(shlex.split(f"-i {SRC} -o {output}"))
        assert output.exists()
        with pytest.raises(ValueError):
            cli.run(shlex.split(f"-i {SRC} -o {output}"))


def test_ast_tweak():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        cli.run(shlex.split(f"-i {SRC} -o {output} -a -f"))
        assert exec_assert(output) == 0


def test_encoding():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        prev_size = 0
        for enc in ("b85", "b64", "b32", "b16"):
            cli.run(shlex.split(f"-i {SRC} -o {output} -s {enc} -f"))
            assert output.stat().st_size > prev_size
            prev_size = output.stat().st_size
            assert exec_assert(output) == 0


def test_loader_encoding():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        prev_size = 0
        for enc in ("none", "b85", "b64", "b32", "b16"):
            cli.run(shlex.split(f"-i {SRC} -o {output} -l {enc} -f"))
            assert output.stat().st_size > prev_size
            prev_size = output.stat().st_size
            assert exec_assert(output) == 0


def test_nokey():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        cli.run(shlex.split(f"-i {SRC} -o {output} -f"))
        assert exec_assert(output) == 0


def test_key():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        cli.run(shlex.split(f"-i {SRC} -o {output} -f -k foo"))
        assert exec_assert(output) == 0


def test_bom():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        cli.run(shlex.split(f"-i {SRC} -o {output} -f --bom"))
        assert exec_assert(output) == 0
        assert output.open("rb").read(3) == b"\xef\xbb\xbf"

        cli.run(shlex.split(f"-i {SRC} -o {output} -f"))
        assert exec_assert(output) == 0
        assert output.open("rb").read(3) != b"\xef\xbb\xbf"


def test_env():
    with NamedTemporaryFile(suffix=".py") as tmp:
        output = Path(tmp.name)
        cli.run(shlex.split(f"-i {SRC} -o {output} -f -e FOO=BAR"))
        assert exec_assert(output, env={"FOO": "bar"}) != 0
        assert exec_assert(output, env={"FOO": "BAR"}) == 0
