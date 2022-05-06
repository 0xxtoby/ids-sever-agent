#url解码
import re
import urllib


def urldecode(param):
    try:
        return urllib.parse.unquote(param)
    except:
        return param
    # 匹配规则库
def match_rule(line, rule):

    sql_inject_pattern = re.compile(rule, re.I | re.M)
    if re.search(sql_inject_pattern, urldecode(line['url'])):
            return True
    return False
def match_rule_str(data_str, rule):

    sql_inject_pattern = re.compile(rule, re.I | re.M)
    if re.search(sql_inject_pattern, urldecode(data_str)):
            return True
    return False


if __name__ == '__main__':
    a={}

    a["url"]='''------WebKitFormBoundarylBhhfkczrccwZ6Jq
Content-Disposition: form-data; name="MAX_FILE_SIZE"

100000
------WebKitFormBoundarylBhhfkczrccwZ6Jq
Content-Disposition: form-data; name="uploaded"; filename="1.php"
Content-Type: text/php

<?php @eval($_POST['Cknife']);?>
------WebKitFormBoundarylBhhfkczrccwZ6Jq
Content-Disposition: form-data; name="Upload"

Upload
------WebKitFormBoundarylBhhfkczrccwZ6Jq--

'''

    print(match_rule_str(a["url"],"\b(and|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|declare|or)\b|(\*|;|\+|'|%)"))

