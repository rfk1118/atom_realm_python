import concurrent

import requests
from concurrent.futures import ThreadPoolExecutor

url = f"https://ep.atomicals.xyz/proxy/blockchain.atomicals.get_realm_info"
max_retry = 3


def query_string(string):
    retry = 0
    while True:
        if retry >= max_retry:
            break
        queryNowBody = {"params": [string, 0]}
        response = requests.post(url, json=queryNowBody)
        if response.status_code != 200:
            print(f"{string}未找到")
            retry = retry + 1
            continue
        mint_data = response.json()['response']
        if mint_data['result']['atomical_id'] is None:
            print("can mint:" + string)
            return string
        else:
            print("have mint:" + string)
            return ""
    return ""


def genAll():
    az1_combinations = []
    for i in range(ord('a'), ord('z') + 1):
        for digit in range(0, 10):
            for j in range(ord('a'), ord('z') + 1):
                combination = chr(i) + str(digit) + chr(j)
                az1_combinations.append(combination)
    return az1_combinations


def concurrent_query(strings):
    results = []
    with ThreadPoolExecutor(max_workers=64) as executor:
        # 提交查询任务
        futures = {executor.submit(query_string, string): string for string in strings}
        # 等待任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error querying string: {e}")
    return results


if __name__ == '__main__':
    strings_to_query = genAll()
    query_results = concurrent_query(strings_to_query)
    with open('output01.txt', 'w') as file:
        for string, result in zip(strings_to_query, query_results):
            print(f"Result for {string}: {result}")
            if len(result) == 0:
                continue
            else:
                file.write(result + "\n")
