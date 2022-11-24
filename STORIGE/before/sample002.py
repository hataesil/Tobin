from openpyxl import load_workbook

workbook_name = 'sample.xlsx'
wb = load_workbook(workbook_name)
page = wb.active

# New data to write:
new_companies = [['name3','address3','tel3','web3'], ['name4','address4','tel4','web4']]

for info in new_companies:
    page.append(info)

wb.save(filename=workbook_name)
