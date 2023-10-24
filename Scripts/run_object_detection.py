import subprocess



#os.chdir("Scripts")
# Specify the command you want to run
command = "python3.8 detectnet.py /dev/video0"

# Run the command in the terminal
try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Command output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
