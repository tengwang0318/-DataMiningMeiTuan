from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import csv


class Crawler:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def log_in(self, url):

        self.browser.get(url)

        time.sleep(10)
        telephone = self.browser.find_element_by_xpath('/html/body/div[2]/div[7]/div[1]/input')

        telephone.send_keys('18291893261')
        time.sleep(2)
        classify_code = self.browser.find_element_by_xpath('/html/body/div[2]/div[7]/div[1]/div/span')
        classify_code.click()
        code = input("Please enter the classify code:")
        password = self.browser.find_element_by_xpath('/html/body/div[2]/div[7]/div[2]/input')
        password.send_keys(str(code))
        time.sleep(random.randint(8, 10))
        login = self.browser.find_element_by_xpath('/html/body/div[2]/div[7]/div[3]/button[2]')
        login.click()
        time.sleep(random.randint(5, 10))



    def location(self):
        loc = self.browser.find_element_by_xpath('/html/body/mieta/div[1]/div/div/div/div/div/div/div[1]/div[1]')
        loc.click()
        time.sleep(10)
        loc_again = self.browser.find_element_by_xpath(
            '/html/body/mieta/div[1]/div/div/div/div/div/div/div/div[2]/div/p[2]/span')
        loc_again.click()
        time.sleep(10)

    # def scroll_the_window(self):
    #     all_window_heights = []
    #     all_window_heights.append(self.browser.execute_script("return document.body.scrollHeight;"))
    #     while True:
    #         self.browser.execute_script('scroll(0,10000)')
    #         time.sleep(random.randint(5, 10))  # 随机数避免被检测出是爬虫
    #         check_height = self.browser.execute_script("return document.body.scrollHeight;")
    #         if check_height == all_window_heights[-1]:
    #             print("已经到了浏览器底层")
    #             break
    #         else:
    #             all_window_heights.append(check_height)
    #             print("正在下拉浏览器")
    def scroll_the_window(self):
        js = "return action=document.body.scrollHeight"
        height = self.browser.execute_script(js)

        # 将滚动条调整至页面底部
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)

        # 定义初始时间戳（秒）
        t1 = int(time.time())

        # 定义循环标识，用于终止while循环
        status = True

        # 重试次数
        num = 0

        while status:
            # 获取当前时间戳（秒）
            t2 = int(time.time())
            # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
            if t2 - t1 < 30:
                new_height = self.browser.execute_script(js)
                if new_height > height:
                    time.sleep(1)
                    self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    # 重置初始页面高度
                    height = new_height
                    # 重置初始时间戳，重新计时
                    t1 = int(time.time())
            elif num < 3:  # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
                time.sleep(3)
                num = num + 1
            else:  # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
                print("滚动条已经处于页面最下方！")
                status = False
                # 滚动条调整至页面顶部
                self.browser.execute_script('window.scrollTo(0, 0)')
                break

    def get_source(self):
        html = self.browser.page_source
        html = html.encode('utf8')
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        self.save_data(soup)

    def save_data(self, soup):
        # 确定用的那个css字体

        file = soup.find('body').find('style').text
        file_name = file[-17:-4]
        # print(file)
        a_list = soup.find(class_="_14I_ga12izfkrbg8LnpHcW").find_all('li')

        for item in a_list:
            time.sleep(2)
            name = item.find(class_='_1DtOrxweBD8MIzOOrhn9cs').text
            print("name:", name)
            sales = item.find(class_="_257aD1mYh6bWz4bmXz3DSv _3fbi7-DiA-2q0ecYl1bi2j mtsi-num").string[2:-1]

            print("sales:", sales)
            final_sales = ""
            for temp in sales:
                final_sales += num_map[file_name][temp]
                print(num_map[file_name][temp], end="")
            print("\n")

            send_time = item.find(class_="_3fbi7-DiA-2q0ecYl1bi2j mtsi-num").string[:-2]
            final_send_time = ""
            print("send_time:", send_time)
            for temp in send_time:
                final_send_time += num_map[file_name][temp]
                print(num_map[file_name][temp], end="")
            print("\n")
            distance = item.find(class_="_3fbi7-DiA-2q0ecYl1bi2j _2vTtS2LuUOARC19vNowA9w mtsi-num").string
            if distance[-2] == "k":
                distance = distance[:-2]
            else:
                distance = distance[:-1]
            final_distance = ""
            print("distance:", distance)
            for temp in distance:
                if temp == ".":
                    final_distance += "."
                    print(".", end="")
                else:
                    final_distance += num_map[file_name][temp]
                    print(num_map[file_name][temp], end='')
            print("\n")
            starting_price = item.find(class_="_3DcMzS2xKx7PfzNq_sUnxn").find(
                class_='_3fbi7-DiA-2q0ecYl1bi2j mtsi-num').string[4:]
            final_start_price = ""
            print("start_price:", starting_price)
            for temp in starting_price:
                print(num_map[file_name][temp], end="")
                final_start_price += num_map[file_name][temp]
            print('\n')
            delivery_price = item.find(class_="_3DcMzS2xKx7PfzNq_sUnxn").find_all(
                class_="_3fbi7-DiA-2q0ecYl1bi2j _2vTtS2LuUOARC19vNowA9w mtsi-num")[0].string
            print(delivery_price)
            final_delivery_price = ""
            if delivery_price == "免配送费":
                delivery_price = 0
                print("delivery_price:", delivery_price)
                final_delivery_price += "0"
            else:
                delivery_price = delivery_price[4:]
                print("delivery_price:", delivery_price)
                for temp in delivery_price:
                    if temp == ".":
                        final_delivery_price += "."
                        print(".")
                    else:
                        print(num_map[file_name][temp], end="")
                        final_delivery_price += num_map[file_name][temp]
                print("\n")
            final_mean_price = ""
            try:
                mean_price = item.find(class_="_3DcMzS2xKx7PfzNq_sUnxn").find_all(
                    class_='_3fbi7-DiA-2q0ecYl1bi2j _2vTtS2LuUOARC19vNowA9w mtsi-num')[1].string[4:]
                print("mean_price:", mean_price)
                for temp in mean_price:
                    final_mean_price += num_map[file_name][temp]
                    print(num_map[file_name][temp], end="")
                print("\n")
            except:
                mean_price = 0
                print("mean_price:", mean_price)
                final_mean_price += "0"

            score = item.find(class_="_3fbi7-DiA-2q0ecYl1bi2j _3xfmNN1n12Gov71h-3rfhp").string
            final_score = str(score)
            print("score:", score)
            with open('meituan.csv', 'a+', newline='', encoding='utf-8-sig')as f:
                writer = csv.writer(f)
                writer.writerow(
                    [name, final_sales, final_send_time, final_distance, final_start_price, final_delivery_price,
                     final_mean_price, final_score])


