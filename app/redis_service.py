import threading
import time
from app.redis_parser import RedisParser


class RedisService:
    def __init__(self, cache):
        self.rp = RedisParser()
        self.cache = cache

    def handle_request(self, request):
        req = self.rp.decode(request)
        print(f"Processing command {req}")
        command = req[0].upper()
        if command == 'PING':
            return self._ping_response()
        if command == 'ECHO':
            return self._echo_response(req)
        if command == 'SET':
            return self._set_response(req)
        if command == 'GET':
            return self._get_response(req)

    def _set_response(self, req):
        key = req[1]
        value = req[2]
        print(f"Caching key {key} as {value} ")
        self.cache[key] = value
        if time_out := self._is_timed_delete(req):
            print(f"Cache value of key {key} expires in {time_out}ms")
            background_thread = threading.Thread(target=self._remove_from_cache, args=(key, time_out))
            background_thread.start()
        return self.rp.encode_simple_str('OK')

    def _is_timed_delete(self, set_req):
        for i, ele in enumerate(set_req):
            if ele.upper() == 'PX':
                print("Detected timeout arg")
                return set_req[i+1]
        return False

    def _remove_from_cache(self, key, timer=0):
        print(f"Removing {key} from cache after {timer}ms...")
        time.sleep(int(timer)/1000)
        print(f"Removing {key} from cache")
        del self.cache[key]

    def _get_response(self, req):
        print(f"Getting {req}")
        if req[1] in self.cache:
            res = self.cache[req[1]]
            return self.rp.encode_bulk_str(res)
        return self.rp.encode_simple_str("-1")

    def _echo_response(self, req):
        print("Echoing response")
        return self.rp.encode_simple_str(req[1])

    def _ping_response(self):
        print("Respoding to ping")
        return self.rp.encode_simple_str('PONG')
