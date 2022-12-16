*** Settings ***
Documentation  Test case used to search for top 2 most expensive items in a category.
Resource  robotlib.robot


Test Setup  SETUP
Test Teardown  TEARDOWN

*** Variables ***
${emag_webpage}    https://www.emag.ro/

*** Keywords ***
SETUP
    START CHROME    ${emag_webpage}

TEARDOWN
    CLOSE CHROME

*** Test Cases ***
GET MOST EXPENSIVE ITEMS
    TAP BY XPATH    ${Emag['tv_audio_video_photo']}    0.5
    TAP BY XPATH    ${Emag['TVs']}    0.5
    TAP BY XPATH    ${Emag['dropdown_order']}    0.5
    TAP BY XPATH    ${Emag['highest_price']}    0.5
    ADD TWO ITEMS TO CART    ${Emag['first_displayed_element']}    ${Emag['second_displayed_element']}
    ${products_from_cart} =    RETRIEVE TEXT BY XPATH    ${Emag['shopping_cart_items']}
    should be equal  ${products_from_cart}    ${2}    Fail, 2 items were not added to shopping cart.