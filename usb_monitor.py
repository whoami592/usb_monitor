import usb.core
import usb.util
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='usb_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def log_usb_device(device):
    """Log details of a USB device."""
    try:
        vendor_id = device.idVendor
        product_id = device.idProduct
        manufacturer = usb.util.get_string(device, device.iManufacturer) or "Unknown"
        product = usb.util.get_string(device, device.iProduct) or "Unknown"
        serial = usb.util.get_string(device, device.iSerialNumber) or "Unknown"
        
        log_message = (f"Device Connected: VendorID={vendor_id:04x}, ProductID={product_id:04x}, "
                      f"Manufacturer={manufacturer}, Product={product}, Serial={serial}")
        logging.info(log_message)
        print(log_message)
    except Exception as e:
        logging.error(f"Error logging device: {e}")
        print(f"Error logging device: {e}")

def monitor_usb():
    """Monitor USB devices for connections."""
    print("Monitoring USB devices... Press Ctrl+C to stop.")
    
    # Store known devices to detect new connections
    known_devices = set()
    
    while True:
        try:
            # Find all USB devices
            devices = usb.core.find(find_all=True)
            current_devices = set()
            
            for dev in devices:
                dev_id = f"{dev.idVendor:04x}:{dev.idProduct:04x}"
                current_devices.add(dev_id)
                
                # Log new devices
                if dev_id not in known_devices:
                    log_usb_device(dev)
                
            # Update known devices
            known_devices = current_devices
            
            # Sleep briefly to avoid high CPU usage
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            break
        except Exception as e:
            logging.error(f"Error in monitoring: {e}")
            print(f"Error in monitoring: {e}")
            time.sleep(1)

if __name__ == "__main__":
    # Check if pyusb is installed
    try:
        import usb
    except ImportError:
        print("Please install pyusb: pip install pyusb")
        exit(1)
    
    # Run the monitor
    monitor_usb()