request_handlers = [] # There should be default 404 matcher for unknown paths

"""
Register function as a http request handler.
Params:
- uri - uri to be matched against request uri
Response dict structure:
{ "result" : Handler method result }
Decorated function signature:
function accepting parsed request and producing response data

"""
def request_handler(uri):
    def decorator(function):
        def wrapper(req): # handler shuld accept parsed req dict and produce result dict
#            print(f"[DEBUG] Running handler for {uri}. Request {req}")
            handled = False
            res = {}
            
            # TODO add uri variables parsing and extend req dict here
            if req["path"].find(uri) == 0: # TODO use real reuest matcher
                print(f"[DEBUG] Handling {uri}")
                res["result"] = function(req) #get response of the function, turn it into string and send to the client
                return res
        request_handlers.append(wrapper)
        return wrapper
    print(f"Registered request handler for {uri}")
    return decorator