import gdal
import random
import numpy
import time

def populate():
  in_file = open('change2.txt', 'r')
  in_file.readline()
  prob = []
  for row in range(16):
    line = in_file.readline()
    line = line.strip().split()
    sum_val = 0
    for i in range(1, len(line) - 1):
      sum_val += float(line[i])
    new_line = []
    for col in range(1, len(line) - 1):
      percentage = 0
      percentage = float(line[col]) / float(sum_val)
      new_line.append(percentage)
    prob.append((line[0], new_line))
  in_file.close()
  return prob
def translate(count):
  if count == 0:
    return 0
  elif count == 1:
    return 11
  elif count == 2:
    return 21
  elif count == 3:
    return 22
  elif count == 4:
    return 23
  elif count == 5:
    return 24
  elif count == 6:
    return 31
  elif count == 7:
    return 41
  elif count == 8:
    return 42
  elif count == 9:
    return 43
  elif count == 10:
    return 52
  elif count == 11:
    return 71
  elif count == 12:
    return 81
  elif count == 13:
    return 82
  elif count == 14:
    return 90
  elif count == 15:
    return 95
def predict(value, prob):
  rng = random.random()
  count = 0
  total = 0
  if value == 0:
    for val in prob[0].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 11:
    for val in prob[1].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 21:
    for val in prob[2].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 22:
    for val in prob[3].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 23:
    for val in prob[4].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 24:
    for val in prob[5].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 31:
    for val in prob[6].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 41:
    for val in prob[7].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 42:
    for val in prob[8].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 43:
    for val in prob[9].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 52:
    for val in prob[10].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 71:
    for val in prob[11].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 81:
    for val in prob[12].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 82:
    for val in prob[13].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 90:
    for val in prob[14].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
  elif value == 95:
    for val in prob[15].values():
      if rng < val + total:
        return translate(count)
      else:
        total += float(val)
def main():
  in_raster = gdal.Open('LC2011upload.tif')
  format = 'GTiff'
  driver = gdal.GetDriverByName(format)
  band = in_raster.GetRasterBand(1)
  dataraster = band.ReadAsArray().astype(numpy.float)
  prob = populate()
  for cell in dataraster:
    cell = predict(cell, prob)
  new_raster.GetRasterBand(1).WriteArray(dataraster)
main()
