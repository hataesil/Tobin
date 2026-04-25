# -*- coding: utf-8 -*-
import requests
import pandas as pd
import os
import time
from urllib.parse import urlencode
from datetime import date, timedelta
from dotenv import load_dotenv


# ── 설정 ────────────────────────────────────────────────
def load_config() -> dict:
    load_dotenv()
    api_key = os.environ.get('NARABID_API_KEY')
    if not api_key:
        raise EnvironmentError("API 키가 없습니다. .env 파일을 확인하세요.")

    today = date.today()
    return {
        'api_key'  : api_key,
        'url'      : 'https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServcPPSSrch',
        'start'    : (today - timedelta(days=15)).strftime('%Y%m%d'),
        'end'      : today.strftime('%Y%m%d'),
        'industry' : ['1162', '1164', '1166', '1260', '2775'],  # 경비청소시설
        'region'   : ['00', '30'],
        'columns'  : ['bidNtceNo', 'bidNtceOrd', 'bidNtceNm', 'bidBeginDt', 'bidClseDt', 'sucsfbidLwltRate', 'rgstDt','industry','region'],
    }


# ── API 단일 페이지 호출 ─────────────────────────────────
def fetch_page(url: str, params: dict, page: int) -> list | None:
    query = "?" + urlencode({**params, 'pageNo': str(page)})
    try:
        response = requests.get(url + query, timeout=10)
        response.raise_for_status()
        r_dic = response.json()
    except requests.exceptions.Timeout:
        print(f"  [timeout] 페이지 {page} — 건너뜁니다")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP 오류] {e} — 건너뜁니다")
        return None
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"  [오류] {e} — 건너뜁니다")
        return None

    body = r_dic.get('response', {}).get('body', {})
    return body.get('items') or []


# ── 페이지네이션 포함 전체 수집 ──────────────────────────
def fetch_all(url: str, params: dict) -> list:
    all_items = []
    page = 1
    num_of_rows = int(params['numOfRows'])

    while True:
        items = fetch_page(url, params, page)

        if items is None:       # 오류 → 중단
            break
        if not items:           # 빈 페이지 → 수집 완료
            break

        all_items.extend(items)
        print(f"  → 페이지 {page}: {len(items)}건")

        if len(items) < num_of_rows:  # 마지막 페이지
            break

        page += 1
        time.sleep(0.5)

    return all_items


# ── 업종 × 지역 조합 순회 ────────────────────────────────
def collect(config: dict) -> pd.DataFrame:
    base_params = {
        'serviceKey'     : config['api_key'],
        'numOfRows'      : '500',
        'inqryDiv'       : '1',
        'inqryBgnDt'     : config['start'],
        'inqryEndDt'     : config['end'],
        'bidClseExcpYn'  : 'Y',
        'type'           : 'json',
    }

    frames = []
    total_combinations = len(config['industry']) * len(config['region'])
    done = 0

    for industry in config['industry']:
        for region in config['region']:
            done += 1
            print(f"[{done}/{total_combinations}] 업종 {industry} / 지역 {region}")

            params = {**base_params, 'indstrytyCd': industry, 'prtcptLmtRgnCd': region}
            items = fetch_all(config['url'], params)

            if items:
                df_part = pd.DataFrame(items)
                df_part['industry'] = industry  # 추가
                df_part['region'] = region      # 추가
                frames.append(df_part)

            time.sleep(0.5)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ── 데이터 정제 ──────────────────────────────────────────
def clean(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    # 존재하는 컬럼만 추출 (API 변경 대비)
    valid_cols = [c for c in columns if c in df.columns]
    df = df[valid_cols].drop_duplicates(keep='first', ignore_index=True)
    df = df.set_index('rgstDt')
    return df


# ── 저장 ─────────────────────────────────────────────────
def save(df: pd.DataFrame, end: str) -> str:
    output_file = f'Bidlist{end}.xlsx'
    df.to_excel(output_file)
    return output_file


# ── 실행 진입점 ──────────────────────────────────────────
def main():
    config = load_config()
    print(f"수집 기간: {config['start']} ~ {config['end']}\n")

    df = collect(config)

    if df.empty:
        print("\n수집된 데이터가 없습니다.")
        return

    df = clean(df, config['columns'])
    output_file = save(df, config['end'])

    print(f"\n완료 — 총 {len(df)}건 저장: {output_file}")


if __name__ == '__main__':
    main()
