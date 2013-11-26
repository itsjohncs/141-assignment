#!/usr/bin/env python

# stdlib
import sys
import optparse

# setup logging
import logging
log = logging.getLogger("dnasearch")

def parse_arguments(args = sys.argv[1:]):
    make_option = optparse.make_option
    option_list = [
        make_option(
            "-n", "--num-results", nargs = 1, default = 10,
            help = "The number of results to print out. Default is %default."
        ),
        make_option(
            "-a", "--print-alignment", action = "store_true", default = False,
            help =
                "If this flag is present, alignment information will be "
                "print out in the results."
        ),
        make_option(
            "-v", "--verbose", action = "count", default = 0,
            help =
                "May be specified twice. If specified once, INFO messages "
                "and above are output. If specified twice, DEBUG messages and "
                "above are output. By default, only WARN messages and above "
                "are output."
        ),
        make_option(
            "-q", "--quiet", action = "store_true", default = False,
            help = "Only CRITICAL log messages will be output."
        )
    ]

    parser = optparse.OptionParser(
        usage = "usage: %prog [options] [DATABASE_FILE] [QUERY_FILE]",
        description =
            "Finds organisms that are similar to the given organism in "
            "QUERY_FILE contained in DATABSE_FILE.",
        option_list = option_list
    )

    options, args = parser.parse_args(args)

    if len(args) < 2:
        parser.error("Both a DATABASE_FILE and a QUERY_FILE must be supplied.")

    return (options, args)

def setup_logging(options, args):
    if options.verbose >= 2:
        log_level = logging.DEBUG
    elif options.verbose == 1:
        log_level = logging.INFO
    elif options.quiet:
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARN

    format = "[%(levelname)s] %(message)s"

    logging.basicConfig(level = log_level, format = format)

    log.debug("Logging initialized.")

def main(args = sys.argv[1:]):
    options, args = parse_arguments(args)
    setup_logging(options, args)

    log.debug("Contents of options: %s", repr(options))
    log.debug("Contents of args: %s", repr(args))

    return 0

if __name__ == "__main__":
    sys.exit(main())