num_map = {'08220675.woff': {'\ue0f9': '9', '\ue275': '2', '\ue13e': '4', '\uf785': '0', '\ue5c7': '1', '\uf8f9': '5',
                             '\uf8fc': '7',
                             '\ue060': '6', '\ue6c0': '3', '\uf140': '8'},
           '5f0be5ce.woff': {'\ue350': '9', '\ue4d4': '6', '\uf005': '5', '\uf56f': '2', '\ue97b': '1', '\ue458': '0',
                             '\ue5e0': '4',
                             '\ue379': '8', '\ue3fc': '7', '\ueb7b': '3'},
           '8a16e02d.woff': {'\uf80c': '3', '\ue196': '9', '\ue7ba': '5', '\ue04c': '8', '\uf41d': '2', '\ue92a': '7',
                             '\ue9cf': '6',
                             '\ue3c9': '1', '\ue340': '0', '\ued8b': '4'},
           'c722c643.woff': {'\uee40': '2', '\uf117': '8', '\uf3e7': '6', '\uebc4': '7', '\ue990': '0', '\ueb02': '3',
                             '\uef32': '1',
                             '\ueed7': '9', '\uec2e': '5', '\ue518': '4'},
           'd2324528.woff': {'\ue703': '7', '\ue8c2': '9', '\ue5b9': '5', '\ue199': '3', '\ue168': '2', '\uf34f': '6',
                             '\ue14f': '8',
                             '\uead7': '1', '\ue9d3': '0', '\uf80a': '4'},
           '26454aeb.woff': {'\ue426': '9', '\ue13b': '6', '\ueae8': '3', '\uee88': '4', '\uf553': '0', '\uf8a6': '7',
                             '\uf8d8': '2',
                             '\uf08d': '5', '\uf198': '1', '\ued18': '8'},
           'b3b7ee0d.woff': {'\ue69f': '2', '\uf58f': '0', '\uf170': '4', '\uf0ea': '5', '\ue391': '1', '\ue1be': '9',
                             '\uf4fa': '7',
                             '\ueb13': '6', '\ue1dd': '3', '\uf79f': '8'},
           '7e941ac2.woff': {'\ued9a': '7', '\ue7a5': '5', '\ue641': '0', '\ueb24': '6', '\uf4fd': '1', '\ue306': '9',
                             '\ue3a5': '8',
                             '\uf62e': '2', '\uf484': '4', '\uef14': '3'},
           'd2f7b57f.woff': {'\ue163': '2', '\uea95': '1', '\ueff2': '3', '\ue5f2': '0', '\uf1c9': '5', '\uf0ef': '8',
                             '\uea41': '6',
                             '\ue3b5': '9', '\ue85a': '4', '\uf0fc': '7'},
           'd308c5b0.woff': {'\uebd3': '6', '\ue716': '0', '\uf3b7': '5', '\ue62a': '9', '\uec06': '7', '\ue76b': '8',
                             '\uefca': '4',
                             '\uf4af': '2', '\uee0c': '3', '\ueb02': '1'}}

if __name__ == '__main__':
    with open('meituan.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['name', 'sales', 'send_time', 'distance', 'start_price', 'delivery_price', 'mean_price', 'score'])

    crawler = Crawler()
    crawler.log_in(
        'https://h5.waimai.meituan.com/waimai/mindex/kingkong?navigateType=910&firstCategoryId=910&secondCategoryId=910&title=%E7%BE%8E%E9%A3%9F')
    # crawler.log_in('https://h5.waimai.meituan.com/waimai/mindex/home')
    time.sleep(240)
    # crawler.scroll_the_window()
    crawler.get_source()
