#!/usr/bin/env python

# stdlib
import time
import sys
import Queue
import threading
import optparse
import subprocess

# internal
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
            "-j", "--num-jobs", nargs = 1, default = 3,
            help =
                "The number of organisms to process concurrently. Default: "
                "%default"
        ),
        make_option(
            "--chunk-size", nargs = 1, default = 200000,
            help =
                "The chunk size to use when processing large organisms. "
                "Default: %default"
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

    # Read the entire query file into memory
    with query_file as f:
        query_sequence = f.read()

    # This will store organisms where the key is the organism's similarity
    # score and the value is a tuple
    # (name, reference_alignment, query_alignment, score) which is appropriate
    # to pass directly to the output.write_result function.
    pq = priorityqueue.PriorityQueue()

    # The thread-safe queue the workers will pull their jobs from
    job_queue = Queue.Queue(maxsize = 1)

    # The thread-safe queue the workers will put their results into
    results_queue = Queue.Queue()

    def worker_main():
        """The main function of each worker thread."""

        try:
            while True:
                organism = job_queue.get()
                if organism is None:
                    job_queue.task_done()
                    return

                # Figure out this organism's score
                result = similarity.score(organism.sequence, query_sequence,
                    chunk_size = options.chunk_size)
                log.debug("Organism '%s' has score %s.", organism.description,
                    result[0])

                if options.print_alignment:
                    results_queue.put((organism, result))
                else:
                    results_queue.put((organism, (result[0], None, None)))
                job_queue.task_done()
        except:
            log.debug("Shutting down prematurely.")
            raise

    def add_result(organism, result):
        """Adds a result to the priority queue. Not thread safe."""

        score, reference_alignment, query_alignment = result

        if len(pq) < int(options.num_results):
            pq.push(score, (organism.description, reference_alignment,
                query_alignment, score))
        elif pq.top().key < score:
            pq.pop()
            pq.push(score, (organism.description, reference_alignment,
                query_alignment, score))

    # Start up the threads
    workers = [threading.Thread(target = worker_main) for i in
        xrange(int(options.num_jobs))]
    for i in workers:
        i.daemon = True
        i.start()

    # We're going to keep adding jobs to the job queue until we run out of jobs
    # after which we'll wait for all the results to come in and then carry on.
    db = iter(database.load_database(database_file))
    while True:
        try:
            cur_organism = next(db)
        except StopIteration:
            break

        while True:
            try:
                job_queue.put(cur_organism, timeout = 1)
                break
            except Queue.Full:
                pass

        try:
            while not results_queue.empty():
                add_result(*results_queue.get(block = False))
        except Queue.Empty:
            pass

    # Shut down all the workers
    for i in xrange(len(workers)):
        job_queue.put(None)
    while [i for i in workers if i.is_alive()]:
        time.sleep(1)

    # Grab all the results
    while not results_queue.empty():
        add_result(*results_queue.get(block = False))

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
