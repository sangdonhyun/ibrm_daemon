import os
cmd="""curl -d @data.json -H "Content-Type: application/json" -X POST http://121.170.193.207:53004/shell-list 
"""

print cmd
print os.popen(cmd).read()