import ghasedakpack
from random import randint



code = randint(1000, 10000)

sms = ghasedakpack.Ghasedak("6a053b7aabc10ecb15f53dd0e6e7f6419de45d6c7d514065f4dcd3b1ed341b4a")

sms.verification({'receptor': '09134624323','type': '1','template': 'kavianshop','param1': 'code'})