from euronews import EuroNews
from hotnews import HotNews
from protv import ProTV

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

if __name__ == "__main__":
    main()