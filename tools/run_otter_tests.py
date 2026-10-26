"""Locally replay the otter-grader tests that a notebook carries in its metadata.

Assignments from this course ship as otter notebooks: every `grader.check("qX")` test
lives verbatim in `notebook["metadata"]["otter"]["tests"]`, so the exact pass criteria
can be read out (`--dump`) and replayed against the notebook's own code cells (default)
without having otter-grader installed locally.

Usage:
    python tools/run_otter_tests.py NOTEBOOK.ipynb                  # run every embedded test
    python tools/run_otter_tests.py NOTEBOOK.ipynb --list           # test names + point values
    python tools/run_otter_tests.py NOTEBOOK.ipynb --dump           # print the tests (pass criteria)
    python tools/run_otter_tests.py NOTEBOOK.ipynb --only q1,q2
    python tools/run_otter_tests.py NOTEBOOK.ipynb --skip-substr 'poly_multiply_naive(poly1'

Exit status is 0 only when every test that ran passed.
"""
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
import time as _time
import traceback

import matplotlib

matplotlib.use("Agg")  # notebooks plot; keep it headless and non-blocking

# Cells that need otter itself (or a Jupyter shell) cannot run as plain Python. Their
# non-otter content (the import block, rng_seed, ...) is re-created by PRELUDE below.
SKIP_MARKERS = ("!pip", "!conda", "import otter", "grader.", "%matplotlib")

PRELUDE = """\
import numpy as np
from numpy.random import randint
from time import time
import heapq
import pickle
import tqdm
import scipy
import math
import matplotlib.pyplot as plt
import numpy.random as random
import networkx as nx
"""


def load_notebook(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def embedded_tests(nb):
    return nb.get("metadata", {}).get("otter", {}).get("tests", {})


def test_points(src):
    for line in src.splitlines():
        if line.startswith("points"):
            return line.split("=", 1)[1].strip()
    return "?"


def without_otter(src):
    """Drop the otter import and the @test_case decorator so the test runs standalone."""
    kept = [
        line
        for line in src.splitlines()
        if not line.startswith("from otter.test_files import")
        and not line.startswith("@test_case")
    ]
    return "\n".join(kept)


def build_namespace(path, nb, skip_substr=()):
    """Exec the notebook's code cells top to bottom, minus the otter/pip ones."""
    ns = {"__name__": "__main__"}
    exec(compile(PRELUDE, "<prelude>", "exec"), ns)
    ran, skipped = [], []
    # otter executes notebooks with the notebook's folder as the working directory;
    # do the same so cells that open relative data files (e.g. generated_testcases.pkl) work.
    previous_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(path)))
    try:
        for i, cell in enumerate(nb["cells"]):
            if cell.get("cell_type") != "code":
                continue
            src = "".join(cell.get("source", []))
            if any(m in src for m in SKIP_MARKERS) or any(m in src for m in skip_substr):
                skipped.append(i)
                continue
            exec(compile(src, f"{path}:cell{i}", "exec"), ns)
            ran.append(i)
    finally:
        os.chdir(previous_cwd)
    if "rng_seed" not in ns:
        ns["rng_seed"] = 0
    return ns, ran, skipped


def run_tests(path, only=None, skip_substr=(), verbose=True):
    nb = load_notebook(path)
    tests = embedded_tests(nb)
    if not tests:
        raise SystemExit(f"{path}: no embedded otter tests found in metadata")

    ns, ran, skipped = build_namespace(path, nb, skip_substr)
    if verbose:
        print(f"{path}: ran code cells {ran}")
        print(f"{path}: skipped code cells {skipped}")

    results = {}
    for name, src in tests.items():
        if only and name not in only:
            continue
        tns = {}
        exec(compile(without_otter(src), f"<test {name}>", "exec"), tns)
        fn = next(v for k, v in tns.items() if k.startswith("test_"))
        kwargs = {}
        for param in inspect.signature(fn).parameters:
            if param in ns:
                kwargs[param] = ns[param]
            elif param in tns:
                kwargs[param] = tns[param]
            else:
                raise SystemExit(
                    f"test {name} needs {param!r}, which the notebook never defines "
                    f"(is the cell defining it being skipped?)"
                )
        if verbose:
            print(f"\n===== {path} :: {name} =====")
        start = _time.time()
        try:
            fn(**kwargs)
            status = "PASS"
        except Exception as e:  # noqa: BLE001 - report whatever the test threw
            status = f"FAIL: {type(e).__name__}: {str(e)[:500]}"
            if verbose:
                traceback.print_exc()
        results[name] = status
        if verbose:
            print(f"----- {name}: {status} ({_time.time() - start:.2f}s)")
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notebooks", nargs="+", help="path(s) to .ipynb file(s)")
    ap.add_argument("--list", action="store_true", help="list test names and point values, then exit")
    ap.add_argument("--dump", action="store_true", help="print the embedded test sources, then exit")
    ap.add_argument("--only", help="comma separated list of test names to run")
    ap.add_argument(
        "--skip-substr",
        action="append",
        default=[],
        help="skip any code cell containing this substring (repeatable; use for slow cells)",
    )
    args = ap.parse_args(argv)

    only = args.only.split(",") if args.only else None
    all_results = {}
    for path in args.notebooks:
        if args.list or args.dump:
            for name, src in embedded_tests(load_notebook(path)).items():
                if args.dump:
                    print(f"{'#' * 30} {path} :: {name} (points = {test_points(src)})")
                    print(src)
                else:
                    print(f"{path} :: {name}: {test_points(src)} points")
            continue
        print(f"\n########## {path} ##########")
        for name, status in run_tests(path, only=only, skip_substr=args.skip_substr).items():
            all_results[f"{path}::{name}"] = status

    if args.list or args.dump:
        return 0

    print("\n=========== SUMMARY ===========")
    for key, status in all_results.items():
        print(f"  {key}: {status}")
    failed = [k for k, v in all_results.items() if v != "PASS"]
    print(f"{len(all_results) - len(failed)}/{len(all_results)} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
