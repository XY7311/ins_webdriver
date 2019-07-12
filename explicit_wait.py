'''
封装webdriver等待
https://www.cnblogs.com/kevin-liutianping/p/9967792.html
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# wait = WebDriverWait(driver,10,0.5)
# wait.until(EC.presence_of_element_located((By.ID,'KW')))

def explicit_wait(driver, track, ec_params, timeout=35, notify=True):
    # isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
    if not isinstance(ec_params, list):
        ec_params = [ec_params]

    # find condition according to the tracks
    # 判断某个元素是否被添加到了dom里并且可见
    if track == "VOEL":
        elem_address, find_method = ec_params
        #xpath后      #xpath/css/class_name
        ec_name = "visibility of element located"

        find_by = (By.XPATH if find_method == "XPath" else
                   By.CSS_SELECTOR if find_method == "CSS" else
                   By.CLASS_NAME)
        locator = (find_by, elem_address)
        condition = EC.visibility_of_element_located(locator)

    # 判断title是否与包含预期值,返回布尔值
    elif track == "TC":
        expect_in_title = ec_params[0]
        ec_name = "title contains '{}' string".format(expect_in_title)

        condition = EC.title_contains(expect_in_title)
    
    # 等待某个元素从dom树中移除
    elif track == "SO":
        ec_name = "staleness of"
        element = ec_params[0]
        condition = EC.staleness_of(element)

    # generic wait block
    try:
        wait = WebDriverWait(driver, timeout)
        result = wait.until(condition)

    except:
        if notify is True:
            print(
                "Timed out with failure while explicitly waiting until {}!\n"
                .format(ec_name))
        return False

    return result

