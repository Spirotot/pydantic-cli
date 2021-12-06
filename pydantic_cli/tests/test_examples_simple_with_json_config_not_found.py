from . import _TestHarness, HarnessConfig

from pydantic_cli.examples.simple_with_json_config_not_found import (
    Options,
    example_runner,
)


class TestExamples(_TestHarness[Options]):

    CONFIG = HarnessConfig(Options, example_runner)

    def test_simple_01(self):
        with self.assertWarnsRegex(
            UserWarning, f"Unable to find {Options.Config.CLI_JSON_CONFIG_PATH}"
        ):
            self.run_config(
                ["--input_file", "/path/to/file.txt", "--max_record", "1234"]
            )

    def test_simple_02(self):
        bad_path_file = "/bad/path/file.json"
        with self.assertWarnsRegex(UserWarning, f"Unable to find {bad_path_file}"):
            self.run_config(
                [
                    "--input_file",
                    "/path/to/file.txt",
                    "--max_record",
                    "1234",
                    "--json-config",
                    bad_path_file,
                ]
            )
