import json
import paramiko
from requests import get
from typing import Optional


class Config:
  def __init__(self, host: str, port: str, username: str, password: str) -> None:
    self.host = host
    self.port = int(port)
    self.username = username
    self.password = password


def getConfig() -> Config:
  f = open('./config.json')
  data = json.load(f)

  return Config(data['host'], data['port'], data['username'], data['password'])


def getRouterIp(client: paramiko.SSHClient) -> Optional[str]:
  ip = ''
  try:
    _, stdout, stderr = client.exec_command(
        "ifconfig ppp0 | head -n 2 | tail -n 1"
    )

    res = str(stdout.readline())
    ip = res.replace("          ", "").split(" ")[1].replace('addr:', '')

  except:
    ip = None

  return ip


def getPublicIp() -> str:
  return get('https://api.ipify.org').content.decode('utf8')


if __name__ == '__main__':
  config = getConfig()
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  ssh.connect(
      hostname=config.host,
      username=config.username,
      password=config.password,
      port=config.port
  )
  if getRouterIp(ssh) != getPublicIp():
    ssh.exec_command("restart")

  ssh.close()
