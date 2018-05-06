import threading

class robot_thread(threading.Thread):
    def __init__(self, tactic_instance, state, publisher, **kwargs):
        threading.Thread.__init__(self)
        self.instance = tactic_instance
        self.state = state
        self.publisher = publisher

    def run(self):
        self.instance.execute(self.state, self.publisher)
