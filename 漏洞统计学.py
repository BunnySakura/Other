import requests
from bs4 import BeautifulSoup
from tqdm import trange


class GetBugInfo(object):
    """获取指定关键字的漏洞数量及危害等级。

    Attributes:
        keyword: 搜索关键字。
        date_begin: 搜索的起始时间。
        date_end: 搜索的终止时间。
    """

    def __init__(self, keyword: str, date_begin: str, date_end: str):
        """获取参数以初始化类。

        Args:
            keyword: 搜索关键字。
            date_begin: 搜索的起始时间。
            date_end: 搜索的终止时间。
        """
        self.keyword = keyword
        self.date_begin = date_begin
        self.date_end = date_end

    def get_url_from_one_page(self, page: str) -> list:
        """从一页搜索结果获取URL。

        Args:
            page: 页码。

        Returns:
            包含一页搜索结果的URL的列表。
        """
        url = "http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno=" + page + "&repairLd="
        data = {
            "CSRFToken": "",
            "cvHazardRating": "",
            "cvVultype": "",
            "qstartdateXq": "",
            "cvUsedStyle": "",
            "cvCnnvdUpdatedateXq": "",
            "cpvendor": "",
            "relLdKey": "",
            "hotLd": "",
            "isArea": "",
            "qcvCname": self.keyword,
            "qcvCnnvdid": "CNNVD或CVE编号",
            "qstartdate": self.date_begin,
            "qenddate": self.date_end,
        }
        result_list = []  # 返回的URL结果列表

        get_html = requests.post(url=url, data=data, )
        parsing_html = BeautifulSoup(get_html.text, "html.parser")
        parsing_html_find_a_title2 = str(parsing_html.find_all(class_="a_title2")).split()
        for i in parsing_html_find_a_title2:
            if 'href' in i:
                get_url = "http://www.cnnvd.org.cn" + i.split("\"")[1]
                result_list.append(get_url)
        return result_list

    def get_url_from_all_page(self) -> list:
        """从所有结果获取URL。

        Returns:
            包含所有搜索结果的URL的列表。
        """
        result_list = []  # 返回的URL结果列表

        for page in range(1, 999):
            one_page_list = self.get_url_from_one_page(str(page))
            print(one_page_list)
            if not one_page_list:
                result_list.extend(one_page_list)
                break
            else:
                result_list.extend(one_page_list)
        return result_list

    def get_level(self, url: str):
        """获取危害等级。

        Args:
            url: 漏洞信息的链接。

        Returns:
            无。
        """
        table = {
            "/web/images/jb_0.png": "未分级",
            "/web/images/jb_1.png": "低危",
            "/web/images/jb_2.png": "中危",
            "/web/images/jb_3.png": "高危",
            "/web/images/jb_4.png": "超危",
        }
        get_html = requests.get(url=url)
        parsing_html = BeautifulSoup(get_html.text, "html.parser").find_all(border="0")[0]
        level_key = str(parsing_html).split("\"")[-2]
        return table[level_key]


if __name__ == "__main__":
    keyword = input("请输入搜索关键词：")
    date_begin = input("以此格式\"2017 - 03 - 15\"输入搜索终止时间时间：")
    date_end = input("以此格式\"2022 - 03 - 15\"输入搜索终止时间时间：")
    Bug = GetBugInfo(keyword, date_begin, date_end)
    # Bug = GetBugInfo("smb", "2017 - 03 - 15", "2022 - 03 - 15")
    result_url = Bug.get_url_from_all_page()
    count0 = 0  # 未分级
    count1 = 0  # 低危
    count2 = 0  # 中危
    count3 = 0  # 高危
    count4 = 0  # 超危

    for i in trange(len(result_url)):
        if Bug.get_level(result_url[i]) == "未分级":
            count0 += 1
        elif Bug.get_level(result_url[i]) == "低危":
            count1 += 1
        elif Bug.get_level(result_url[i]) == "中危":
            count2 += 1
        elif Bug.get_level(result_url[i]) == "高危":
            count3 += 1
        elif Bug.get_level(result_url[i]) == "超危":
            count4 += 1

    print(f"漏洞总数：{len(result_url)}")
    print(f"未分级数量：{count0}")
    print(f"低危数量：{count1}")
    print(f"中危数量：{count2}")
    print(f"高危数量：{count3}")
    print(f"超危数量：{count4}")
