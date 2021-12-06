import sys
import unittest
from . import _TestHarness, HarnessConfig

import json
from tempfile import NamedTemporaryFile
from pydantic_cli.examples.simple_with_json_config import Opts, runner

try:
    import yaml
except ModuleNotFoundError:
    pass


class TestExample(_TestHarness[Opts]):

    CONFIG = HarnessConfig(Opts, runner)

    opt = Opts(
        hdf_file="/path/to/file.hdf5",
        max_records=12,
        min_filter_score=1.024,
        alpha=1.234,
        beta=9.854,
    )

    def _util_json(self, d, more_args):
        with NamedTemporaryFile(mode="w", delete=True) as f:
            json.dump(d, f)
            f.flush()
            f.name
            args = ["--json-training", str(f.name)] + more_args
            self.run_config(args)

    def _util_yaml(self, d, more_args):
        with NamedTemporaryFile(mode="w", delete=True) as f:
            yaml.dump(d, f, yaml.Dumper)
            f.flush()
            f.name
            args = ["--json-training", str(f.name)] + more_args
            self.run_config(args)

    def test_simple_json(self):
        self._util_json(self.opt.dict(), [])

    def test_simple_partial_json(self):
        d = dict(max_records=12, min_filter_score=1.024, alpha=1.234, beta=9.854)

        self._util_json(d, ["--hdf_file", "/path/to/file.hdf5"])

    @unittest.skipIf("yaml" not in sys.modules, "yaml not installed")
    def test_simple_yaml(self):
        self._util_yaml(self.opt.dict(), [])

    @unittest.skipIf("yaml" not in sys.modules, "yaml not installed")
    def test_simple_partial_yaml(self):
        d = dict(max_records=12, min_filter_score=1.024, alpha=1.234, beta=9.854)

        self._util_yaml(d, ["--hdf_file", "/path/to/file.hdf5"])
