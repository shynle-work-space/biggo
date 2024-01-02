from datetime import datetime
import pytz

def unix_timestamp_to_tz(unix_timestamp):
    utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=pytz.utc)
    ho_chi_minh_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    ho_chi_minh_time = utc_datetime.astimezone(ho_chi_minh_tz)
    return ho_chi_minh_time.strftime('%Y-%m-%d %H:%M:%S')


