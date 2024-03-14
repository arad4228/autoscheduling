from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from autoscheduler import *
import schedule

global lastReservation

def job():
    global lastReservation
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--lang=ko_KR")
    chrome_options.add_argument("--lang=ko")
    # chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option('prefs', {
        "safebrowsing.enabled": True
    })
    strSeminarDay_list = ['화', '금']
    lastReservation = datetime.date.today()

    list_reservation = []
    for day in strSeminarDay_list:
        list_reservation += find_seminar_day_list(day)
    list_reservation.sort()

    for day in list_reservation:
        if day > lastReservation:
            print(f'{len(list_reservation)}개의 예약 중 {day.strftime("%Y-%m-%d")}를 예약합니다.')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            lastReservation = autoscheduling(driver, day, lastReservation)
       

def run_schedule_job():
    today = datetime.date.today().weekday()
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d-%I:%M')} 작업 동작")
    if today == 1 or today == 4:
        job()

if __name__ == '__main__':
    lastReservation = datetime.date.today()
    # 특정 요일 설정(매주 토요일 오후 0:00)
    schedule.every().day.at("00:00").do(run_schedule_job)
    while True:
        schedule.run_pending()
        time.sleep(60)  # 검사 간격을 60초로 설정s