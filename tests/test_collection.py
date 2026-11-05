import unittest
from tributary.collect import initial, run


class CollectionTests(unittest.TestCase):
    def test_failure_then_recovery_preserves_cursor_and_history(self):
        state = initial()
        src = [{"id":"irs","url":"test","geography":"WA"}]
        body = b"EIN,NAME,CITY,STATE,TAX_PERIOD\n911090450,FOOD LIFELINE,SEATTLE,WA,202506\n"
        run(state,src,lambda *_: (200,body,{"etag":"a"}))
        previous = state["sources"]["irs"].copy()
        for code, outcome in [(503,"failed"), (403,"blocked"), (200,"failed")]:
            run(state,src,lambda *_: (code,b"invalid",{}))
            self.assertEqual(state["runs"][-1]["attempts"][0]["outcome"],outcome)
            for key in ("last_success","checkpoint"):
                self.assertEqual(state["sources"]["irs"][key],previous[key])
        def unchanged(url, checkpoint):
            self.assertEqual(checkpoint["etag"],"a")
            return 304,b"",{}
        run(state,src,unchanged)
        self.assertEqual(state["runs"][-1]["attempts"][0]["outcome"],"unchanged")
        run(state,src,lambda *_: (200,body.replace(b"202506",b"202606"),{}))
        self.assertEqual(len(state["items"]["irs/911090450"]),2)
        self.assertEqual(state["runs"][-1]["new_accounts"],[])
