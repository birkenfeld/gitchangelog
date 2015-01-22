Git changelog hook
==================

This hook should be used as ``prepare-commit-msg``.  It uses the staged
diff of a pre-determined "changelog" file to pre-fill the commit message.

For example, if you add this in your changelog file prior to committing::

   - Fix #1234: prevent crash when arguments missing

the hook will take this out of the diff to be committed and pre-fill the
commit message with ::

   Fix #1234: prevent crash when arguments missing

The file to check is determined by the ``hooks.changelogfile`` config setting,
and defaults to ``CHANGES``.


This hook is copyright 2015 by Georg Brandl, and can be
distributed under the GNU GPL version 2 or later.
