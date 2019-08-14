import argparse
import logging
import subprocess
import os

from test.integration_tests.test_case import IntegrationTestCase, IntegrationTestType
from test.integration_tests.config import *

logging.basicConfig(level=logging.getLevelName(os.environ.get("TESTS_LOGLEVEL", "INFO")))


def test_is_running():
    cmd = ["systemctl", "is-system-running", "--wait"]
    logging.info(f"Running: {cmd}")
    systemctl = subprocess.run(cmd, capture_output=True)
    logging.info(f"systemctl ruternud: code={systemctl.returncode}, stdout={systemctl.stdout.decode()}")
    assert systemctl.returncode == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run integration tests')
    parser.add_argument('--list', dest='list', action='store_true', help='list test cases')
    parser.add_argument('--case', dest='specific_case', metavar='TEST_CASE', help='run single test case')
    args = parser.parse_args()

    logging.info(f"Using {OBJECTS} for objects storage.")
    logging.info(f"Using {OUTPUT_DIR} for output images storage.")
    logging.info(f"Using {OSBUILD} for building images.")

    boot = IntegrationTestCase(
        name="boot",
        pipeline="base.json",
        output_image="base.qcow2",
        test_cases=[test_is_running],
        type=IntegrationTestType.BOOT_WITH_QEMU
    )

    cases = [boot]

    if args.list:
        print("Available test cases:")
        for case in cases:
            print(f" - {case.name}")
    else:
        if not args.specific_case:
            for case in cases:
                case.run()
        else:
            for case in cases:
                if case.name == args.specific_case:
                    case.run()
