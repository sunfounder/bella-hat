import os
import time
import subprocess
import shlex

# Create output directory if it doesn't exist
def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def run_command(cmd, capture_output=True):
    """Run a command and return its output"""
    print(f"Executing: {cmd}")
    
    try:
        # Use shlex to properly split the command for subprocess
        if isinstance(cmd, str):
            cmd_args = shlex.split(cmd)
        else:
            cmd_args = cmd
            
        # Run the command and capture output
        result = subprocess.run(
            cmd_args,
            capture_output=capture_output,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        # Print the output
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
            
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"Error executing '{cmd}': {str(e)}")
        return -1, "", str(e)

def run_background_command(cmd):
    """Run a command in the background and return its process"""
    print(f"Executing in background: {cmd}")
    try:
        # Use subprocess.Popen to run the command in the background
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Error executing '{cmd}' in background: {str(e)}")
        return None

def ble_test():
    output_dir = ensure_output_dir()
    output_file = os.path.join(output_dir, 'ble_log.txt')
    commands_output = os.path.join(output_dir, 'ble_commands_output.txt')
    
    with open(commands_output, 'w') as cmd_log:
        cmd_log.write("=== BLE TEST COMMANDS OUTPUT ===\n\n")
        
        print("Starting BLE Test...")
        # Enable Bluetooth interface
        cmd_log.write("== hciconfig hci0 up ==\n")
        code, stdout, stderr = run_command("sudo hciconfig hci0 up")
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Start BLE scanning in background
        cmd_log.write("== sudo hcitool lescan ==\n")
        lescan_process = run_background_command("sudo hcitool lescan")
        time.sleep(5)
        
        # Stop BLE scanning
        cmd_log.write("== sudo pkill --signal SIGINT hcitool ==\n")
        code, stdout, stderr = run_command("sudo pkill --signal SIGINT hcitool")
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Process lescan output if available
        if lescan_process:
            try:
                lescan_stdout, lescan_stderr = lescan_process.communicate(timeout=1)
                cmd_log.write(f"lescan STDOUT:\n{lescan_stdout}\n")
                cmd_log.write(f"lescan STDERR:\n{lescan_stderr}\n\n")
            except subprocess.TimeoutExpired:
                lescan_process.kill()
                cmd_log.write("lescan process timed out or was killed\n\n")
        
        # Capture BLE packets
        cmd_log.write("== sudo hcidump -X ==\n")
        hcidump_process = run_background_command(f"sudo hcidump -X")
        time.sleep(5)
        
        # Write hcidump output to the BLE log file
        if hcidump_process:
            try:
                hcidump_stdout, hcidump_stderr = hcidump_process.communicate(timeout=1)
                with open(output_file, 'w') as f:
                    f.write(hcidump_stdout)
                cmd_log.write(f"hcidump STDERR:\n{hcidump_stderr}\n\n")
            except subprocess.TimeoutExpired:
                hcidump_process.kill()
                cmd_log.write("hcidump process timed out or was killed\n\n")
        
        # Stop hcidump
        cmd_log.write("== sudo pkill --signal SIGINT hcidump ==\n")
        code, stdout, stderr = run_command("sudo pkill --signal SIGINT hcidump")
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
    
    print(f"BLE Test completed. Logs saved in {output_file}")
    return [output_file, commands_output]

