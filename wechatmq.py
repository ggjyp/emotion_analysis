import itchatmp
import json
import requests

# 微信公众号Token
token = 'RICKJIANG'

itchatmp.update_config(itchatmp.WechatConfig(
    token=token,
    appId='your_appid',
    appSecret='your_appSecret'))


@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    analysis_result = get_result(msg['Content'])
    print(analysis_result)
    text = analysis_result['text']
    items = analysis_result['items']
    items = items[0]
    return '哈喽，你分析的句子是：' + text + '\n它属于积极倾向的可能性是：' + str(items['positive_prob']) + '\n它属于消极倾向的可能性是：' + str(
        items['negative_prob'])


# 调用百度API——情绪分析
def get_result(analysis_data):
    # 获取access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
           '&client_id=your_client_id&client_secret=your_client_secret'
    r = requests.get(url=host)
    access_token = json.loads(r.text)['access_token']
    # 根据analysis_data获取情绪倾向分析结果
    host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
    params = {'access_token': access_token}
    data = {'text': analysis_data}
    r = requests.post(url=host, params=params, data=json.dumps(data))
    return json.loads(r.text)


# 运行itchatmp
itchatmp.run()
