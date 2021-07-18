#!/usr/bin/env python

"""
A set of useful tools.
"""

import os
import shutil
import sys

from loguru import logger

LOG_FORMAT = '<light-green>[{time:HH:mm:ss}]</light-green> <level>{message}</level>'
LOG_LEVEL = 'TRACE'

logger.remove()
logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)


def trace(s): logger.info(s) if s else ''
def debug(s): logger.debug(s) if s else ''
def info(s): logger.info(s) if s else ''
def success(s): logger.success(s) if s else ''
def warning(s): logger.warning(s) if s else ''
def error(s): logger.error(s) if s else ''
def critical(s): logger.critical(s) if s else ''


def error_and_exit(msg, code=1):
    error(msg)
    sys.exit(code)
    
    
def mkdir(path):
    if not path:
        error_and_exit('Path for mkdir must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for mkdir is not a string.')
    try:
        os.mkdir(path)
    except FileExistsError:
        debug(f'Directory {path} already exist.')
    except OSError as e:
        error_and_exit(f'{e}, create directory failed!')
    return path
    
    
def touch(path, overwrite=False):
    if not path:
        error_and_exit('Path for touch must a be non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for touch is not a string.')
    if os.path.isfile(path):
        if overwrite:
            try:
                with open(path, 'w') as o:
                    o.write('')
            except OSError as e:
                error_and_exit(f'{e}, touch file (overwrite existing file) failed!')
        else:
            logger.debug(f'File {path} already exists and did not overwrite.')
    else:
        try:
            with open(path, 'w') as o:
                o.write('')
        except OSError as e:
            error_and_exit(f'{e}, touch file failed!')
    return path


def rm(path, exit_on_error=True):
    if not path:
        error_and_exit('Path for rm must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for rm is not a string.')
    if os.path.exists(path):
        try:
            os.unlink(path)
        except IsADirectoryError:
            try:
                shutil.rmtree(path)
            except Exception as e:
                error(f'{e}, delete directory failed!')
                if exit_on_error:
                    sys.exit(1)
        except OSError as e:
            error(f'{e}, delete file failed!')
            if exit_on_error:
                sys.exit(1)
    else:
        debug(f"No such file or directory '{path}', delete file or directory aborted!")
        
        
def equal_len_lists(l1, l2, msg='', exit_if_unequal=True):
    equal = len(l1) == len(l2)
    error(msg)
    if not equal and exit_if_unequal:
        sys.exit(1)
    return equal
            

if __name__ == '__main__':
    pass
