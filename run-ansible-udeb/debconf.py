from __future__ import absolute_import, division, print_function

import os
import ansible.utils.display 
from ansible.plugins.callback import CallbackBase

display = ansible.utils.display.Display()

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'shrug'
    CALLBACK_NAME = 'debconf'

    def __init__(self):
        conn = None

        if "DEBCONF_REDIR" in os.environ:
            try:
                conn = os.fdopen(3, 'w')
            except:
                display.vvvv("failed to fdopen debconf fd")
            else:
                display.vvvv("opened debconf fd")
        else:
            display.vvvv("debconf callbacks disabled as DEBCONF_REDIR unset")

        self._debconf_connection = conn
            
        # Might confuse child processes
        for env in ["DEBCONF_OLD_FD_BASE", "DEBCONF_REDIR", 
                    "DEBIAN_FRONTEND", "DEBIAN_HAS_FRONTEND"]:
            try:
                del os.environ[env]
            except:
                pass

        super(CallbackModule, self).__init__()

    def _thing_start(self, thing_type, thing):
        thing_name = " ".join(thing.get_name().strip().split())
        template = "run-ansible/progress/info/running"

        conn = self._debconf_connection

        if conn is not None:
            conn.write("SUBST {} THINGTYPE {}\n".format(template, thing_type))
            conn.write("SUBST {} THINGNAME {}\n".format(template, thing_name))
            conn.write("PROGRESS INFO {}\n".format(template))
            conn.flush()

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._thing_start("task", task)

    def v2_playbook_on_cleanup_task_start(self, task):
        self._thing_start("cleanup-task", task)

    def v2_playbook_on_handler_task_start(self, task):
        self._thing_start("handler", task)

    def v2_playbook_on_play_start(self, play):
        self._thing_start("play", play)
