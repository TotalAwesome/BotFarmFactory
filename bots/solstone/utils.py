from datetime import timezone 
import datetime 
  
def utc_timestamp():  
    now = datetime.datetime.now(timezone.utc) 
    utc_time = now.replace(tzinfo=timezone.utc) 
    return utc_time.timestamp()
  

now = int(utc_timestamp())
end = 1722083825 + (8 * 60 * 60 + 10)
print(datetime.datetime.fromtimestamp(now))
print(datetime.datetime.fromtimestamp(end))
print((end - now))
print()