# call_exit.py
import subprocess

cp = subprocess.run(["python.exe","factoryEnroll.py", "-m", "00:90:e8:44:22:11", "-M", "UC-8112A-ME-T-LX", "-s", "A12345678"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print('return Code:' + str(cp.returncode))
print('return Output:' + cp.stdout)