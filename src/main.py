from euronews import EuroNews
from hotnews import HotNews
from protv import ProTV
from database import Database

def main():
    print("[INFO] Initializing EuroNews...")
    ch_euro = EuroNews()
    print("[INFO] Initializing HotNews...")
    ch_hot = HotNews()
    print("[INFO] Initializing ProTV...")
    ch_pro = ProTV()

    ch_euro.fetch_articles()
    ch_hot.fetch_articles()
    ch_pro.fetch_articles()

    print("[INFO] All articles have been fetched successfully...")

    print("[INFO] Trying to fill missing descripitons...")
    Database().fill_missing_descriptions()

    print("[EXIT] All jobs were executed - exiting...")

if __name__ == "__main__":
    main()