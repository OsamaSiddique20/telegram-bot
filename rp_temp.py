import subprocess

# Define the sudo password (replace 'your_password' with the actual password)
def getTemp():
    sudo_password = 'O$ama@3099'

    # Run the 'sudo vcgencmd measure_temp' command with password automation
    command = 'sudo -S vcgencmd measure_temp'
    try:
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=sudo_password + '\n')
        
        if process.returncode == 0:
            print("Temperature:", stdout.strip())
        else:
            print("Error:", stderr.strip())
    except Exception as e:
        print("Exception:", str(e))
    return str(stdout.strip())
