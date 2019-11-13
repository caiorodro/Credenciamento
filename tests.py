#import unittest
# from elasticsearch import Elasticsearch

# es = Elasticsearch([{'host': 'https://aws.data.highio.i3', 'port': '9200'}])
# es.con
# print(es)

# from app.base.loggerNoSQL import loggerNoSQL

# l1 = loggerNoSQL()

# l1.newLog('message of Today 1', "ERROR", "Tests", 1)

# class Foo:
#     def __init__(self, val):
#         self.val = val

#     def __eq__(self, other):
#         return self.val == other.val

# def test_compare():
#     f1 = Foo(1)
#     f2 = Foo(2)
#     try:
#         assert f1 == f2
#     except AssertionError as ae:
#         print(ae)

#test_compare()

def FibN(n, count=None):

    if count is not None:
        count += 1

    if n <= 2:
       f = 1
       print(f)
    elif n > 2:
        count = 1 if count is None else count + 1
        f = FibN(n-1) + FibN(n-2)
        print(f, ':n')

    return f

FibN(8)
