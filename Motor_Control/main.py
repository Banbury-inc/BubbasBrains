import serial
import time
import L300n
import L400n
def main():
    # call function L300n which is in another file
    while True:
        L300n.L300n()
        # Set a timer for 5 seconds
        time.sleep(5)
        L400n.L400n()

        time.sleep(5)

if __name__ == "__main__":
    main()
