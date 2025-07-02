import serial
import serial.tools.list_ports

# --- Find the Orange Pi's Serial Port ---
# This is the most important part for a good user experience.
# We can identify the right port by looking for a device with a known name.
# On Windows, this might be "Standard Serial over Bluetooth link".
# On macOS, it might be "/dev/tty.orangepi-SPP".

def find_pi_port():
    """Scans available serial ports and returns the one for the Pi."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # You might need to adjust the description text based on your OS
        if "serial" in port.description.lower() or "spp" in port.description.lower():
            print(f"Found potential Pi port: {port.device} - {port.description}")
            return port.device
    return None

# --- Main Communication Loop ---
def main():
    pi_port = find_pi_port()

    if not pi_port:
        print("Error: Could not find the Orange Pi's Bluetooth serial port.")
        print("Please make sure the device is paired and connected.")
        return

    try:
        # Connect to the found serial port
        with serial.Serial(pi_port, 9600, timeout=5) as ser:
            print(f"Connected to Orange Pi on {pi_port}")
            
            while True:
                # Get input from the user
                user_input = input("You: ")
                if user_input.lower() == 'exit':
                    break

                # Send the user's message to the Pi
                # We add a newline character so the Pi's readline() function knows the message is complete
                ser.write(f"{user_input}\n".encode('utf-8'))
                
                # Wait for and read the response from the Pi
                response = ser.readline().decode('utf-8').strip()
                print(f"Luna: {response}")

    except serial.SerialException as e:
        print(f"Error communicating with the serial port: {e}")

if __name__ == "__main__":
    main()