*** Settings ***
Documentation     This a test suite for the Source class.
Library           robot_source_custom_library.py

*** Test Cases ***
Test Source Connection - No Error
    ${source}    Create Source Instance    https://api.binance.com/api/v3/
    Connect To Source    ${source}

Test Source Connection - Error
    ${source}    Create Source Instance    bad_connection_string
    Run Keyword And Expect Error    SourceError: Error connecting to source: None - .    Connect To Source    ${source}
