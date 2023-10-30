import queue
from navigation_agent.navigation_agent import NavigationAgent
from vision_agent.vision_agent import VisionAgent
from communication_agent.communication_agent import CommunicationAgent
class TaskManagementAgent:
    running_programs = []
    def __init__(self, maxsize=0):
        # Using Python's built-in queue module.
        # maxsize=0 means infinite size
        self._tasks = queue.Queue(maxsize)
    def start_program(application_name, priority, running):
        program = {
            "Name": application_name,
            "Priority": priority,
            "Running": running
            }
        TaskManagementAgent.running_programs.append(program)
    def kill_program():
        pass
    def list_active_programs():
        return TaskManagementAgent.running_programs
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
    def log_message():
        role = "Task Management Agent"
        message = "Task Management Agent Initialized"
        CommunicationAgent.log_message(role, message)
    def manage_usage():
        print("Eliminating application with lowest priority")

    def run(self):
        print("Task Management Agent Initialized")
        role = "Task Management Agent"
        message = "Task Management Agent Initialized"
        CommunicationAgent.log_message(role, message)
# Example usage
if __name__ == "__main__":
    agent = TaskManagementAgent()

    # Adding some tasks
    agent.add_task({"type": "navigate", "destination": "room_101"})
    agent.add_task({"type": "interact", "message": "Hello, guest!"})

    # Processing tasks
    while agent.has_tasks():
        task = agent.get_task()
        print(f"Processing task: {task['type']} with data {task}")
