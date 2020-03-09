import pymysql
import requests
import time
import sys
from urllib import parse


class Db:
    host = "localhost"
    user = "root"
    password = "skrskr220"
    db = "events_from_twitter_api"
    charset = "UTF-8"

    def __init__(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except pymysql.Error:
            self.conn.rollback()
            print(sql)

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def escape(s):
        if "'" in s:
            s = s.replace("'", "''")
        return s


class Http:

    class TimeoutError(Exception):

        def __init__(self, timeout):
            err = "Empty response after %d seconds." % timeout
            Exception.__init__(self, err)
            print(err)

    class UnknownError(Exception):

        def __init__(self):
            err = "Request failed."
            Exception.__init__(self, err)
            print(err)

    @staticmethod
    def get(url, encoding="UTF-8", timeout=10, anonymous=False):

        if anonymous:
            while True:
                try:
                    r = requests.get(url, headers={
                        'authorization: OAuth '
                        'oauth_consumer_key="consumer-key-for-app", '
                        'oauth_nonce="generated-nonce", '
                        'oauth_signature="generated-signature", '
                        'oauth_signature_method="HMAC-SHA1", '
                        'oauth_timestamp="generated-timestamp", '
                        'oauth_token="access-token-for-authed-user", '
                        'oauth_version="1.0"'},
                                     timeout=timeout, proxies=Http.proxy())
                    r.encoding = encoding
                    return r.status_code, r.text
                except requests.exceptions.Timeout:
                    print("Empty response after %d seconds. Retrying with another proxy..." % timeout, flush=True)
                    time.sleep(0.2)


class SearchApi:

    def __init__(self):
        self._db = Db()

    def __del__(self):
        self._db.close()

    def __get_batch(self, fields_str, table, offset, batch_size):
        last_batch = False
        sql = "SELECT %s FROM %s LIMIT %d,%d;" % (fields_str, table, offset, batch_size)

        self._db.execute(sql)
        res = self._db.fetch_all()
        if len(res) < batch_size:
            last_batch = True

        batch = list()
        for tup in res:
            batch.append(tup)

        return batch, last_batch


class ProgressBar:

    def __init__(self, total, headline, bar_length=100):
        self.total = total
        self.bar_length = bar_length
        self.digits = len(str(self.total))

        print("\n%s" % headline)

    def refresh(self, progress):
        percent = progress / self.total

        hashes = '#' * int(percent * self.bar_length)
        spaces = ' ' * (self.bar_length - len(hashes))

        sys.stdout.write("\r|%s[%.2f%%]%s| %s/%d"
                         % (hashes, percent * 100, spaces, str(progress).rjust(self.digits), self.total))
        sys.stdout.flush()

    def finish(self, report):
        print("%s (total: %d)\n" % (report, self.total))
