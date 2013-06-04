# WARNING! if you are trying to pass several args to make file then they will be started by fabric one by one:
#
# ``make autoactivate init_project`` will result in::
#
#    fab autoactivate
#    fab init_project
#
# And this will not activate env. To call them all you should do ``make "autoactivate init_project"``
#
# But simple commands like ``make test`` can still be run if you configur virtualenv settings in fabsettings.py
# or if you activate virtualenv before running ``make`` (some automated test systems activate env before calling ``make test``)
#

-include Makefile.def

%:
	fab $@
