from handler import data_handler

"""
 "C:\python_2.7\python.exe" "C:\Program Files (x86)\Google\google_appengine\dev_appserver.py" "./app.yaml"
"""
analysis_handler = data_handler()
results=analysis.modelize()
print(results)


analysis_handler = data_handler()
    results=analysis_handler.modelize()
    if(results is None):
      self.response.out.write("""
      <ul><li>
      No Results Data
      </li></ul>
      """)
    else:
      self.response.out.write('<ul>')
      for X in results:
        self.response.out.write('<li> %s </li>' % X)
      self.response.out.write('</ul>')
  self.response.out.write('</body></html>')