import subprocess

cmd = ['atlas-run-standalone', '--product', 'confluence', '--version', '6.6.0', '--server', 'localhost']

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
for line in p.stdout:
    if line.startswith('Would you like to subscribe to the Atlassian developer mailing list'.encode()):
        print('Found mailing list line')
        p.stdin.writelines('n'.encode())
    elif line.startswith('[INFO] Type Ctrl-C to exit'.encode()):
        print('Found exit line')
        break
