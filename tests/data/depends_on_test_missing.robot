*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
A Test that Depends on "Missing Test"
    Depends on test    Missing Test
