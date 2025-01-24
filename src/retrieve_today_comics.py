# -*- coding: utf-8 -*-
"""本日発売のお気に入りコミックを抽出する"""

# ライブラリのインポート
import bs4
import requests


class ComicScraper:
    TARGET_URL = "https://comic.sumikko.info/date-item/"  # 本日発売コミック新刊
    FAVORITE_TITLES = ["ウォーズ", "スーパー"]  # お気に入りのコミックタイトル

    def __init__(self):
        pass

    def get_soup_from_url(self, url: str) -> bs4.BeautifulSoup:
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
        except requests.exceptions.RequestException:
            return None

    def extract_title(self, soup: bs4.BeautifulSoup) -> list:
        """BeautifulSoupオブジェクトからコミックタイトルを抽出する

        Args:
            soup (bs4.BeautifulSoup): BeautifulSoupオブジェクト

        Returns:
            list: コミックタイトルのリスト
        """
        comic_titles = [
            item.find("div", attrs={"class": "name"}).text
            for item in soup.find_all("li", attrs={"class": "item"})
        ]
        return comic_titles

    def retrieve_today_comics(self) -> list:
        """本日発売のコミック一覧を取得する

        Returns:
            list: 本日発売のコミック一覧
        """
        soup = self.get_soup_from_url(self.TARGET_URL)
        if soup is None:
            return []

        comic_titles = self.extract_title(soup)
        # print("\n".join(comic_titles))  # デバッグ用: 取得した全コミック一覧を表示

        filtered_titles = [
            title
            for title in comic_titles
            if any(favorite in title for favorite in self.FAVORITE_TITLES)
        ]
        return filtered_titles


if __name__ == "__main__":
    print("本日発売のコミック一覧")
    items = ComicScraper().retrieve_today_comics()
    print("\n".join(items))
