import xlrd
import xlwt
def main():
  # save the file names of spreadsheets as variables so they may be accessed
  # the files must be in the same folder as this program or there will be problems
  cafo_data = 'CAFOtable.xls'
  ip_permits = 'permits_ip.xls'
  playa_RSC = 'playa_RSCs.xlsx'
  gp_permits = 'CAFO_DATA_REQUEST_2018.XLS'
  pending_permits = 'CAFO_PENDING_APPLICATION_2018.xls'

  # create a 'master' worksheet of the largest spreadsheet
  workbook = xlrd.open_workbook(cafo_data)
  master = workbook.sheet_by_name('Sheet1')

  # create variables to out write relevant data
  writeBook = xlwt.Workbook()
  writeSheet = writeBook.add_sheet('Sheet1', cell_overwrite_ok=True)

  # create variables to store data from smaller spreadsheets
  readbook1 = xlrd.open_workbook(ip_permits)
  readbook2 = xlrd.open_workbook(playa_RSC)
  readbook3 = xlrd.open_workbook(gp_permits)
  readbook4 = xlrd.open_workbook(pending_permits)

  read1 = readbook1.sheet_by_name('Sheet1')
  read2 = readbook2.sheet_by_name('Sheet1')
  read3 = readbook3.sheet_by_name('Sheet1')

    # iterate through each row of larger xls
  for row in range(1, master.nrows):
    # (re)set variables equal to nothing so that data is not input redundantly
    animal = ''
    count = ''
    area = ''
    # store the permit number (which is in column 'E') as variable 'permitNum'
    permitNum = master.cell_value(row, 4)
    permitNum = permitNum[ : 5]
    # store the epa number (in column 'D') as epaNum
    epaNum = master.cell_value(row, 3)

    for roW in range(1, read3.nrows):
      epa = read3.cell_value(roW, 1)
      if epa == epaNum:
        site = read3.cell_value(roW, 3)
        rn = read3.cell_value(roW, 2)
        parent_type = read3.cell_value(roW, 8)
        if parent_type == 'PRIMARY SIC CODE':
          sic = read3.cell_value(roW, 9)
        if parent_type == 'ANIMAL TYPE':
          animal = read3.cell_value(roW, 9)
          count = read3.cell_value(roW, 11)
        if parent_type == 'LMU TOTAL ACRES':
          area = read3.cell_value(roW, 9)
        if parent_type == 'OPERATIONAL STATUS':
          status = read3.cell_value(roW, 9)
    writeSheet.row(row).write(0, rn)
    writeSheet.row(row).write(2, area)
    writeSheet.row(row).write(3, sic)
    writeSheet.row(row).write(4, animal)
    writeSheet.row(row).write(5, count)
    writeSheet.row(row).write(6, site)
    writeSheet.row(row).write(11, status)

    # iterate through each row of smaller xls to find industrial RNs
    for rowW in range(1, read1.nrows):
      # store the permit number (which is in column 'A') as variable 'ai'
      ai = read1.cell_value(rowW, 0)
      ai = ai[4:9]

      # use boolean comparison to determine if the permit numbers are the same
      if ai == permitNum:
        rn = read1.cell_value(rowW, 1)
        site = read1.cell_value(rowW, 18)
        # out write the rn to the first column of the writeBook
        writeSheet.row(row).write(0, rn)
        sic = read1.cell_value(rowW, 33)
        animal = read1.cell_value(rowW, 39)
        animal = animal.split()
        writeSheet.row(row).write(3, sic)
        writeSheet.row(row).write(5, animal[0])
        writeSheet.row(row).write(6, site)

    # iterate through the other smaller spreadsheet to find data about PLAYA RSCs
    for rowWw in range(1, read2.nrows):
      epa = read2.cell_value(rowWw, 1)
      if epa == epaNum:
        writeSheet.row(row).write(1, 'PLAYA RSCs')

  # out write the rest of the data from the master spreadsheet
  for row in range(0, master.nrows):
    for col in range(0, master.ncols):
      content = master.cell_value(row, col)
      # this conditional ensures that all permit types are either 'GP'(General Permit) or 'IP' (Industrial Permit)
      if col == 10:
        if content == 'GP-C':
          content = 'GP'
        elif content == 'CP':
          content = 'IP'
      if content == 'End of pipe as indicated on paper map':
        content = 'Point indicated on map'
      if col == 11:
        content = master.cell_value(row, col+1)
      writeSheet.row(row).write(col+7, content)

  # save the new spreadsheet  
  writeBook.save('output.xls')
main()
