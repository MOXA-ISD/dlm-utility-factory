# call_exit.py
import subprocess

cp = subprocess.run(["python.exe","factoryEnroll.py"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print('return Code:' + str(cp.returncode))
print('return Output:' + cp.stdout)