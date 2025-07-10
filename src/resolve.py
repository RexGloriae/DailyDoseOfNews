from euronews import EuroNews
from hotnews import HotNews
from protv import ProTV
from logs import *

def load_articles():
    print("[INFO] Initializing EuroNews...")
    logging.info("Initializing EuroNews...")
    ch_euro = EuroNews()
    print("[INFO] Initializing HotNews...")
    logging.info("Initializing HotNews...")
    ch_hot = HotNews()
    print("[INFO] Initializing ProTV...")
    logging.info("Initializing ProTV")
    ch_pro = ProTV()

    ch_euro.fetch_articles()
    ch_hot.fetch_articles()
    ch_pro.fetch_articles()

    print("[INFO] All articles have been fetched successfully...")
    logging.info("Articles fetches successfully...")
    print("[EXIT] All jobs were executed - exiting...")
    logging.info("Succesfully exiting...")