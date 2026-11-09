import csv
import time
import urllib.robotparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 目标网址（建议换成对爬虫友好的测试站点，如 example.com 或 quotes.toscrape.com）
TARGET_URL = "https://quotes.toscrape.com/"
USER_AGENT = "MySimpleScraper/1.0"


def can_fetch(url, user_agent):
    """检查 robots.txt 是否允许抓取该 URL"""
    rp = urllib.robotparser.RobotFileParser()
    # 拼接 robots.txt 地址
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        print(f"读取 robots.txt 失败：{e}，默认允许抓取")
        return True
    return rp.can_fetch(user_agent, url)

'''


def scrape_titles_and_links(url):
    """请求网页并提取标题与链接"""
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    # 示例：提取所有 h2 标签下的 a 标签（可按目标网页结构调整）
    for h2 in soup.find_all("h2"):
        a_tag = h2.find("a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = a_tag.get("href", "")
            # 把相对链接转成绝对链接
            full_link = urljoin(url, link) if link else ""
            data.append({"title": title, "link": full_link})

    # 如果 h2 里没有链接，至少把标题存下来（适应不同页面结构）
    if not data:
        for h2 in soup.find_all("h2"):
            title = h2.get_text(strip=True)
            if title:
                data.append({"title": title, "link": ""})

    return data 
'''
def scrape_titles_and_links(url):
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print("状态码:", response.status_code)
    print("最终URL:", response.url)
    print("内容长度:", len(response.text))
    print("前500字符:\n", response.text[:500])
    soup = BeautifulSoup(response.text, "html.parser")
    # ===== 临时调试 =====
    print("div.quote 数量:", len(soup.find_all("div", class_="quote")))
    print("small.author 数量:", len(soup.select("small.author")))
    first = soup.find("div", class_="quote")
    print("第一个 quote:", first.prettify()[:600] if first else "None")
    # ====================
    data = []

    # 每条名言是一个 div.quote，作者链接在 .author a
    data = []
    for quote in soup.find_all("div", class_="quote"):
        small = quote.select_one("small.author")
        if not small:
            continue
        title = small.get_text(strip=True)              # 作者名，如 "Albert Einstein"

        # 作者链接是 small 外面的兄弟 <a href="/author/...">，从整个 quote 里找
        a_tag = quote.select_one("a[href^='/author/']")
        link = urljoin(url, a_tag.get("href", "")) if a_tag else ""

        data.append({"title": title, "link": link})

    return data

def scrape_all_pages(start_url, max_pages=10):
    all_data = []
    url = start_url
    for page in range(max_pages):
        if not url:
            break
        all_data.extend(scrape_titles_and_links(url))
        time.sleep(1)                       # 每页之间礼貌等待
        # 找下一页
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        next_a = soup.select_one("li.next a")
        url = urljoin(start_url, next_a["href"]) if next_a else None
        print(f"第 {page+1} 页完成，下一页：{url}")
    return all_data

def save_to_csv(data, filename="scraped_data.csv"):
    """保存为 CSV"""
    if not data:
        print("没有数据可保存。")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(data)
    print(f"已保存 {len(data)} 条数据到 {filename}")


def main():
    # 1. 先看 robots.txt
    if not can_fetch(TARGET_URL, USER_AGENT):
        print("robots.txt 不允许抓取该页面，程序退出。")
        return

    # 2. 抓取
    print(f"开始抓取：{TARGET_URL}")
    data = scrape_titles_and_links(TARGET_URL)
    data1=scrape_all_pages(TARGET_URL)

    # 3. 礼貌等待（如果是循环抓多个页面，在每次请求后加）
    # time.sleep(20)

    # 4. 保存
    save_to_csv(data)
    save_to_csv(data1,'scraped_data1.csv')


if __name__ == "__main__":
    main()