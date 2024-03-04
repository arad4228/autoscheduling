from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException
from secrete import *
from sendMail import *
import time
import datetime
import calendar

dictStrToNum = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "일": 6}

def find_seminar_day_list(strDay) -> list:
    currentTime = datetime.datetime.now()
    year = currentTime.year
    month = currentTime.month
    day = currentTime.day
    requirementDay = dictStrToNum[strDay]
    currentDay = calendar.weekday(year, month, day)

    seminar_day_list = []
    diff = (requirementDay - currentDay) % 7
    next_seminar_day = currentTime + datetime.timedelta(days=diff)

    # 첫 번째 가능한 세미나 날짜가 현재 날짜로부터 14일 이내인 경우 추가
    if (next_seminar_day - currentTime).days <= 14:
        seminar_day_list.append(next_seminar_day)
    
    # 두 번째 가능한 세미나 날짜 (다음 주) 추가 검사
    next_next_seminar_day = next_seminar_day + datetime.timedelta(days=7)
    if (next_next_seminar_day - currentTime).days <= 14:
        seminar_day_list.append(next_next_seminar_day)
    
    return seminar_day_list


def skipHTTPSError(driver: webdriver):
    # 자동화도구가 너무 빨라 10초간 대기
    time.sleep(10)

    driver.switch_to.window(driver.window_handles[1])
    # 버튼이 보이고, 누를수 있을 때까지 대기.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "proceed-button")))
    btnIgnore = WebDriverWait(driver, 4).until(
        EC.visibility_of_element_located((By.ID, "proceed-button"))
    )
    btnIgnore.click()


def repeatReservation(driver: webdriver, reserve_date):
    settingStartTime_list = ["10:00", "13:00"]
    settingEndTime_list = ["13:00", "16:00"]
    
    reserve_window = driver.current_window_handle

    for start, end in zip(settingStartTime_list, settingEndTime_list):
        # JSP에서 데이터를 잃어버림으로 인해 다시 로딩
        manual_search_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='rm_reserve_control1_all.jsp']"))
        )
        manual_search_link.click()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "frame1"))
        )

        building_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "blid"))
        )
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
        date.send_keys(reserve_date)

        # 조회
        btnSearch = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button'][@value='조회']"))
        )
        btnSearch.click()

        # 예약
        btnReserve = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button'][@value='예약 신청'][@name='button']"))
        )
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

        # 시간 설정
        timeStart_list = driver.find_element(By.NAME, "time_start")
        timeStart = Select(timeStart_list)
        timeStart.select_by_value(start)
        timeEnd_list = driver.find_element(By.NAME, "time_end")
        timeEnd = Select(timeEnd_list)
        timeEnd.select_by_value(end)

        # 예약
        btnInnerReserve = driver.find_element(By.XPATH, "//input[@type='button'][@value='예약신청'][@name='button']")
        btnInnerReserve.click()
        driver.close()
        driver.switch_to.window(reserve_window)
        time.sleep(2)

    # 모든 창 종료
    driver.quit()

def autoscheduling(driver: webdriver, strDay, lastReservation):
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
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    # new_tab = [tab for tab in driver.window_handles if tab != original_window]
    try:
        skipHTTPSError(driver)

        repeatReservation(driver, strDay.strftime("%Y-%m-%d"))
        return strDay

    except WebDriverException as e:
        print(e)
        sendEmail(Mail_Address, e)
        driver.quit()