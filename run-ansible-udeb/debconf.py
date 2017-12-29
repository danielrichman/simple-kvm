from __future__ import absolute_import, division, print_function

import os
from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'shrug'
    CALLBACK_NAME = 'debconf'

    def __init__(self):
        self._enabled = False

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

    def _thing_start(self, thing_type, thing):
        thing_name = " ".join(thing.get_name().strip().split())
        template = "run-ansible/progress/info/running"

        self._communicate("SUBST {} THINGTYPE {}".format(template, thing_type))
        self._communicate("SUBST {} THINGNAME {}".format(template, thing_name))
        self._communicate("PROGRESS INFO {}".format(template))

    def _set_progress(self):
        num = self._progress_current
        denom = self._progress_total

        self._display.vvvv("progress bar: {}/{}".format(num, denom))

        p = (num * 100) // denom
        p = min(p, 100)

        self._communicate("PROGRESS SET {}".format(p))

    def v2_playbook_on_play_start(self, play):
        self._thing_start("play", play)
        self._progress_current = 0
        self._progress_total = len(play.tasks())
        self._set_progress()

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._thing_start("task", task)
        self._progress_current += 1
        self._set_progress()

    def v2_playbook_on_cleanup_task_start(self, task):
        self._thing_start("cleanup-task", task)

    def v2_playbook_on_handler_task_start(self, task):
        self._thing_start("handler", task)
