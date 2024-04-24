*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
Failing Test
    Fail    This test failed for some reason.

A Test that Depends on "Failing Test"
    Depends on test    Failing Test
    Log    The rest of the keywords (including this log) will NOT run!
