import threading
from navigation_agent.navigation_agent import NavigationAgent

def main():
    # Initialize agents
#    task_agent = TaskManagementAgent()
#    vision_agent = VisionAgent()
    print("Initializing Navigation Agent")
    navigation_agent = NavigationAgent()

    # Assuming each agent has a 'run' method which starts its main loop/process.
    # We'll use Python threads to run each agent in parallel for simplicity.
    # Depending on the application, you might opt for processes or even distributed setups.
    
    agent_threads = [
#        threading.Thread(target=task_agent.run, name="TaskManagementAgent"),
#        threading.Thread(target=task_agent.run, name="VisionAgent"),
        threading.Thread(target=navigation_agent.run, name="NavigationAgent"),

    ]

    # Start all agent threads
    for thread in agent_threads:
        thread.start()

    # Optionally, wait for all threads to complete. In a real-world scenario,
    # you might have a supervisory loop here that monitors the health of agents,
    # responds to system signals, or performs other top-level tasks.
    for thread in agent_threads:
        thread.join()

if __name__ == "__main__":
    main()
