import queue

class TaskQueue:
    def __init__(self, maxsize=0):
        # Using Python's built-in queue module.
        # maxsize=0 means infinite size
        self._tasks = queue.Queue(maxsize)

    def add_task(self, task):
        """Adds a task to the queue."""
        try:
            self._tasks.put_nowait(task)
            return True
        except queue.Full:
            print("Task queue is full.")
            return False

    def get_task(self):
        """Retrieves a task from the queue. Returns None if no tasks are available."""
        try:
            return self._tasks.get_nowait()
        except queue.Empty:
            return None

    def has_tasks(self):
        """Checks if there are tasks remaining in the queue."""
        return not self._tasks.empty()

    def size(self):
        """Returns the number of tasks in the queue."""
        return self._tasks.qsize()

# Example usage
if __name__ == "__main__":
    tq = TaskManagementAgent()

    # Adding some tasks
    tq.add_task({"type": "navigate", "destination": "room_101"})
    tq.add_task({"type": "interact", "message": "Hello, guest!"})

    # Processing tasks
    while tq.has_tasks():
        task = tq.get_task()
        print(f"Processing task: {task['type']} with data {task}")
