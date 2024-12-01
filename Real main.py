# run_both.py
import subprocess

def run_scripts():
    # Run main.py
    process1 = subprocess.Popen(["python", "main.py"])

    # Run main2.py
    process2 = subprocess.Popen(["python", "main2.py"])

    # Wait for both processes to finish
    process1.communicate()
    process2.communicate()

if __name__ == "__main__":
    run_scripts()
