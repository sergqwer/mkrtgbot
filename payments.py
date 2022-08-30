import requests

lava_wallet = 'R10188601'
lava_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiJmNmEwNDQzMi04YjE0LTBlM2YtNjIyMy1lOTQ1N2I2NmFlMDEiLCJ0aWQiOiI2ZTAwYzFjYS05ZTU2LWUzNjUtMDU1ZS05Y2VmYTAwMGViZDMifQ.597Qs4V7n5bRliworyzFu5HyUqqTip_zirW_DOjbr_I'
lava_summ = 10

ping_responce = requests.get('https://api.lava.ru/wallet/list',
                             headers={
                                 'Authorization': str(lava_token)}
                             )
print(ping_responce.json())
responce = requests.post('https://api.lava.ru/invoice/create',
                         data={
                             'wallet_to': str(lava_wallet),
                             'sum': float(lava_summ),
                             'order_id': str(123),
                             'hook_url': str('https://goodniceday.pp.ua/wh'),
                             'success_url': str('https://goodniceday.pp.ua/success'),
                             'fail_url': str('https://goodniceday.pp.ua/fail'),
                             'expire': int(30),
                             'subtract': str(0),
                             'custom_fields': str(123),
                             'comment': str(123),
                             'merchant_id': str(123),
                             'merchant_name': str(123)
                         },
                         headers={
                             'Authorization': str(lava_token)
                         })

print(responce.json())
