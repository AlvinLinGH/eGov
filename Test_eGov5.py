from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys

myCourse = []

def eGovScrapying():
    eGov_Login = 'https://www.cp.gov.tw/portal/Clogin.aspx?ReturnUrl=https%3A%2F%2Felearn.hrd.gov.tw%2Fegov_login.php'
    eGov_Course = "https://elearn.hrd.gov.tw/mooc/user/mycourse.php"

    dirverPath=r"chromedriver.exe"
    browser = webdriver.Chrome(dirverPath)
    browser.get(eGov_Login)

    #讀取文字文件 第一行是密 第二行是帳號
    userInfo = open("userInfo.txt")
    PassW = userInfo.readline()
    Account = userInfo.readline()

    eGovAccount = browser.find_element_by_id("ctl00_ContentPlaceHolder1_AccountPassword1_txt_account")
    eGovPassWord = browser.find_element_by_id("ctl00_ContentPlaceHolder1_AccountPassword1_txt_password")
    eGovAccount.clear()
    eGovPassWord.clear()
    eGovAccount.send_keys(Account)
    eGovPassWord.send_keys(PassW)

    # loginSubmit = browser.find_element_by_id("ctl00_ContentPlaceHolder1_AccountPassword1_btn_LoginHandler")
    # loginSubmit.click()

    time.sleep(3)
    #讀取個人資料及關掉視窗

    #fancybox-outer個人上課資訊
    alertTxt = browser.find_element_by_class_name("fancybox-outer")
    print(alertTxt.text)
    time.sleep(1)
    alertClsoe = browser.find_element_by_class_name("fancybox-item")
    alertClsoe.click()

    #WebDriverWait(browser, 1800, 600).until(EC.title_contains("行政院人事行政總處、公務人員數位學習、e等公務園+學習平臺")) ###
    eGovTitle = browser.title
    print(eGovTitle)
    #WebDriverWait(browser, 1800, 600).until(EC.title_contains(eGovTitle))  ###
    browser.get(eGov_Course)
    time.sleep(3)

    #抓取訊息
    #ml15 課程名稱
    #info 課程資訊
    #fb   藉由FB來抓取上課網址
    allCourse = browser.find_elements_by_class_name("ml15")
    courseInfo = browser.find_elements_by_class_name("info")
    allLink = browser.find_elements_by_class_name("fb")

    i = 0
    courseList = []

    for course in allCourse:
        print("課程 :",course.text)
        # print("ABC :",course)
        # print("Test ",courseInfo[i].text)
        if "尚未通過" in courseInfo[i].text:
            print("尚未通過")
            # print("courseInfo :",courseInfo[i].text)
            print("需要上課幾小時 :", courseInfo[i].text[42:43],"小時")
            #用get_attribute獲取裡面的屬性並抓取字串上課的網址
            print("TEST :",allLink[i].get_attribute("href")[-45:-6])
            courseList.append(allLink[i].get_attribute("href")[-45:-6])

        # else:
        #     print("已通過")

        #print("ABC :",icStar[i].id)
        i+=1

    # print("共幾堂課沒有上完 :",len(courseList))
    # for startCourse in courseList:
    #     browser.execute_script(startCourse)

    #=============單一課程資訊頁

    browser.get(courseList[0])
    print("courseList[0] :",courseList)
    courseTime = browser.find_element_by_class_name("majorstatus")
    print("courseTime :",courseTime.text)
    #browser.execute_script(courseList[0])
    time.sleep(2)

    btnAction = browser.find_element_by_class_name("btnAction")
    btnAction.click()
    time.sleep(3)

    #跳換到frame視窗-大視窗
    browser.switch_to.frame("s_catalog")
    # print(browser.page_source)
    #小視窗-課程選項
    browser.switch_to.frame("pathtree")

    #frame : mooc_sysbar 最左邊的視窗 (開始上課、測驗考試、.....)
    #frame : mooc_header 最上面的視窗 (我的課程、離開課程、.....)

    cssAnchor1 = browser.find_elements_by_class_name("cssAnchor1") #
    # print("cssAnchor1 :", len(cssAnchor1))
    cssAnchor1[2].click()

    #每隔20分種，重新連線
    try:
        WebDriverWait(browser, 600, 60).until(EC.title_contains(eGovTitle))
        # print("Restart :",browser.title)
    except:
        print("Error :", sys.exc_info()[0])
        # print("Title :",browser.title)
        #browser.close()

    eGovScrapying()

#================
eGovScrapying()

















