import datetime
import psutil

HANDLED_EMAILS: int = 0
TOTAL_EXCEPTIONS_CNT: int = 0
STARTUP_TIME: datetime.datetime = datetime.datetime.now()
UPTIME = lambda: datetime.datetime.now() - STARTUP_TIME

def get_stats() -> str:
  cpu_times = psutil.cpu_times()
  mem = psutil.virtual_memory()
  freq = psutil.cpu_freq()
  result = "CPU times:\n"
  result += f"\tuser = {cpu_times[0]}\n"
  result += f"\tsys  = {cpu_times[2]}\n"
  result += f"\tidle = {cpu_times[3]}\n"
  result += f"CPU load: {psutil.cpu_percent(1)}\n"
  result += "CPU freq:\n"
  result += f"\tcur = {int(freq[0])}MHz\n"
  result += f"\tmin = {int(freq[1])}MHz\n"
  result += f"\tmax = {int(freq[2])}MHz\n"
  result += "Memory:\n"
  result += f"\ttotal = {round(mem[0] / 1024 / 1024 / 1024, 2)}GB\n"
  result += f"\tused  = {mem[2]}%, {round(mem[3] / 1024 / 1024 / 1024, 2)}GB\n"
  result += f"\tfree  = {round(mem[4] / 1024 / 1024 / 1024, 2)}GB\n"
  return result