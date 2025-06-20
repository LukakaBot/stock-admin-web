from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import datetime
import pandas as pd
import json


router = APIRouter()


def get_plate_data(date: str, k: int = 0):
    url1 = "xxx"
    url2 = "xxx"

    headers = {
        "Host": "XXXX" if k == 1 else "XXX",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "lhb/5.17.9 (XXXX; build:0; iOS 16.6.0) Alamofire/4.9.1",
        "Accept-Language": "zh-Hans-CN;q=1.0",
        "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
    }
    params = {
        "Date": date if k == 1 else datetime.date.today().strftime("%Y-%m-%d"),
        "Index": "0",
        "Order": "1",
        "PhoneOSNew": "2",
        "Type": "1",
        "VerSion": "5.17.0.9",
        "ZSType": "7",
        "a": "XXXXXX",
        "apiv": "w38",
        "c": "XXXXX",
        "st": "20",
    }
    url = url1 if k == 0 else url2
    print(f"请求地址：{url}")
    print(f"请求参数：{params}")

    try:
        response = requests.post(url=url, headers=headers, data=params)
        if response.status_code == 200:
            data = response.json()
            if "list" in data and data["list"]:
                plate_list = []
                for item in data["list"]:
                    if len(item) >= 4:
                        plate_list.append(
                            {
                                "代码": item[0],
                                "名称": item[1],
                                "强度": item[2],
                                "涨幅%": item[3],
                            }
                        )
                print("获取数据陈宫")
                return JSONResponse(
                    content={
                        "code": 200,
                        "message": "success",
                        "data": plate_list,
                    }
                )
            else:
                print("数据缺失")
                return JSONResponse(
                    content={
                        "code": 400,
                        "message": "数据缺失",
                        "data": None,
                    }
                )
        else:
            print("接口调用失败")
            return JSONResponse(
                content={
                    "code": 400,
                    "message": f"接口请求失败：{response.status_code}",
                    "data": None,
                }
            )
    except Exception as err:
        return JSONResponse(
            content={
                "code": 400,
                "message": f"数据获取失败：{str(err)}",
                "data": None,
            }
        )


def get_stock_data(plate_code: str, date: str, k: int = 0):
    url1 = "xxx"
    url2 = "xxx"
    headers = {
        "Host": "XXXX" if k == 1 else "XXXX",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "lhb/5.17.9 (XXXX; build:0; iOS 16.6.0) Alamofire/4.9.1",
        "Accept-Language": "zh-Hans-CN;q=1.0",
        "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
    }
    params = {
        "PlateID": plate_code,
        "Date": date if k == 1 else datetime.date.today().strftime("%Y-%m-%d"),
        "Index": "0",
        "Order": "1",
        "PhoneOSNew": "2",
        "Type": "6",
        "VerSion": "5.17.0.9",
        "a": "XXXXX",
        "apiv": "w38",
        "c": "XXXXX",
        "st": "20",
    }
    url = url1 if k == 0 else url2

    try:
        response = requests.post(url=url, headers=headers, data=params)
        if response.status_code == 200:
            data = response.json()
            if "list" in data and data["list"]:
                stock_list = []
                for item in data["list"]:
                    if len(item) >= 4:
                        stock_list.append(
                            {
                                "代码": item[0],
                                "名称": item[1],
                                "涨幅%": item[6],
                                "连板": item[23],
                                "板块": item[4],
                            }
                        )
                return JSONResponse(
                    content={
                        "code": 200,
                        "message": "success",
                        "data": stock_list,
                    }
                )
            else:
                return JSONResponse(
                    content={"code": 400, "message": "数据缺失", "data": None}
                )
        else:
            return JSONResponse(
                content={
                    "code": 400,
                    "message": f"接口请求失败：{response.status_code}",
                    "data": None,
                }
            )
    except Exception as err:
        return JSONResponse(
            content={
                "code": 400,
                "message": f"获取个股数据失败：{str(err)}",
                "data": None,
            }
        )


@router.get("/")
async def hello():
    return {"message": "Hello World"}


@router.get("/plate")
async def get_plates():
    return get_plate_data(date="2025-06-20")
