#!/usr/bin/env python

# stdlib
import sys
import optparse
import subprocess

# internal
from . import scorefunc
from . import output
from . import similarity
from . import database
from . import priorityqueue

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
            "--no-colors", action = "store_true", default = False,
            help =
                "If this flag is present, colors will not be used when "
                "printing the alignment."
        ),
        make_option(
            "--score-file", default = None,
            help =
                "The file to generate the subsitution matrix and gap penalty "
                "function with."
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

    if len(args) != 2:
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

    # Open up the database
    database_path = args[0]
    try:
        database_file = open(database_path, "r")
    except IOError:
        log.exception("Could not load database file.")
        return 2

    # Open up the query file
    query_path = args[1]
    try:
        query_file = open(query_path, "r")
    except IOError:
        log.exception("Could not load query file.")
        return 2

    # Load the score file
    if options.score_file is None:
        sub_score, gap_score = scorefunc.make_score_functions(None)
    else:
        with open(options.score_file, "r") as f:
            sub_score, gap_score = scorefunc.make_score_functions(f)

    # Read the entire query file into memory
    with query_file as f:
        query_sequence = f.read()

    # This will store organisms where the key is the organism's similarity
    # score and the value is a tuple
    # (name, reference_alignment, query_alignment, score) which is appropriate
    # to pass directly to the output.write_result function.
    pq = priorityqueue.PriorityQueue()

    # Go through every item in the database and create a similarity score for
    # each. Note I don't want to close the database after this call returns
    # because it's a generator.
    db = database.load_database(database_file)
    for i, organism in enumerate(db):
        # Figure out this organism's score
        score, reference_alignment, query_alignment = \
            similarity.score(organism.sequence, query_sequence, sub_score,
                gap_score)

        log.debug("Organism '%s' has score %s.", organism.description, score)

        if len(pq) < int(options.num_results):
            pq.push(score, (organism.description, reference_alignment,
                query_alignment, score))
        elif pq.top().key < score:
            pq.pop()
            pq.push(score, (organism.description, reference_alignment,
                query_alignment, score))

    # The priority queue will return the list of organisms in ascending order,
    # we want to reverse this.
    result = []
    while pq:
        result.append(pq.pop().value)
    result.reverse()

    # Figure out the width of the terminal
    try:
        process = subprocess.Popen(["stty", "size"], stdout = subprocess.PIPE)
        process.wait()

        if process.returncode == 0:
            console_width = int(process.stdout.read().split()[1])
        else:
            log.warning("stty failed. Using default console width of 72.")
            console_width = 72
    except OSError:
        log.warning("stty program not found. Using default console width of "
            "72.")
        console_width = 72

    # Print out the results
    for i in result:
        output.write_result(
            *i,
            use_colors = not options.no_colors,
            console_width = console_width,
            show_alignment = options.print_alignment)
        print

    return 0
