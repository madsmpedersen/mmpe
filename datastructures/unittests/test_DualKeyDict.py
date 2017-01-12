'''
Created on 08/11/2013

@author: mmpe
'''
import unittest

from mmpe.datastructures.dual_key_dict import DualKeyDict


class Example(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Test(unittest.TestCase):

    def setUp(self):
        self.ex1 = Example(1, "one")
        self.ex2 = Example(2, "two")
        self.ex3 = Example(3, "two")
        self.dkd = DualKeyDict("id", "name")
        for ex in [self.ex1, self.ex2, self.ex3]:
            self.dkd.add(ex)


    def testget(self):
        self.assertEqual(self.dkd[1], self.ex1)
        self.assertEqual(self.dkd['one'], self.ex1)
        self.assertEqual(self.dkd[2], self.ex2)
        self.assertRaisesRegex(AttributeError, "More objects associated by key, 'two'. Use 'get' function to get list of objects", self.dkd.__getitem__, ("two"))


    def testset(self):
        self.dkd[1] = Example(4, "four")
        self.assertEqual(self.dkd[4].name, "four")


    def test_add_not_unique_key(self):
        self.assertRaisesRegex(KeyError, "Key '3' already exists in dict", self.dkd.add, (Example(3, "three")))

    def test_add_additional_not_existing(self):
        ex4 = Example(4, "four")
        self.dkd.add(ex4)
        self.assertTrue(4 in self.dkd)
        self.assertEqual(self.dkd[4], ex4)
        self.assertEqual(self.dkd["four"], ex4)

    def test_add_additional_existing(self):
        ex4 = Example(4, "one")
        self.dkd.add(ex4)
        self.assertTrue(4 in self.dkd)
        self.assertEqual(self.dkd[4], ex4)
        self.assertEqual(self.dkd._dict["one"], [self.ex1, ex4])

    def test_add_additional_existing_list(self):
        ex4 = Example(4, "two")
        self.dkd.add(ex4)
        self.assertTrue(4 in self.dkd)
        self.assertEqual(self.dkd[4], ex4)
        self.assertEqual(self.dkd._dict["two"], [self.ex2, self.ex3, ex4])

    def test_values(self):
        self.assertEqual(self.dkd.values(), [self.ex1, self.ex2, self.ex3])

    def test_keys(self):
        self.assertEqual(self.dkd.keys(), [1, 2, 3])

    def test_remove_id(self):
        removed = self.dkd.remove(1)
        self.assertEqual(removed, self.ex1)
        self.assertFalse(1 in self.dkd)
        self.assertFalse("one" in self.dkd)
        self.assertEqual(len(self.dkd), 2)

    def test_remove_additional(self):
        removed = self.dkd.remove("one")
        self.assertEqual(removed, self.ex1)
        self.assertFalse(1 in self.dkd)
        self.assertFalse("one" in self.dkd)
        self.assertEqual(len(self.dkd), 2)

    def test_remove_additional_in_list_with_one_other(self):
        removed = self.dkd.remove(2)
        self.assertEqual(removed, self.ex2)
        self.assertFalse(2 in self.dkd)
        self.assertTrue(3 in self.dkd)
        self.assertTrue("two" in self.dkd)
        self.assertEqual(self.dkd._dict["two"], self.ex3)
        self.assertEqual(len(self.dkd), 2)

    def test_remove_additional_in_list_with_two_others(self):
        ex = Example(4, "two")
        self.dkd.add(ex)
        removed = self.dkd.remove(2)
        self.assertEqual(removed, self.ex2)
        self.assertEqual(self.dkd.keys(), [1, 3, 4])
        self.assertTrue("two" in self.dkd)
        self.assertEqual(self.dkd._dict["two"], [self.ex3, ex])
        self.assertEqual(len(self.dkd), 3)

    def test_get(self):
        self.assertEqual(self.dkd.get(1), self.ex1)
        self.assertEqual(self.dkd.get("one"), self.ex1)

    def test_get_default(self):
        self.assertEqual(self.dkd.get(4), None)
        self.assertEqual(self.dkd.get(4, "default"), "default")

    def test_get_list(self):
        self.assertEqual(self.dkd.get("two"), [self.ex2, self.ex3])
        self.assertRaisesRegex(AttributeError, "More objects associated by key, 'two'", self.dkd.get, "two", multiple_error=True)

    def test_clear(self):
        self.dkd.clear()
        self.assertEqual(len(self.dkd), 0)
        self.assertEqual(len(self.dkd._dict), 0)
        self.assertEqual(len(self.dkd._unique_keys), 0)

    def test_copy(self):
        dkdcopy = self.dkd.copy()
        self.assertEqual(len(dkdcopy), len(self.dkd))
        self.assertEqual(dkdcopy.values(), self.dkd.values())


    def test_copy_change_contents(self):
        dkdcopy = self.dkd.copy()
        self.dkd.add(Example(4, "four"))
        self.assertFalse(4 in dkdcopy)
        dkdcopy.add(Example(4, "five"))
        self.assertFalse(5 in self.dkd)
        self.dkd.remove(self.ex1)
        self.assertTrue(1 in dkdcopy)

    def test_copy_change_key_att(self):
        dkdcopy = self.dkd.copy()
        dkdcopy._unique_key_att += "copy"
        self.assertEqual(self.dkd._unique_key_att, "id")
        dkdcopy._additional_key_att[0].replace("n", "copy")
        self.assertEqual(self.dkd._additional_key_att, "name")

    def test_iterate(self):
        self.assertEqual([1, 2, 3], [i for i in self.dkd])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
