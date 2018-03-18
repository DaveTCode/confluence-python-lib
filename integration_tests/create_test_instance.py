import argparse
import subprocess


def create_detached_server(version):
    # type: (str) -> None
    cmd = ['atlas-run-standalone', '--product', 'confluence', '--version', version, '--server', 'localhost']

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout:
        p.stdin.writelines('n'.encode())
        if line.startswith('[INFO] Type Ctrl-C to exit'.encode()):
            print('Found exit line')
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('version', default='6.6.0')
    args = parser.parse_args()

    create_detached_server(args.version)
