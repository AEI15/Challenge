*** Settings ***
Library  ChromeMethods.py
Variables  constants.yaml

*** Variables ***

*** Keywords ***
START CHROME
    [Arguments]    ${path}
    [Documentation]    Start chrome browser
    START CHROME BROWSER  ${path}

CLOSE CHROME
    [Documentation]    Quit chrome browser
    QUIT CHROME

TAP BY XPATH
    [Arguments]    ${xpath}    ${wait}=${0}
    Log    xpath=${xpath}
    ${verdict} =   TAP ON ELEMENT BY    XPATH    ${xpath}
    Should be True    ${verdict}    Element ${xpath} has not been found
    Sleep    ${wait}

TAP BY CSS
    [Arguments]    ${css_selector}    ${wait}=${0}
    ${verdict} =   TAP ON ELEMENT BY    CSS_SELECTOR    ${css_selector}
    Should be True    ${verdict}    Element has not been found
    Sleep    ${wait}

TAP BY ID
    [Arguments]    ${id}    ${wait}=${0}
    ${verdict} =    TAP ON ELEMENT BY    ID    ${id}
    Should be true    ${verdict}    Element has not been found
    Sleep    ${wait}

TAP BY TEXT
    [Arguments]    ${text}    ${wait}=${0}
    ${verdict} =   TAP ON ELEMENT BY    PARTIAL_LINK_TEXT    ${text}
    Should be True    ${verdict}    Element has not been found
    Sleep    ${wait}

ADD TWO ITEMS TO CART
    [Arguments]    ${first_item}    ${second_item}
    [Documentation]   This kw is used to add first to elements to shopping cart.
    TAP BY XPATH    ${first_item}
    TAP BY XPATH    ${Emag['add_to_cart_first_element']}
    GO BACK PAGE
    TAP BY XPATH    ${second_item}
    TAP BY XPATH    ${Emag['add_to_cart_second_element']}
    GO BACK PAGE

RETRIEVE TEXT BY XPATH
    [Arguments]    ${xpath}    ${attr}=${None}
    ${text_retrieved} =    RETRIEVE TEXT USING    XPATH    ${xpath}    ${attr}
    Run Keyword If    """${text_retrieved}""" == """""" or "${text_retrieved}" == "False"    Run Keyword
    ...    Fail    No text has been retrieved
    [Return]    ${text_retrieved}