import xlwt

def deal_excel(rate_key, rate_value):
    rate_book = xlwt.Workbook()
    rate_sheet = rate_book.add_sheet('sheet1', cell_overwrite_ok=True)
    count = 0
    for item in rate_key:
        # print(item,':',rate_dict[item])
        rate_sheet.write(count, 0, item)
        count = count + 1
    count = 0
    for item in rate_value:
        rate_sheet.write(count, 1, item)
        count = count + 1
    rate_book.save('chiara.xls')