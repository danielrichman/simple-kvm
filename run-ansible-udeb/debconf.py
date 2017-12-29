from __future__ import absolute_import, division, print_function

import os
import atexit
from ansible.plugins.callback import CallbackBase

RUNNING_TEMPLATE = "run-ansible/progress/info/running"

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'shrug'
    CALLBACK_NAME = 'debconf'

    def __init__(self):
        self._enabled = False
        self._progress_started = False
        # This is nasty:
        atexit.register(self._stop_progress_if_started)

        super(CallbackModule, self).__init__()

        if "DEBCONF_REDIR" in os.environ:
            try:
                self._debconf_in  = os.fdopen(os.dup(0), 'r')
                self._debconf_out = os.fdopen(3, 'w')
            except:
                self._display.vvvv("failed to fdopen debconf fd")
            else:
                self._enabled = True
                self._display.vvvv("opened debconf fd")
        else:
            self._display.vvvv("debconf callbacks disabled as DEBCONF_REDIR unset")

        # Might confuse child processes
        for env in ["DEBCONF_OLD_FD_BASE", "DEBCONF_REDIR", 
                    "DEBIAN_FRONTEND", "DEBIAN_HAS_FRONTEND"]:
            try:
                del os.environ[env]
            except:
                pass
    
    def _communicate(self, line):
        if self._enabled:
            self._display.vvvv("debconf_out: {}".format(line))
            self._debconf_out.write(line + "\n")
            self._debconf_out.flush()
            reply = self._debconf_in.readline()
            self._display.vvvv("debconf_in: {}".format(reply))
        else:
            self._display.vvvv("debconf disabled: {}".format(line))

    def _subst(self, thing_type, thing):
        thing_name = " ".join(thing.get_name().strip().split())
        self._communicate("SUBST {} THINGTYPE {}".format(RUNNING_TEMPLATE, thing_type))
        self._communicate("SUBST {} THINGNAME {}".format(RUNNING_TEMPLATE, thing_name))

    def _start_progress(self, thing_type_for_title, thing_for_title, total):
        self._progress_current = 0
        self._progress_total = total
        self._subst(thing_type_for_title, thing_for_title)
        self._communicate("PROGRESS START 0 {} {}".format(total, RUNNING_TEMPLATE))
        self._progress_started = True

    def _set_progress_info(self, thing_type, thing):
        self._subst(thing_type, thing)
        self._communicate("PROGRESS INFO {}".format(RUNNING_TEMPLATE))

    def _step_progress_bar(self):
        if self._progress_current < self._progress_total:
            self._progress_current += 1
            self._communicate("PROGRESS SET {}".format(self._progress_current))

    def _stop_progress_if_started(self):
        if self._progress_started:
            self._communicate("PROGRESS STOP")
            self._progress_started = False

    def v2_playbook_on_play_start(self, play):
        # This is an approximation, because of conditional tasks; rescue/always, etc.
        # It works well enough.
        def count_tasks(things):
            res = 0

            for thing in things:
                did_recurse = False

                for recursion in ("block", "always"):
                    inner = getattr(thing, recursion, None)
                    if inner:
                        res += count_tasks(inner)
                        did_recurse = True

                if not did_recurse:
                    res += 1

            return res

        self._stop_progress_if_started()
        self._start_progress("play", play, count_tasks(play.compile()))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._set_progress_info("task", task)
        self._step_progress_bar()

    def v2_playbook_on_cleanup_task_start(self, task):
        self._set_progress_info("cleanup-task", task)

    def v2_playbook_on_handler_task_start(self, task):
        self._set_progress_info("handler", task)
