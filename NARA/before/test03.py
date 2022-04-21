# openpyxl을 가져옵니다.
import openpyxl
# 워크북(엑셀파일)을 새로 만듭니다.
wb = openpyxl.Workbook()
# 현재 활성화된 시트를 선택합니다.
sheet = wb.active
# A1셀에 hello world!를 입력합니다.
sheet['A1'] = 'hello world! Korea'
# 워크북(엑셀파일)을 원하는 이름으로 저장합니다.
wb.save('test01.xlsx')
