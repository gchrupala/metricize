import tempfile
import zipfile
import shutil
import os.path

def modifyZip(zipfname, outzipfname, match, modify):
  '''Apply transformation _modify_ to all file whose name _match_'''
  tempdir = tempfile.mkdtemp()
  try:
    tempname = os.path.join(tempdir, 'new.zip')
    with zipfile.ZipFile(zipfname, 'r') as zipread:
      with zipfile.ZipFile(tempname, 'w') as zipwrite:
        for item in zipread.infolist():
          data = zipread.read(item.filename)                  
          if match(item.filename):
            f = modify
          else:
            f = lambda x: x
          zipwrite.writestr(item, f(data))
    shutil.move(tempname, outzipfname)
  finally:
    shutil.rmtree(tempdir)
