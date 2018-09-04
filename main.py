#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@file 
@brief pubg APIからtelemetryファイルを取得するスクリプト (アカウントIDで検索かけるメッソドもおまけ)
@date 2018-09-04
'''

import requests
import json

API_KEY = "<自身のAPIキー>"
SERVER = "<好きなShardidに変更>"

'''
Player名と{アカウントID + 参加したマッチIDのリスト}を対応させたdictを返す
@params {string list} 検索したいPlayer名のリスト
@return {object} Player名とアカウントIDの対応
'''
def request_accountInfo(playername_list):

    # リクエスト準備
    headers = {
        "Authorization" : "Bearer "+ API_KEY,
        "Accept": "application/json"
    }
    end_point = "https://api.pubg.com/shards/{}/players".format(SERVER)

    query = {
        "filter[playerNames]": ','.join(playername_list)
    }

    # リクエスト実行
    res = requests.get(end_point, headers=headers,params=query)
    res_json = json.loads(res.text)

    # parse処理
    return_obj = {}
    for account_data in res_json['data']:
        if account_data['attributes']['name'] in playername_list:
            add_obj = {}
            add_obj['accountid'] = account_data['id']
            tmp_list = []
            for match in account_data['relationships']['matches']['data']:
                tmp_list.append(match['id'])
            add_obj['matchIDs'] = tmp_list
            return_obj[account_data['attributes']['name']] = add_obj
            
    return return_obj

'''
検索したいマッチIDを受け取って対応するtelemetry.jsonのURLを返す
@params {string} 検索したいマッチのID
@return {object} telemetry.jsonが取れるURL
'''
def request_matchTelemetry(matchID):
    # リクエスト準備
    headers = {
        "Authorization" : "Bearer "+ API_KEY,
        "Accept": "application/json"
    }
    end_point = "https://api.pubg.com/shards/{}/matches/{}".format(SERVER,matchID)
    
    # リクエスト実行
    res = requests.get(end_point, headers=headers)
    res_json = json.loads(res.text)

    # parse処理
    telemetry_URL = [x['attributes']["URL"] for x in res_json['included'] if x['type'] == 'asset']
    return telemetry_URL


# テスト用のメイン処理
if __name__ == '__main__' :
    accountInfo = request_accountInfo(["yobiyobi","nicky_pon"])
    print(accountInfo)
    telemetryURL = request_matchTelemetry(accountInfo["yobiyobi"]["matchIDs"][0])
    print (telemetryURL)
        
    
