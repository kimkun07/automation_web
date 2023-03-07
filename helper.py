import time
from typing import Callable, Iterator, TypeVar


def only_one(__iterable: Iterator[TypeVar("_T")]) -> TypeVar("_T"):
    """iterable의 원소가 단 하나라는 것을 확인시켜주고 반환"""
    cnt = 0
    the_one = None
    for element in __iterable:
        the_one = element
        cnt += 1
    assert cnt == 1, f"__iterable is not only one. cnt={cnt}"
    return the_one


def wait_until(condition: Callable[[], bool], timeout=120, period=5):
    """
    condition 함수가 만족할 때까지 기다리기. 단위는 초.
    timeout까지 기다렸는데 condition이 만족하지 않는다면 false를 반환한다.
    """
    # wait을 지원하지 않는 경우, 직접하는 것이다
    quit_time = time.time() + timeout
    while time.time() < quit_time:
        print("Debug - While")
        if condition():
            return True
        time.sleep(period)
    print(f"Waited for {timeout}s but {condition} never completed.")
    return False
