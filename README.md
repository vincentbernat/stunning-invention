# Language choice

This project is written in Python 3 which is great to prototype ideas
into a robust implementation without loosing too much time. If at some
point, performance becomes a problem, Go may become a better choice.
The project is not compatible with Python 2 because Python 2 is soon
EoL, Python 3 is now available in modern and not-so-modern
distributions and the gap between the two implementations is starting
to grow (notably asyncio and f-strings).

Also, Python's stdlib is complete enough for such a script to not get
additional dependencies. Notably, I am a big fan of the argparse
module which is lacking in many other languages (Go flag package is
quite limited and third-party packages like urfave/cli or spf13/cobra
do not match the quality of argparse, IMO).

# Architecture

This is a single-file script which makes sense for a small tool. This
allows a user without any knowledge to easily "deploy" the program by
just copying the script to the target host. The documentation is
embedded into the script and available through `--help`. Only tests
are kept apart as most users won't need them.

Using a single-file script implies to try to keep the code concise to
keep everything readable. Notably, this means some patterns are
avoided. For example, a log line is parsed into a dictionary, not a
dedicated object. As long as the attached behaviors are trivial, I
don't see this as a weakness.

The script relies on coroutines to make the work. As we control when
we schedule coroutines, we don't need locks when manipulating some
data structures.

# Tests

You can run tests with `pytest` (or `pytest-3`). [pytest-asyncio][] is
needed to run the tests. The tests do not cover everything (I don't
think that would be useful).

[pytest-asyncio]: https://github.com/pytest-dev/pytest-asyncio

# Limitations

The date/time in log files is not used for alerting or showing the
last 10 seconds. We assume logs are pushed in the file in realtime.
This seems the best solution, because if there is a 1-minute constant
lag, the last 10 seconds could be always empty. If the lag is not
constant, the situation gets even more complex. An alternative would
be to use the log file as the only "clock". However, when there is no
log, we don't know if they are just late or non-existent.

The script is using `tail -F` because it's convenient to do so.
Spawning a process in Python is easy and reproducing its behavior is
not totally trivial (notably to follow the file when log rotation
happens).

The screen real estate is poorly used. There is a version displaying
stats on two columns (see git history), but I am unconvinced with it.
I have kept the simpler version.

# Evolution

If at some point, the code exceeds 1000 lines, it will become
difficult to keep the architecture as is. Therefore, it may be time to
split the script into multiple files, making deployment a bit more
complex for unsuspecting users, unless there is a strong culture of
using Docker containers or some kind of packaging mechanisms.

At the beginning, I thought about using an ncurses/newt interface to
be able to refresh statistics while displaying alerts on the same
screen, but this seemed unnecessary. With some additional features, it
could start to make sense (toggle between stats, going back into
history, ...).
