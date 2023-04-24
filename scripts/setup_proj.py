#!/usr/bin/python3
"""
project setup scripts

version: 0.3.1

This script should
 - setup a virtual environment
 - installs requirements from a requirement.txt file
 - installs a postgresql server
 - creates a database
"""
import sys
import os
import subprocess
import pathlib
from exceptions import (
    NoOptionPassed,
    OptionNo
)

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
setup_db_file = 'setupdb'

def install_db():
    """installs a database by running script
    """
    install_pgsql = ['./scripts/setupdb']
    subprocess.run(install_pgsql, cwd=BASE_DIR)

def create_db(db_name:str, user:str, h=None, p=None, E=None):
    """creates a postgresql database
    """
    if type(db_name) and type(user) != str:
        TypeError('unexpected argument type provided for db_name or user\
            , must be a string')

    if len(db_name) == 0:
        db_name = 'proj-dev-db-local1'

    host = 'localhost'
    port = 5432
    enconding = 'utf8'
    if h and p and E != None:
        host = h
        port = p
        enconding = E

    create_db_args = f'createdb/-U {user}/-h{host}/-p {port}/-E {enconding}/{db_name}'.split(sep='/')
    with open('logfile', mode='w+', encoding='utf8') as logfile:
        try:
            os.system(' '.join(create_db_args))
        except Exception:
            raise(Exception)
    print(f'database {db_name} created with user {user}.')


def setup_venv(venv_name=None):
    """creates a virtual environment
    """
    vname = 'proj_venv'
    if venv_name != None:
        vname = venv_name

    # installs virtualenv
    # creates a virtual environment
    # install dependecies
    # stores some output in a logfile
    install_virtualenv = ['./scripts/install_virtualenv']
    make_venv = ['virtualenv', f'{vname}']
    install_dependecies = [f'{vname}/bin/python3',
                            '-m', 'pip', 'install', '-r', 'requirements.txt']

    with open('logfile', mode='w+', encoding='utf8') as logfile:
        try:
            subprocess.run(install_virtualenv,
                               stdout=logfile, cwd=BASE_DIR)
            subprocess.run(make_venv, stdout=logfile, cwd=BASE_DIR)

            install_option = input(
                'would you like to install requirements.txt (y/n, Yes/No)? ')

            if install_option in ('y', 'Yes'):
                subprocess.run(install_dependecies, cwd=BASE_DIR)
            if install_option in ('n', 'No'):
                raise(OptionNo)
            else:
                raise(NoOptionPassed)

        except OptionNo:
            pass
        except Exception:
            raise(Exception)

def main():
    """ script entry point
    """
    idb = input('install a postgresql db (y/n)? ')
    if idb != 'n':
        try:
            install_db()
        except Exception as e:
            print(str(e))

    cdb = input('create a postgresql database (y/n)? ')
    if cdb != 'n':
        dbname = input('dbname default(proj-dev-db-local1): ')
        username = input('user: ')
        #host = input('host default(localhost): ')
        #port = input('port default(5432): ')
        #econding = input('encoding default(utf8): ')

        try:
            create_db(db_name=dbname, user=username)
        except Exception as e:
            print(str(e))

    ivenv = input('create a virtual environment (y/n)?')
    if ivenv != 'n':
        try:
            venv_name: str
            venv_name = input('virtual environemt name (defualt: proj_venv)? ')
            if venv_name:
                pass
            else:
                raise(NoOptionPassed)
        except NoOptionPassed:
            venv_name = 'proj_venv'
    
        try:
            setup_venv(venv_name=venv_name)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()
