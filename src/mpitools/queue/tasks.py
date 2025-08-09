class Task:
    """
    Abstract representation of a task in the queue.
    """
    ...

class EndTask(Task):
    """
    Special task to signal the end of the queue.
    """
    def __init__(self):
        pass
    
    