def bt_classic_test(target_mac):
    output_dir = ensure_output_dir()
    output_file = os.path.join(output_dir, 'bt_classic_log.txt')
    commands_output = os.path.join(output_dir, 'bt_classic_commands_output.txt')
    
    with open(commands_output, 'w') as cmd_log:
        cmd_log.write("=== BLUETOOTH CLASSIC TEST COMMANDS OUTPUT ===\n\n")
        
        print("Starting Bluetooth Classic Test...")
        # Send ping packets
        cmd = f"l2ping -c 5 {target_mac}"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save the ping output
        with open(output_file, 'w') as f:
            f.write(f"L2PING RESULTS FOR {target_mac}:\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
    
    print(f"Bluetooth Classic Test completed. Logs saved in {output_file}")
    return [output_file, commands_output]

def wifi_test(interface='wlan0', iperf_server='192.168.1.100'):
    output_dir = ensure_output_dir()
    lower_output = os.path.join(output_dir, 'wifi_lower_log.txt')
    upper_output = os.path.join(output_dir, 'wifi_upper_log.txt')
    commands_output = os.path.join(output_dir, 'wifi_commands_output.txt')
    
    with open(commands_output, 'w') as cmd_log:
        cmd_log.write("=== WIFI 2.4GHZ TEST COMMANDS OUTPUT ===\n\n")
        
        print("Starting Wi-Fi Test on 2.4 GHz channels...")
        print(f"Using iPerf server: {iperf_server}")
        
        # Get current interface information
        cmd_log.write(f"== iwconfig {interface} ==\n")
        code, stdout, stderr = run_command(f"iwconfig {interface}")
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Lower channel (1 - 2412 MHz)
        cmd = f"iw dev {interface} set channel 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Run iperf3 on lower channel
        cmd = f"iperf3 -c {iperf_server} -t 10 -i 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save iperf output
        with open(lower_output, 'w') as f:
            f.write(f"IPERF3 RESULTS FOR CHANNEL 1 (2412 MHz):\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        print(f"Lower channel test completed. Logs saved in {lower_output}")
        
        # Upper channel (13 - 2472 MHz)
        cmd = f"iw dev {interface} set channel 13"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Run iperf3 on upper channel
        cmd = f"iperf3 -c {iperf_server} -t 10 -i 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save iperf output
        with open(upper_output, 'w') as f:
            f.write(f"IPERF3 RESULTS FOR CHANNEL 13 (2472 MHz):\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        print(f"Upper channel test completed. Logs saved in {upper_output}")
    
    return [lower_output, upper_output, commands_output]

def wifi_5ghz_test(interface='wlan0', iperf_server='192.168.1.100'):
    output_dir = ensure_output_dir()
    lower_output = os.path.join(output_dir, 'wifi_5ghz_lower_log.txt')
    upper_output = os.path.join(output_dir, 'wifi_5ghz_upper_log.txt')
    commands_output = os.path.join(output_dir, 'wifi_5ghz_commands_output.txt')
    
    with open(commands_output, 'w') as cmd_log:
        cmd_log.write("=== WIFI 5GHZ TEST COMMANDS OUTPUT ===\n\n")
        
        print("Starting Wi-Fi Test on 5 GHz channels...")
        print(f"Using iPerf server: {iperf_server}")
        
        # Get current interface information
        cmd_log.write(f"== iwconfig {interface} ==\n")
        code, stdout, stderr = run_command(f"iwconfig {interface}")
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Lower 5GHz channel (36 - 5180 MHz)
        cmd = f"iw dev {interface} set channel 36"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Run iperf3 on lower 5GHz channel
        cmd = f"iperf3 -c {iperf_server} -t 10 -i 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save iperf output
        with open(lower_output, 'w') as f:
            f.write(f"IPERF3 RESULTS FOR CHANNEL 36 (5180 MHz):\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        print(f"Lower 5GHz channel test completed. Logs saved in {lower_output}")
        
        # Upper 5GHz channel (149 - 5745 MHz)
        cmd = f"iw dev {interface} set channel 149"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Run iperf3 on upper 5GHz channel
        cmd = f"iperf3 -c {iperf_server} -t 10 -i 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save iperf output
        with open(upper_output, 'w') as f:
            f.write(f"IPERF3 RESULTS FOR CHANNEL 149 (5745 MHz):\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        print(f"Upper 5GHz channel test completed. Logs saved in {upper_output}")
    
    return [lower_output, upper_output, commands_output]

def fcc_rss_emc_tests(interface='wlan0', iperf_server='192.168.1.100'):
    output_dir = ensure_output_dir()
    tx_output = os.path.join(output_dir, 'fcc_tx_log.txt')
    sim_output = os.path.join(output_dir, 'sim_comm_log.txt')
    commands_output = os.path.join(output_dir, 'fcc_commands_output.txt')
    
    with open(commands_output, 'w') as cmd_log:
        cmd_log.write("=== FCC/RSS/EMC TEST COMMANDS OUTPUT ===\n\n")
        
        print("Starting FCC 15 C/E, RSS-247 & EMC Mode Tests...")
        print(f"Using iPerf server: {iperf_server}")
        
        # Individual TX tests - set channel
        cmd = f"iw dev {interface} set channel 6"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Run UDP iperf3 test
        cmd = f"iperf3 -c {iperf_server} -u -b 10M -t 10"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save iperf output
        with open(tx_output, 'w') as f:
            f.write(f"IPERF3 UDP RESULTS FOR CHANNEL 6 (TX TEST):\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        print(f"Individual TX test completed. Logs saved in {tx_output}")
        
        # BLE continuous TX
        cmd = "hcitool cmd 0x08 0x1E 0x01"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Simultaneous test with iperf
        cmd = f"iperf3 -c {iperf_server} -t 10 -i 1"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        # Save simultaneous test output
        with open(sim_output, 'w') as f:
            f.write(f"SIMULTANEOUS COMMUNICATION TEST RESULTS:\n\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
        
        # Stop BLE TX
        cmd = "hcitool cmd 0x08 0x1E 0x00"
        cmd_log.write(f"== {cmd} ==\n")
        code, stdout, stderr = run_command(cmd)
        cmd_log.write(f"Return Code: {code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}\n\n")
        
        print(f"Simultaneous communication test completed. Logs saved in {sim_output}")
    
    return [tx_output, sim_output, commands_output]

def read_output_file(file_path):
    """Read and return the content of an output file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def main():
    ble_test()
    # bt_classic_test(target_mac="9C:76:0E:7C:56:79")  # Replace with actual MAC address
    # wifi_test(iperf_server="192.168.86.23")
    # wifi_5ghz_test(iperf_server="192.168.86.23")
    # fcc_rss_emc_tests(iperf_server="192.168.86.23")
    print("EN 300 328, EN 301 893, FCC 15 C/E, RSS-247 & EMC Mode Tests Completed!")

if __name__ == "__main__":
    main()
