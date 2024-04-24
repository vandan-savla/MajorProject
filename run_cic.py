import subprocess
import os
import sys
import time

class CicflowmeterService:
    def __init__(self, interface):
        self.interface = interface
        self.process = None

    def start(self):
        if self.process is None or self.process.poll() is not None:
            self.process = self._run_cicflowmeter()
            print("cicflowmeter process started in the background.")
        else:
            print("cicflowmeter process is already running.")

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            print("cicflowmeter process stopped.")
        else:
            print("No cicflowmeter process is currently running.")

    def restart(self):
        self.stop()
        self.start()

    def _run_cicflowmeter(self):
        try:
            # Construct the command
            command = ["sudo", "cicflowmeter", "-i", self.interface, "-c", "--dir", "output_flows/"]

            # Open the process in the background and detach it
            with open(os.devnull, 'w') as devnull:
                return subprocess.Popen(command, stdout=devnull, stderr=devnull, stdin=devnull, preexec_fn=os.setsid)
        except FileNotFoundError:
            print("Error: cicflowmeter command not found. Make sure it is installed and in your system PATH.")
            return None

def print_usage():
    print("Usage: python script_name.py <interface> <start|stop|restart>")
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print_usage()

    interface = sys.argv[1]
    action = sys.argv[2].lower()
    
    if action not in ['start', 'stop', 'restart']:
        print("Error: Invalid action.")
        print_usage()

    service = CicflowmeterService(interface)

    if action == 'start':
        service.start()
    elif action == 'stop':
        service.stop()
    elif action == 'restart':
        service.restart()

if __name__ == "__main__":
    main()
