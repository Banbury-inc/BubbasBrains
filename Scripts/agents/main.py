import threading
import sys
from navigation_agent.navigation_agent import NavigationAgent
from task_management_agent.task_management_agent import TaskManagementAgent
from vision_agent.vision_agent import VisionAgent
from communication_agent.communication_agent import CommunicationAgent
from health_agent.health_agent import HealthAgent




def main():
    # Initialize agents
#    task_agent = TaskManagementAgent()
#    vision_agent = VisionAgent()
    print("Initializing Communication Agent")
    communication_agent = CommunicationAgent()
    print("Initializing Server")
    server = CommunicationAgent.run_server()
    print("Initializing Task Management Agent")
    task_management_agent = TaskManagementAgent()
    print("Initializing Navigation Agent")
    navigation_agent = NavigationAgent()
    print("Initializing Vision Agent")
    vision_agent = VisionAgent()
    print("Initializing Object Detection")
    object_detection = VisionAgent.objectDetection()
    print("Initializing Health Agent")
    health_agent = HealthAgent()

   # Assuming each agent has a 'run' method which starts its main loop/process.
    # We'll use Python threads to run each agent in parallel for simplicity.
    # Depending on the application, you might opt for processes or even distributed setups.
 
    agent_threads = [
        threading.Thread(target=communication_agent.run, name="CommunicationAgent"),
        threading.Thread(target=communication_agent.run_server, name="Server"),
        threading.Thread(target=task_management_agent.run, name="TaskManagementAgent"),
        threading.Thread(target=vision_agent.run, name="VisionAgent"),
        threading.Thread(target=navigation_agent.run, name="NavigationAgent"),
        threading.Thread(target=health_agent.run, name="HealthAgent"),
        threading.Thread(VisionAgent.objectDetection, name="Objectdetection"),
    ]
    # Redirect or suppress output for the VisionAgent thread
    for thread in agent_threads:
        if thread.name == "ObjectDetection":
            thread.daemon = True  # Mark the thread as a daemon to prevent it from blocking program exit
            # Redirect the output to a custom stream (suppress output)
            sys.stdout = NullOutput()

    # Start all agent threads
    for thread in agent_threads:
        thread.start()

    # Optionally, wait for all threads to complete. In a real-world scenario,
    # you might have a supervisory loop here that monitors the health of agents,
    # responds to system signals, or performs other top-level tasks.
    for thread in agent_threads:
        thread.join()

    # Restore the original sys.stdout
    sys.stdout = sys.__stdout__

# Create a custom stream for suppressing output
class NullOutput:
    def write(self, text):
        pass



if __name__ == "__main__":
    main()
