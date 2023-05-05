import web
import requests
import jsonpath
import json
import random
import time
import html


urls = (
    '/gptyier', 'gptyier',
    '/setsession', 'setsession',
    '/stream', 'stream',
    '/css/(.*)', 'static_handler_css',
    '/js/(.*)', 'static_handler_js',
)

headers = {
        'Host': 'yierco.slack.com',
        'Cookie': 'x=a363001cfd1849be739f45d4ea94d99e.1683296136; d=xoxd-1I6hZnXXuqtY1h0mTyZ14zBEzedNXkiJ%2FkrCzSGRNBiomJaLJNHzxvBuTA%2FrFZT3vEWOeHmlqibv1g3W7beAREUY43YIzmpyhcXfZCvEApneIxacpGmnvrpzQuPZ6okNYEuHwaK8hf3dlx24NkvexoaZ7bURIECdoTsWu2cmw1sEOh49EtyD5ET%2BIA%3D%3D; d-s=1683296149; lc=1683296149; _gcl_au=1.1.438343165.1683296151; _ga=GA1.2.644746821.1683296151; _gid=GA1.2.1135986881.1683296151; b=.a363001cfd1849be739f45d4ea94d99e; i18n_locale=zh-CN; utm=%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-btn_app_install-index-click%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+05+2023+22%3A18%3A24+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=3ec34c9c-58cd-4382-aef7-99f0b643f07d&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C3%3A0%2C2%3A0%2C4%3A0&AwaitingReconsent=false',
    }

token="xoxc-5216124951045-5212459913558-5204528378663-2dd1f752da78dd1cf2c27b20b0b80a56e21c81377eb4ba50c8d55065a8ff84ea"

Claude_userid="U056HHR8BA8"
fangjian_id="C056EU248D9"

app = web.application(urls, globals())
app.debug = False
render = web.template.render('templates')


class gptyier:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        with open('index.html', 'r',encoding='utf-8') as file:
            html_content = file.read()
        return html_content



