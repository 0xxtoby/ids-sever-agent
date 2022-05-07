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
    # # 追加写入
    # with open('./rules/rules.txt', 'a') as f:
    #     f.write('\.(php|jsp|asp|aspx)\?(\w){1,10}=\d{1,3} HTTP/1.1')
    #读取最后一行
    with open('./rules/rules.txt', 'r') as f:
        lines = f.readlines()
        print(lines[-1])
    # # 追加写入
    a={}

    a["url"]='''GET /shell.jsp?pass=1 HTTP/1.1
User-Agent: Java/1.8.0_161
Host: 10.95.36.50:9997
Accept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
Connection: keep-alive
'''
    a2="\.(php|jsp|asp|aspx)\?(\w){1,10}=\d{1,3} HTTP/1.1"
    print(match_rule_str(a["url"],lines[-1]))
    print(match_rule_str(a["url"],a2))

