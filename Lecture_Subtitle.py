import selenium
from selenium.webdriver import Chrome  # Chrome Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
import helper

URL = "https://34.64.184.185:8000/"


def get_files(dir_path: str, start_index: int) -> list[str]:
    """로컬에서 영상 파일을 모두 불러오기"""

    file_list = os.listdir(path=dir_path)
    file_list.sort()
    file_list = file_list[start_index:]

    print("업로드할 파일 목록")
    for file in file_list:
        print(file)

    # 유저 입력으로 확인 받기
    if not input("계속하려면 y 입력:") == "y":
        print("프로그램 종료")
        exit()

    return file_list


# region driver actions


def setup() -> Chrome:
    """최초 Driver 설정"""

    options = selenium.webdriver.chrome.options.Options()
    # options.add_argument("headless") # 브라우저 창을 띄우지 않고 실행
    # 웹페이지가 SSL을 사용하지 않을 경우 에러가 생기는듯
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    # 그냥 짜증나는 로그 꺼줌
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 함수에서 Driver를 실행할 경우, 함수가 끝나고 scope가 닫히면 브라우저 창이 꺼짐. 방지하기
    options.add_experimental_option("detach", True)

    driver = Chrome(options=options)
    driver.implicitly_wait(10)  # 특정 요소가 로딩될 때까지 기다리기

    driver.get(url=URL)
    return driver


def login(driver: Chrome):
    """로그인 스크립트"""

    driver.find_element(by=By.NAME, value="username").send_keys(dotenv)
    driver.find_element(by=By.NAME, value="password").send_keys(dotenv)
    driver.find_element(by=By.XPATH, value="//input[@type='submit']").submit()


def submit_file(driver: Chrome, file_url: str):
    Select(driver.find_element(by=By.ID, value="id_language")).select_by_value("en-US")
    Select(driver.find_element(by=By.ID, value="id_spec")).select_by_value("Science")

    driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(file_url)

    # submit이 자동으로 popup이 사라질 때까지 기다려줬다.
    helper.only_one(
        # 단 하나의 버튼을 찾은 뒤, submit()
        filter(
            lambda element: element.text == "Create Subtitle",
            driver.find_elements(by=By.XPATH, value="//button[@type='submit']"),
        )
    ).submit()


# endregion


if __name__ == "__main__":

    dir_path = "C:/Data/영문자막인턴/원본 영상"
    lecture_num = 1
    file_list = get_files(dir_path=dir_path, start_index=lecture_num - 1)

    driver = setup()
    login(driver)

    for file_name in file_list:
        submit_file(driver, file_url=dir_path + "/" + file_name)
