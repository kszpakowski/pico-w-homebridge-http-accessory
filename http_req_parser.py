def parse_raw_request(req):

    parsed = {}
    lines = req.split("\n")
    reqLine = lines[0]
    method_separator_index = reqLine.index(" ")
    http_version_separator_index = reqLine.index(" ",method_separator_index+1) 
    parsed["method"] = reqLine[:method_separator_index]
    parsed["version"] = reqLine[http_version_separator_index+1:]
    path_and_params = reqLine[method_separator_index+1:http_version_separator_index]
    params_separator_index = path_and_params.find("?")
    has_params = params_separator_index >= 0
    parsed["path"] = path_and_params[:params_separator_index] if has_params else path_and_params
    if has_params:
        params = {}
        paramsArr = path_and_params[params_separator_index+1:].split("&")
        for param in paramsArr:
            kv = param.split("=")
            params[kv[0]]=kv[1]
        parsed["params"]=params
    
    return parsed
    