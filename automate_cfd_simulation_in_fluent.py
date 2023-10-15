import subprocess
import os
import time

def launch_fluent_console(journal_file, log_file, pid_file):
    # Construct the Fluent command with -gu flag and redirect output/error to log file
    fluent222 = "/data/apps/ansys_inc/v222/fluent/bin/fluent"    
    fluent_command = f"{fluent222} 2ddp -gu -t 10 -i {journal_file} > {log_file} 2>&1 & echo $! > {pid_file}"
    process = subprocess.Popen(fluent_command, shell=True, preexec_fn=os.setsid)

    with open(pid_file, 'w') as pid_file:
        pid_file.write(str(process.pid))

    return process

def check_output_files(output_files):
    for file in output_files:
        if not os.path.exists(file):
            return False
    return True

def check_for_errors(log_file, error_strings):
    with open(log_file, "r") as f:
        log_content = f.read()
        for error_string in error_strings:
            if error_string in log_content:
                location = log_content.find(error_string)  # Find the location of the error string
                return error_string, location
    return None, -1  # Return None and -1 if no error is found


def terminate_fluent_process(pid):
    try:
        os.kill(pid, 15)  # Send a SIGTERM signal to the process
    except ProcessLookupError:
        # Handle the case where the process is not found
        pass

def main():
    journal_file = "airfoil_s6.jou"
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # current time stamp
    log_file = f"/data/marisha/fluent_files/log_files/log_{timestamp}.log"
    output_files_to_check = ["report-def-0-rfile.out", "report-def-1-rfile.out", "report-def-2-rfile.out"]
    pid_file = f"/data/marisha/fluent_files/pid_files/pid_{timestamp}.log"

    # Launch Fluent and wait for it to finish
    error_strings = ["Error", "command not found", "KILLED BY SIGNAL: 9 (Killed)"]  # update the array

    fluent_process = launch_fluent_console(journal_file, log_file, pid_file)

    # Wait until the process starts
    while fluent_process.poll() is None:
        time.sleep(1)

    print("Fluent process has started.")

    try:
        while True:
            user_input = input("Fluent process is running. Enter 'q' to quit: ")
            if user_input.lower() == 'q':
                terminate_fluent_process(fluent_process.pid)  # Terminate the Fluent process by PID
                try:
                    subprocess.run("pkill -9 cortex", shell=True)
                    print("Process terminated successfully.") # Terminate Cortex to close plots display
                    break
                except subprocess.CalledProcessError as e:
                    print(f"Error terminating process: {e}")
                break

            if not check_output_files(output_files_to_check):
                print("Output files were not generated as expected.")
                terminate_fluent_process(fluent_process.pid)  # Terminate the Fluent process by PID
                break

            while fluent_process.poll() is None:  # While the process is running
                error_string, location = check_for_errors(log_file, error_strings)
                if error_string:
                    print(f"Error detected in Fluent console output: {error_string}")
                    print(f"Error location in log file: {location}")
                    terminate_fluent_process(fluent_process.pid)  # Terminate the Fluent process by PID
                    break  # Exit the loop

                time.sleep(1)  # Wait for a short interval before checking again

    except KeyboardInterrupt:
        print("User terminated the script.")

if __name__ == "__main__":
    main()
