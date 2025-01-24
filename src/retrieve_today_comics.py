# -*- coding: utf-8 -*-
"""本日発売のお気に入りコミックを抽出する"""

# ライブラリのインポート
import datetime
import re
from typing import Optional

import bs4
import requests

TARGET_URL = "https://comic.sumikko.info/date-item/"  # 本日発売コミック新刊
FAVORITE_TITLES = ["ウォーズ", "スーパー"]  # お気に入りのコミックタイトル


def get_soup_from_url(url: str) -> bs4.BeautifulSoup:
    """URLからBeautifulSoupオブジェクトを取得する

    Args:
        url (str): 取得対象のURL

    Returns:
        bs4.BeautifulSoup: BeautifulSoupオブジェクト
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # 取得失敗時には、例外を発生する
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print("スクレイピングに失敗しました: ", e)


def convert_date(date_str: str) -> Optional[datetime.date]:
    """日付形式の文字列をdatetime.dateオブジェクトに変換する

    Args:
        date_str (str): 日付形式の文字列（例: "1月4日"）

    Returns:
        Optional[datetime.date]: dste_strが正しい形式の場合はdatetime.dateオブジェクト、そうでない場合はNone
    """
    # 現在の年を取得
    current_year = datetime.datetime.now().year

    # 正規表現で「1月4日」の部分を抽出
    match = re.match(r"(\d+)月(\d+)日", date_str)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))

        # datetimeオブジェクトを作成
        result = datetime.date(current_year, month, day)
        return result
    else:
        return None


def extract_title(soup: bs4.BeautifulSoup) -> list:
    """BeautifulSoupオブジェクトからコミックタイトルを抽出する

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoupオブジェクト

    Returns:
        list: コミックタイトルのリスト
    """
    titles = []
    items = soup.find_all("li", attrs={"class": "item"})
    for item in items:
        titles.append(item.find("div", attrs={"class": "name"}).text)

    return titles


def retrieve_today_comics() -> list:
    """本日発売のコミック一覧を取得する

    Returns:
        list: 本日発売のコミック一覧
    """
    soup = get_soup_from_url(TARGET_URL)
    titles = extract_title(soup)
    # print("\n".join(titles))  # デバッグ用: 取得した全コミック一覧を表示

    filtered_titles = [
        title
        for title in titles
        if any(favorite in title for favorite in FAVORITE_TITLES)
    ]
    return filtered_titles


if __name__ == "__main__":
    print("本日発売のコミック一覧")
    items = retrieve_today_comics()
    print("\n".join(items))
