*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
A Test that Depends on Both "Suite passed 01" and "Suite passed 01"
    Depends On Suite    Suite passed 01
    Depends on Suite    Suite passed 02
    Log    The rest of the keywords in this test will run as normal.
