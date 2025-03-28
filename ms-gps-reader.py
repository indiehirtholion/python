import serial
import pynmea2
import curses

def gps_display(stdscr):
    # Initialize the serial port
    ser = serial.Serial('/dev/ttyUSB0', baudrate=4800, timeout=1)

    # Configure the curses screen
    stdscr.clear()
    stdscr.nodelay(1)  # Make getch() non-blocking
    stdscr.timeout(2500)  # Refresh every 2500ms

    try:
        while True:
            # Read a line from the GPS device
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$GP'):  # Process only GPS sentences
                try:
                    msg = pynmea2.parse(line)
                    
                    # Clear screen before updating
                    stdscr.clear()
                    
                    # Display information
                    stdscr.addstr(0, 0, "GPS Data (Updated Live)", curses.A_BOLD)
                    stdscr.addstr(2, 0, f"Raw Sentence: {line}")
                    stdscr.addstr(3, 0, f"Parsed Data: {msg}")
                    
                    # Extract and display fields
                    row = 5
                    for field in msg.fields:
                        label, attr = field[0], field[1]
                        value = getattr(msg, attr, None)
                        stdscr.addstr(row, 0, f"{label}: {value}")
                        row += 1

                    # Refresh screen
                    stdscr.refresh()

                    # Allow exiting with 'q'
                    key = stdscr.getch()
                    if key == ord('q'):
                        break

                except pynmea2.ParseError as e:
                    stdscr.addstr(5, 0, f"Parse error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

# Run the curses-based interface
curses.wrapper(gps_display)