class static_handler_css:
    def GET(self, filename):
        try:
            with open(f'css/{filename}', 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise web.notfound("File not found")
class static_handler_js:
    def GET(self, filename):
        try:
            with open(f'js/{filename}', 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise web.notfound("File not found")

class setsession:

    def POST(self):

        stream_url_post_postMessage_r_json_ts = web.cookies().get('ts')
        url_conversations_replies_huoqu_latest_reply_json_latest_reply2 = web.cookies().get('latest_reply')


        setsession_data = web.input(message=None)
        message = setsession_data.message


        message=message.replace("\"", '\\\"')

        print(message)

        prompt=message


        url_post_postMessage = 'https://yierco.slack.com/api/chat.postMessage'

        if(url_conversations_replies_huoqu_latest_reply_json_latest_reply2!=None):
            url_post_postMessage_file = {
                'token': (None,
                          token,
                          None),
                'channel': (None, '{}'.format(fangjian_id), None),
                'ts': (None, '1681546073.xxxxx5', None),
                'type': (None, 'message', None),
                'reply_broadcast': (None, 'false', None),
                'thread_ts': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                'unfurl': (None, '[]', None),
                'blocks': (None,
                           '[{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"%s"},{"type":"text","text":" %s"}]}]}]' % (
                               Claude_userid,prompt), None),
                'include_channel_perm_error': (None, 'true', None),
                '_x_reason': (None, 'webapp_message_send', None),
                '_x_mode': (None, 'online', None),
                '_x_sonic': (None, 'true', None)
            }
        else:
            url_post_postMessage_file = {
                'token': (None,
                          token,
                          None),
                'channel': (None, '{}'.format(fangjian_id), None),
                'ts': (None, '1681546073.xxxxx5', None),
                'type': (None, 'message', None),
                'unfurl': (None, '[]', None),
                'blocks': (None,
                           '[{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"%s"},{"type":"text","text":" %s"}]}]}]' % (
                               Claude_userid,prompt), None),
                'include_channel_perm_error': (None, 'true', None),
                '_x_reason': (None, 'webapp_message_send', None),
                '_x_mode': (None, 'online', None),
                '_x_sonic': (None, 'true', None)
            }

        try:
            url_post_postMessage_r = requests.post(url_post_postMessage, headers=headers,
                                               files=url_post_postMessage_file, verify=False)

        except BaseException as e:
            print("查询失败,正在重试")
            print(e)
            for o in range(100):
                try:
                    url_post_postMessage_r = requests.post(url_post_postMessage, headers=headers,
                                                           files=url_post_postMessage_file, verify=False)
                    if url_post_postMessage_r.status_code == 200:
                        break
                except BaseException as e:
                    print("再次查询子域名失败", o)
                    print(e)

        if ("\"ok\":true" in url_post_postMessage_r.text and "thread_ts" in url_post_postMessage_r.text and url_conversations_replies_huoqu_latest_reply_json_latest_reply2!=None):
            url_post_postMessage_r_json = json.loads(url_post_postMessage_r.text)
            url_post_postMessage_r_json_thread_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.message.thread_ts")[0]

            url_post_postMessage_r_json_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.ts")[0]
            web.setcookie('ts', '{}'.format(url_post_postMessage_r_json_thread_ts), 36000)
            web.setcookie('thread_ts', '{}'.format(url_post_postMessage_r_json_ts), 36000)


            return '{"success":true}'
        elif ("\"ok\":true" in url_post_postMessage_r.text and url_conversations_replies_huoqu_latest_reply_json_latest_reply2==None):
            url_post_postMessage_r_json = json.loads(url_post_postMessage_r.text)
            url_post_postMessage_r_json_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.ts")[0]
            web.setcookie('ts', '{}'.format(url_post_postMessage_r_json_ts), 36000)

            return '{"success":true}'
        else:
            return '{"success":false}'


class stream:
    def GET(self):

        stream_url_post_postMessage_r_json_ts = web.cookies().get('ts')
        # url_conversations_replies_huoqu_latest_reply_json_latest_reply2 = web.cookies().get('latest_reply')
        url_post_postMessage_r_json_thread_ts = web.cookies().get('thread_ts')

        url_conversations_replies = 'https://yierco.slack.com/api/conversations.replies'


        for i in range(120):
            try:
                url_conversations_replies_file = {
                    'token': (None,
                              token,
                              None),
                    'channel': (None, '{}'.format(fangjian_id), None),
                    'ts': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                    'inclusive': (None, 'ture', None),
                    'limit': (None, '28', None),
                    'oldest': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                    '_x_reason': (None, 'history-api/fetchReplies', None),
                    '_x_mode': (None, 'online', None),
                    '_x_sonic': (None, 'true', None)
                }
                url_conversations_replies_huoqu_latest_reply = requests.post(url_conversations_replies, headers=headers,
                                                        files=url_conversations_replies_file, verify=False)
            except BaseException as e:
                print("查询失败,正在重试")
                print(e)
                for o in range(100):
                    try:
                        url_conversations_replies_huoqu_latest_reply = requests.post(url_conversations_replies, headers=headers,
                                                                    files=url_conversations_replies_file,
                                                                    verify=False)
                        if url_conversations_replies_huoqu_latest_reply.status_code == 200:
                            break
                    except BaseException as e:
                        print("再次查询子域名失败", o)
                        print(e)

            if(i>2 and "latest_reply" not in url_conversations_replies_huoqu_latest_reply.text and "thread_ts" not in url_conversations_replies_huoqu_latest_reply.text):
                web.header('Content-Type', 'text/event-stream')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                web.header('Pragma', 'no-cache')
                return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}


                            data: [DONE]

                            """ % ("错误")

            #print(url_conversations_replies_huoqu_latest_reply.text)
            if ("\"ok\":true" in url_conversations_replies_huoqu_latest_reply.text and "latest_reply" in url_conversations_replies_huoqu_latest_reply.text and "thread_ts" in url_conversations_replies_huoqu_latest_reply.text):

                url_conversations_replies_huoqu_latest_reply_json = json.loads(url_conversations_replies_huoqu_latest_reply.text)

                url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply = jsonpath.jsonpath(url_conversations_replies_huoqu_latest_reply_json, "$.messages[0].latest_reply")[0]

                #print("url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply:{}".format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply))
                #print("url_post_postMessage_r_json_thread_ts:{}".format(url_post_postMessage_r_json_thread_ts))

                if(url_post_postMessage_r_json_thread_ts!=url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply and url_post_postMessage_r_json_thread_ts!=None):
                    #print(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply)
                    web.setcookie('latest_reply', '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), 36000)
                    break

                elif(url_post_postMessage_r_json_thread_ts==None):
                    #print(url_post_postMessage_r_json_thread_ts)
                    web.setcookie('latest_reply',
                                  '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply),
                                  36000)
                    break
            else:
                time.sleep(0.2)
        # url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply = web.cookies().get('latest_reply')


        if(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply!=None):
            for i in range(120):
                try:
                    url_conversations_replies_file2 = {
                        'token': (None,
                                  token,
                                  None),
                        'channel': (None, '{}'.format(fangjian_id), None),
                        'ts': (None, '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), None),
                        'inclusive': (None, 'ture', None),
                        'limit': (None, '28', None),
                        'oldest': (None, '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), None),
                        '_x_reason': (None, 'history-api/fetchReplies', None),
                        '_x_mode': (None, 'online', None),
                        '_x_sonic': (None, 'true', None)
                    }
                    url_conversations_replies_r = requests.post(url_conversations_replies, headers=headers,
                                                            files=url_conversations_replies_file2, verify=False)
                except BaseException as e:
                    print("查询失败,正在重试")
                    print(e)
                    for o in range(100):
                        try:
                            url_conversations_replies_r = requests.post(url_conversations_replies, headers=headers,
                                                                        files=url_conversations_replies_file2,
                                                                        verify=False)
                            if url_conversations_replies_r.status_code == 200:
                                break
                        except BaseException as e:
                            print("再次查询子域名失败", o)
                            print(e)

                # print(url_conversations_replies_r.text)
                if(i>2 and "_Typing" not in url_conversations_replies_r.text and "thread_ts" not in url_conversations_replies_r.text):
                    web.header('Content-Type', 'text/event-stream')
                    web.header('Access-Control-Allow-Origin', '*')
                    web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                    web.header('Pragma', 'no-cache')
                    return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""% ("错误")

                if ("\"ok\":true" in url_conversations_replies_r.text and "_Typing" not in url_conversations_replies_r.text and "thread_ts" in url_conversations_replies_r.text):
                    url_conversations_replies_r_json = json.loads(url_conversations_replies_r.text)
                    url_conversations_replies_r_json_text = jsonpath.jsonpath(url_conversations_replies_r_json, "$.messages[0].text")[0]

                    url_conversations_replies_r_json_text=html.unescape(url_conversations_replies_r_json_text).replace("\n","\\\\n").replace("\"","\\\"")

                    break
                else:
                    time.sleep(1)
            else:
                web.header('Content-Type', 'text/event-stream')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                web.header('Pragma', 'no-cache')
                return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""% ("错误")

            #print(url_conversations_replies_r_json_text)
            web.header('Content-Type', 'text/event-stream')
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            web.header('Pragma', 'no-cache')
            return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""%(url_conversations_replies_r_json_text)


if __name__ == "__main__":

    app.run()
