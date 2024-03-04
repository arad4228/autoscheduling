from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from autoscheduler import *
import schedule


def job():
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--lang=ko_KR")
    chrome_options.add_argument("--lang=ko")
    # chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option('prefs', {
        "safebrowsing.enabled": True
    })

    strSeminarDay = '금'
    lastReservation = None

    list_reservation = find_seminar_day_list(strSeminarDay)

    for day in list_reservation:
        if day < lastReservation:
            continue
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        lastReservation = autoscheduling(driver, day, lastReservation)

if __name__ == '__main__':
    # 특정 요일 설정(매주 금요일 오후 0:00)
    schedule.every().friday.at("00:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # 검사 간격을 60초로 설정
