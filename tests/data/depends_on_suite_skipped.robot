*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
A Test that Depends on an Entire Test Suite Passing
    Depends on suite    Suite skipped
    Log    The rest of the keywords will run if that whole suite passed.
