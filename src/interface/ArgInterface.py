import sys
import argparse
from datetime import datetime

from src.logger import logger
from src.logger import Severity


class ArgInterface:
    def query_with_args(self, ctran, args):
        try:
            args = self._parse_cl_args(args)
            return ctran.query_date_range(args.date_start, args.date_end)
        except Exception:
            return None

    def _service_date(self, arg):
        try:
            return datetime.strptime(arg, "%Y-%m-%d")
        except ValueError:
            err_msg = "Invalid service date format: {0}, YYYY-MM-DD expected.".format(arg)
            # TODO uncomment when ready to enable logging output
            # logger.log(err_msg, Severity.ERROR)
            raise argparse.ArgumentTypeError(err_msg)

    def _parse_cl_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--date-start",
                            help="Format: --date-start=YYYY-MM-DD (ex. 2020-01-01)",
                            required=True,
                            type=self._service_date)
        parser.add_argument("--date-end",
                            help="Format: --date-end=YYYY-MM-DD (ex. 2020-01-01)",
                            required=True,
                            type=self._service_date)
        return parser.parse_args(args)
