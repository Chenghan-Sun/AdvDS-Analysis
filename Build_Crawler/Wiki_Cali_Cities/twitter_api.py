import json
from utils import Http, Db
from bs4 import BeautifulSoup


class TwitterAPI:

    def __init__(self):
        column_n_desired = list(range(0, 8))
        column_n_desired.remove(6)
        self.__column_id_desired = ["column%d" % n for n in column_n_desired]

        self.__leader_spec = dict()
        self.__leader_event_apis = dict()

        self.__base_event_api = ""
        self.__base_insert_sql = "INSERT INTO events VALUES(NULL,'%s','%s','%s');"

        self.__db = Db()

    def __load_and_insert_events_from_json_apis(self, apis_list):
        ret_count = 20
        for api in apis_list:
            page_no = 1
            last_ret = False

            while not last_ret:
                _, ret = Http.get(api % (page_no, ret_count))

                data = json.loads(ret[1:-1], encoding="utf-8")
                if data["status"] is 0:
                    articles = data["data"]["list"]
                    if len(articles) is not ret_count:
                        last_ret = True

                    for article in articles:
                        title = article["Title"]
                        datetime = article["PubTime"]
                        abstract = article["Abstract"]

                        self.__db.execute(self.__base_insert_sql % (datetime, Db.escape(title), Db.escape(abstract)))
                        print("Event: %s" % title)

                        page_no += 1
                else:
                    last_ret = True


