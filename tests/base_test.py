import os
import functools
import threading
import unittest
from traceback import format_exc
from queue import Queue

TEST_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.dirname(TEST_DIR)

def do_stuff(q1, a, k, method):
    try:
        q1.put(method(*a, **k))
    except Exception as e:
        q1.put(e)

def timeout(sec):
    def timeout_dec(func):
        @functools.wraps(func)
        def test(*args, **kwargs):
            q = Queue()
            p = threading.Thread(target=do_stuff, args=[q, args, kwargs, func], kwargs={}, daemon=True)
            p.start()
            p.join(sec)

            if p.is_alive():
                # I can't kill the thread, but just keep the tests running.
                raise TimeoutError(f"Timed out after {sec} seconds")
            else:
                x = q.get()
                if isinstance(x, Exception):
                    raise x
                return x
        return test
    return timeout_dec

class BaseTest(unittest.TestCase):

    def _callTestMethod(self, method):
        self.maxDiff = None
        try:
            method()
        except AssertionError as e:
            raise e
        except Exception as e:
            print(format_exc())
            raise e
