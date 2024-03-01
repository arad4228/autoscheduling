from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from secrete import *
import time

def repeatReservation(driver: webdriver):
    driver.page_sourve

def autoscheduling(driver: webdriver):
    koreaUniv = 'https://portal.korea.ac.kr/'
    driver.get(koreaUniv)
    time.sleep(2)

    ownerId = driver.find_element(By.ID, "oneid")
    ownerId.send_keys(Korea_ID)
    ownerPW = driver.find_element(By.ID, "_pw")
    ownerPW.send_keys(Korea_PW)
    btnLogin = driver.find_element(By.ID, "loginsubmit")
    btnLogin.click()
    WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "정보생활"))
        )
    
    # 로그인 이후 행동
    js_script = "moveComponent('https://infodepot.korea.ac.kr', '3', '/common/FMSLogin2.jsp', '86', '1260', 'S');"
    driver.execute_script(js_script)
    time.sleep(3)
    # new_tab = [tab for tab in driver.window_handles if tab != original_window]
    driver.switch_to.window(driver.window_handles[1])

    btnIgnore = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "proceed-button"))
    )
    btnIgnore.click()

    manual_search_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='rm_reserve_control1_all.jsp']"))
    )
    manual_search_link.click()
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.NAME, "frame1"))
    )

    # 로봇융합관
    building_list = driver.find_element(By.NAME, "blid")
    PET_Home = Select(building_list)
    PET_Home.select_by_value('012500')
    time.sleep(1)

    # 310A
    room_list = driver.find_element(By.NAME, "rm_id")
    room310A = Select(room_list)
    room310A.select_by_value("310A")

    # 날짜
    date = driver.find_element(By.ID, "date")
    date.clear()
    date.send_keys("2024-03-08")

    # 조회
    btnSearch = driver.find_element(By.XPATH, "//input[@type='button'][@value='조회']")
    btnSearch.click()
    time.sleep(1)

    # 예약
    btnReserve = driver.find_element(By.XPATH, "//input[@type='button'][@value='예약 신청'][@name='button']")
    btnReserve.click()
    time.sleep(2)

    # 예약 창으로 driver를 이동
    driver.switch_to.window(driver.window_handles[2])
    useName = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "subject"))
    )
    useName.send_keys("세미나(ll)")
    content = driver.find_element(By.NAME, "content")
    content.send_keys("세미나")

    # 시간 정하기 (10:00 ~ 13:00)
    timeStart_list = driver.find_element(By.NAME, "time_start")
    timeStart = Select(timeStart_list)
    timeStart.select_by_value("10:00")
    timeEnd_list = driver.find_element(By.NAME, "time_end")
    timeEnd = Select(timeEnd_list)
    timeEnd.select_by_value("13:00")

    # 예약
    btnInnerReserve = driver.find_element(By.XPATH, "//input[@type='button'][@value='예약신청'][@name='button']")
    btnInnerReserve.click()
    time.sleep(1)
