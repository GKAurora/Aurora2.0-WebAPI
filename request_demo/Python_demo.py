import json
import requests

if __name__ == "__main__":

    # 获取token
    url = "https://49.4.21.18:26335/rest/plat/smapp/v1/oauth/token"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "grantType": "password",
        "userName": "13727494636",
        "value": "farmer123!@#"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    token = response.json()['accessSession']
    # print(token)
    # exit(0)
    #查询用户列表
    url = "https://49.4.21.18:26335/rest/campusclientservice/v1/event/userlist"
    data = {
        "level": "1",
        "tenantId": "default-organization-id",
        "startTime": "1623906000000",
        "endTime": "1623909600000",
        "id": "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
        "sortColumn": "totalcount",
        "currPage": "1",
        "pageSize": "100",
        "sortType": "desc"
    }
    header = {
        "X-Auth-Token": token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=header, data=json.dumps(data), verify=False)
    print(res.json()['data']['tableData'])
