# :warning: ERROR MESSAGES

Here is a non-exhaustive list of error messages that you may encounter in the case of a bad configuration, their meaning and how to fix the error related to.

&#160;

MESSAGE | MEANING | HOW TO FIX IT
--------|---------|--------------|
*sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper* | www-data is not allowed to run some bash commands used in python files without providing any password | check if `NOPASSWD` is correctly filled in your `sudoers` |

&#160;
