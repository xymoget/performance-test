# tests.py

import time
import os
import tempfile
import random

def cpu_test():
    """Simulate a CPU performance test by calculating factorials in a loop."""
    start_time = time.time()
    result = 1
    for i in range(1, 1000000000):  # Increase this range for more intense testing
        result *= i
        if result > 1e20:
            result = 1  # Reset to prevent overflow
    end_time = time.time()
    duration = end_time - start_time
    cpu_score = int(5000 + (5 / duration))  # Calculate a score based on time taken
    return cpu_score

def ram_test():
    """Simulate a RAM performance test by allocating and manipulating a large list."""
    start_time = time.time()
    data = [random.random() for _ in range(10**8)]  # Allocate a large list
    for i in range(len(data)):
        data[i] = data[i] ** 2  # Manipulate list data to simulate load
    end_time = time.time()
    duration = end_time - start_time
    ram_score = int(3000 + (2 / duration))  # Calculate a score based on time taken
    return ram_score

def disk_test():
    """Simulate a Disk performance test by writing and reading a temporary file."""
    start_time = time.time()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        # Write a large amount of data
        temp_file.write(os.urandom(10**7))  # 10 MB of random data
        temp_file.flush()
        temp_file.seek(0)

        # Read the data back
        temp_file.read()

    finally:
        temp_file.close()
        os.unlink(temp_file.name)  # Delete the temp file

    end_time = time.time()
    duration = end_time - start_time
    disk_score = int(4000 + (3 / duration))  # Calculate a score based on time taken
    return disk_score
