*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
Passing Test
    No operation

Another Passing Test
    No operation

A Test that Depends on Both "Passing Test" and "Another Passing Test"
    Depends on test    Passing Test
    Depends on test    Another Passing Test
    Log    The rest of the keywords in this test will run as normal.
