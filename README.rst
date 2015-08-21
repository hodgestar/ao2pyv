ao2pyv
======

Converts Archive.org video searches into PyVideo.org API submissions.

Installation
------------

Just `pip install ao2pyv`.

Usage
-----

Usage: ao2pyv [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --version            Show the version and exit.
  -q, --query TEXT     Archive.org search query
  -c, --category TEXT  Pyvideo category
  -l, --language TEXT  Pyvideo language
  --help               Show this message and exit.

Commands:
  sink.json           Output results to a file.
  source.archive-org  Search archive.org for a query and return a...
  source.json         Return results from a JSON file.
  transform.ao2pyv    Transform a video result from archive.org to...
  transform.none      Transform a video result not at all.
