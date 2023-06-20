def error_formator(errors):
    error_list = []
    print(errors)
    for field_name, field_errors in errors.items():
        new_error = {}
        new_error[field_name] = str(field_errors[0])
        error_list.append(new_error)
    return error_list


def api_response(code,data,message,errors):
    res = {}
    res['code'] = code
    res['data'] = data
    res['message'] = message
    res['errors'] = errors
    return res


def check_auth(request):
    try:
        encoded_jwt = request.headers['Authorization']
        a = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        return True, a['user_id']
    except Exception as e:
        print(e)
        return False, 0