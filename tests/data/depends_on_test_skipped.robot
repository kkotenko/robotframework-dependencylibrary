*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
Skipped Test
    Skip    This test is skipped for some reason.

A Test that Depends on "Skipped Test"
    Depends on test    Skipped Test
    Log    The rest of the keywords (including this log) will NOT run!
