from datetime import timezone 
import datetime 
  
def utc_timestamp():  
    now = datetime.datetime.now(timezone.utc) 
    utc_time = now.replace(tzinfo=timezone.utc) 
    return utc_time.timestamp()
  