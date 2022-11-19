from subprocess import PIPE, CalledProcessError, run
from tempfile import TemporaryFile
from time import sleep

with open("stdin.txt", encoding="utf-8") as fp:
    run(["apt-get", "update"], stdin=fp, encoding="utf-8", shell=True)
