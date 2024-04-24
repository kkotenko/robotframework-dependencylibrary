*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
Passing Test
    No operation

A Test that Depends on "Passing Test"
    Depends on test    Passing Test
    Log    The rest of the keywords in this test will run as normal.
