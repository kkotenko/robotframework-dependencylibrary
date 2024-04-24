*** Settings ***
Library     DependencyLibrary


*** Test Cases ***
Depends on Self
    Depends on test    Depends on Self
