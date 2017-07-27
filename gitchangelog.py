#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# changelog git hook
#
# Copyright (c) 2015 by Georg Brandl.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""read default commit message from changelog

Usage: use as prepare-commit-msg hook in git, set the changelog file name with

    git config [--global] hooks.changelogfile CHANGELOG

(Default name is CHANGES).

Then, committing without a given message or logfile will check if the changelog
is included in the commit.  If it is, the commit message shown in the editor
will default to all text added to the changelog.
"""

import os
import re
import sys


CONFIG = 'hooks.changelogfile'
DEFAULT = 'CHANGES'

WARNING_CONFIG = 'hooks.changelogwarning'
WARNING_DEFAULT = ('#===================================\n'
                   '# WARNING: No changelog entry found!\n'
                   '#===================================')

_bullet_re = re.compile(r'\s*[-+*]\s+')


def normalize_log(lines):
    """Outdents newly inserted list items."""
    last_indention = 0
    for idx, line in enumerate(lines):
        match = _bullet_re.match(line)
        if match is not None:
            last_indention = match.end()
            lines[idx] = line[last_indention:]
        elif last_indention:
            if not line[:last_indention].strip():
                lines[idx] = line[last_indention:]
    return '\n'.join(lines)


def main():
    msgfile = sys.argv[1]
    msglines = []
    with open(msgfile) as fp:
        for line in fp:
            if line.strip() and not line.startswith('#'):
                # do nothing if msg already has a nontrivial message
                return
            msglines.append(line)

    logname = os.popen('git config ' + CONFIG).read().strip() or DEFAULT
    diff = os.popen('git diff --color=never --staged -- ' + logname).readlines()
    log = []
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            log.append(line[1:].rstrip().expandtabs())
    log = normalize_log(log)
    if not log:
        warning = (os.popen('git config ' + WARNING_CONFIG).read().strip()
                   or WARNING_DEFAULT)
        log = warning
    with open(msgfile, 'w') as fp:
        fp.write(log)
        fp.write('\n')
        fp.write(''.join(msglines))


if __name__ == '__main__':
    main()
