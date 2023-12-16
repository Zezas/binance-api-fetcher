*** Settings ***
Documentation     This a test suite for the Source class. 
Library           robot_source_custom_library.py

*** Test Cases ***
Test Source Connection
    ${source}    Create Source Instance    https://api.binance.com/api/v3/
    Connect To Source    ${source}
