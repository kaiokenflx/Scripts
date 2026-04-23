from argparse import ArgumentParser
from sys import stdin, stderr
from dataclasses import dataclass
from subprocess import run
from os.path import isfile

''' rsync wrapper script for sending files over SSH  '''

parser = ArgumentParser()
parser.add_argument("-a", "--ip_address", type=str, required=True, help="Target IP address")
parser.add_argument("-p", "--port", type=int, help="Target SSH port")
parser.add_argument("-f", "--file", type=str, required=True, help="Path to file to send")
parser.add_argument("-u", "--user", type=str, required=True, help="Username to login with")
parser.add_argument("-d", "--destination", type=str, required=True, help="Destination path for file sent")
args = parser.parse_args()

ip = args.ip_address

port = 22
if args.port != None:
    port = args.port

address = f"{ip}:{port}"

file = args.file
if not isfile(file):
    print(f"File not found: {file}", file=stderr)
    exit(-1)

username = args.user
destination = args.destination

print(f"Target Address = {address}")
print(f"File to send = {file}")
print(f"Login username = {username}")
print(f"Destination file path = {destination}\n")

print(f"Is this correct? [y/N] ", end='', flush=True)
answer = stdin.read(1)

if answer == 'n' or answer == 'N':
    print("OK, job canceled!")
    exit(0)

@dataclass
class Command:
    app: str
    arg_shell_command: str
    arg_sub_shell: str
    app_arg_archive: str
    app_arg_verbose: str
    app_arg_compress: str
    app_arg_partial: str

command = Command(
    app="rsync", 
    arg_shell_command="e", # specify the remote shell to use
    arg_sub_shell=f"ssh -p {port}",
    app_arg_archive="a", # archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
    app_arg_verbose="v", # increase verbosity
    app_arg_compress="z", # compress file data during the transfer
    app_arg_partial="P" # same as --partial --progress
)

print(f"Sending '{file}' to {address}..")

run(
    [
        command.app, 
        f"-{command.arg_shell_command}", command.arg_sub_shell,
        f"-{command.app_arg_archive}",
        f"-{command.app_arg_verbose}",
        f"-{command.app_arg_compress}",
        f"-{command.app_arg_partial}",
        file,
        f"{username}@{ip}:{destination}"
    ]
)