from libs.broker.alpaca.alpaca_session import Alpaca_Session

class Alpaca_Stock_List(Alpaca_Session):
    def __init__(self):
        super().__init__()
        self.init_alpaca_trading_rest()
        print("Loading white-list ... ", end = "", flush = True)
        self.whitelist = self._load_whitelist(self.broker_rest)
        print("OK")

    def _load_whitelist(self, broker):
        assets = broker.list_assets(status = "active")
        
        return [a.symbol for a in assets if a.fractionable and a.tradable and a.status == "active"]

    def get_whitelist(self):
        return self.whitelist

