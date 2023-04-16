import unittest
import functions


def test_new_password():
    assert functions.new_password("moi", "moi") == None
    assert functions.new_password("moimoimoi", "moimoi") == False
    assert functions.new_password("moimoimoi", "moimoimoi") == True
