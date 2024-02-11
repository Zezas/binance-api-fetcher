*** Settings ***
Documentation     This a test suite for the Source class.
Library           robot_source_custom_library.py


*** Variables ***
${source}


*** Test Cases ***
Test Source Connection - No Error
    [Documentation]    Test that a Source instance can connect without errors.
    Given Source Instance Is Created    https://api.binance.com/api/v3/
    When Source Instance Connects Successfully
    Then Source Connection Is Successful

Test Source Connection - Error
    [Documentation]    Test that a Source instance throws an error with a bad connection string.
    Given Source Instance Is Created    bad_connection_string
    When Source Instance Connects Unsuccessfully
    Then Source Connection Is Unsuccessful

*** Keywords ***
Source Instance Is Created
    [Arguments]          ${connection_string}
    ${source}            Create Source Instance    ${connection_string}
    Set Test Variable    ${source}

Source Instance Connects Successfully
    Connect To Source    ${source}

Source Instance Connects Unsuccessfully
    Run Keyword And Expect Error    SourceError: Error connecting to source: None - .    Connect To Source    ${source}

Source Connection Is Successful
    ${is_connected}      Check If Source Is Connected    ${source}
    Should Be True       ${is_connected}

Source Connection Is Unsuccessful
    ${is_connected}      Check If Source Is Connected    ${source}
    Should Not Be True   ${is_connected}
