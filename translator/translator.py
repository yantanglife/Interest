import re
from js import bd_js_code, test_code
import json
import js2py
import time
import random
import hashlib
import requests
from tkinter import *


class Youdao:
    def __init__(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                        'Referer': 'http://fanyi.youdao.com/',
                        'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
                    }
        self.data = {
                        'i': None,
                        'from': 'AUTO',
                        'to': 'AUTO',
                        'smartresult': 'dict',
                        'client': 'fanyideskweb',
                        'salt': None,
                        'sign': None,
                        'ts': None,
                        'bv': None,
                        'doctype': 'json',
                        'version': '2.1',
                        'keyfrom': 'fanyi.web',
                        'action': 'FY_BY_REALTlME'
                    }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    def translate(self, word):
        ts = str(int(time.time()*10000))
        salt = str(int(time.time()*10000) + random.random()*10 + 10)
        sign = 'fanyideskweb' + word + salt + '97_3(jkMYg@T[KZQmqjTK'
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['ts'] = ts
        self.data['bv'] = bv
        res = requests.post(self.url, headers=self.headers, data=self.data)
        # return [res.json()['translateResult'][0][0].get('tgt')]
        '''
        {'translateResult': [[{'tgt': 'interesting', 'src': '有趣的'}]], 'errorCode': 0, 'type': 'zh-CHS2en', 
        'smartResult': {'entries': ['', 'interesting\r\n', 'funny\r\n', 'amusing\r\n'], 'type': 1}}

        '''
        ans_json = res.json()
        smart_result = ans_json.get("smartResult").get("entries")
        new_s_result = []
        for key in smart_result:
            if len(key) > 0:
                end = key.find("\r", 0)
                new_s_result.append(key[: end])
        return {"result": ans_json['translateResult'][0][0].get('tgt'),
                "smartResult": new_s_result}


class Baidu:
    def __init__(self):
        self.session = requests.Session()
        self.session.cookies.set('BAIDUID', '19288887A223954909730262637D1DEB:FG=1;')
        self.session.cookies.set('PSTM', '%d;' % int(time.time()))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.data = {
            'from': 'zh',
            'to': 'en',
            'transtype': 'realtime',
            'query': '',
            'simple_means_flag': '3',
            'sign': '',
            'token': '',
        }
        self.url = 'https://fanyi.baidu.com/v2transapi'
        self.url_ch2en = "https://fanyi.baidu.com/#zh/en/"

    def get_page(self, ch_word):
        res = requests.post(self.url_ch2en + ch_word, headers=self.headers)
        res.encoding = res.apparent_encoding
        # then res.text is charset type.
        # text is decode to unicode
        # content is bytes
        content = res.content.decode('utf-8')
        return res.text

    def translate(self, word):
        self.data['query'] = word
        self.data['token'], gtk = self.__get_token_gtk()
        # self.data['token'] = '78806fc4c938ba7ca634bd9f80ae91c5'
        '''可能是因为时间戳不同步，导致直接请求得到的token值不能用'''
        self.data['token'] = '6482f137ca44f07742b2677f5ffd39e1'
        self.data['sign'] = self.__get_sign(gtk, word)
        res = self.session.post(self.url, data=self.data)
        all_data = res.json()
        print(all_data)
        trans_result = all_data.get("trans_result").get("data")[0].get("result")[0][1]
        double_result = all_data.get("liju_result").get("double")
        tag_result = all_data.get("liju_result").get("tag")
        print(tag_result)
        double_example_list = []
        # print(self.data)
        for tup in json.loads(double_result):
            juzi = self.__get_sentence(tup[0])
            sentence = self.__get_sentence(tup[1])
            double_example_list.append((juzi, sentence))
        return {"trans_result": trans_result,
                "double_example": double_example_list,
                "tag_result": tag_result}
        # return [res.json()['trans_result']['data'][0]['result'][0][1]]

    def __get_token_gtk(self):
        url = 'https://fanyi.baidu.com/'
        res = requests.get(url, headers=self.headers)
        token = re.findall(r"token: '(.*?)'", res.text)[0]
        gtk = re.findall(r";window.gtk = ('.*?');", res.text)[0]
        return token, gtk

    @staticmethod
    def __get_sign(gtk, word):
        evaljs = js2py.EvalJs()
        js_code = bd_js_code
        js_code = js_code.replace('null !== i ? i : (i = window[l] || "") || ""', gtk)
        evaljs.execute(js_code)
        sign = evaljs.e(word)
        return sign

    @staticmethod
    def __get_sentence(tup):
        """Actually, tup contains info of space for punctuation.
            tup[0] is word or punctuation, and tup[-1] may be the space."""
        sentence = ""
        for i in tup:
            sentence += i[0]
            if isinstance(i[-1], str):
                sentence += i[-1]
        '''
        for i in tup:
            if i[0] in ".,;?!'":
                sentence = sentence[: -1]
            sentence += i[0]
            if mode == 'en':
                sentence += ' '
        if mode == 'en' and not sentence[-1] in ".,?!":
            sentence = sentence[: -1]
        '''
        return sentence


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=YES)
        # self.text = StringVar()
        self.__create_widgets()
        self.baidu_translator = Baidu()

    def __create_widgets(self):
        """"""
        '''frame1: title'''
        self.frame1 = Frame(self)
        self.title_label = Label(self.frame1, text="Translate", font=("微软雅黑", 15), width='10')
        self.title_label.pack()
        self.frame1.pack(side=TOP)
        '''frame2: search text and button'''
        self.frame2 = Frame(self)
        self.frame2_left = Frame(self.frame2)
        self.frame2_right = Frame(self.frame2)
        self.search_text = Entry(self.frame2_left, font=("", 13), width='20')
        self.button = Button(self.frame2_right, text='search', font=("", 15), width='7', command=self.__translate)
        '''Press button or ENTER key'''
        self.search_text.bind('<Return>', self.__enter)
        self.search_text.pack()
        self.button.pack()
        self.frame2_left.pack(side=LEFT)
        self.frame2_right.pack(side=RIGHT)
        self.frame2.pack(side=TOP, ipadx=3, pady=2)
        '''frame3: answer word'''
        self.frame3 = Frame(self)
        self.trans_answer = Entry(self.frame3, font=("", 13), width='30')
        self.smart_answer = Entry(self.frame3, font=("", 13), width='60')
        self.trans_answer.pack(side=TOP, pady=3)
        self.smart_answer.pack(side=TOP, padx=10, fill=X)
        self.frame3.pack(side=TOP, fill=BOTH, ipady=3)
        '''frame4 answer text area'''
        self.frame4 = Frame(self)
        self.y_scrollbar = Scrollbar(self.frame4)
        self.x_scrollbar = Scrollbar(self.frame4, orient=HORIZONTAL)
        self.search_answer = Text(self.frame4)
        # Combine scrollbar with text.
        self.y_scrollbar.config(command=self.search_answer.yview)
        self.x_scrollbar.config(command=self.search_answer.xview)
        # If wrap = 'none' in config. text would show in one line.
        self.search_answer.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set,
                                  font=("", 12), width='60', wrap=NONE)
        # Pack order is important.
        self.x_scrollbar.pack(side=BOTTOM, fill=BOTH)
        self.y_scrollbar.pack(side=RIGHT, fill=BOTH)
        self.search_answer.pack(fill=BOTH, expand=YES)
        self.frame4.pack(expand=YES, fill=BOTH, anchor=CENTER)
        # Init state.
        self.trans_answer.config(state=DISABLED)
        self.smart_answer.config(state=DISABLED)
        self.search_answer.config(state=DISABLED)
        self.search_text.focus()

    def __enter(self, event):
        print(event)
        self.__translate()

    def __translate(self):
        # self.update()
        info = self.search_text.get()
        res = self.baidu_translator.translate(info)
        trans_result = res.get("trans_result", None)
        double_example = res.get("double_example", None)
        tag_result = res.get("tag_result", None)
        # text = ""
        '''clear'''
        self.trans_answer.config(state=NORMAL)
        self.smart_answer.config(state=NORMAL)
        self.search_answer.config(state=NORMAL)
        self.trans_answer.delete(0, END)
        self.smart_answer.delete(0, END)
        self.search_answer.delete(1.0, END)

        self.trans_answer.insert(END, trans_result)
        for word in tag_result:
            self.smart_answer.insert(END, "{}  ".format(word))
        for idx, example in enumerate(double_example, 1):
            print("{}.\t{}\n\t{}".format(idx, example[0], example[1]))
            # text += "{}.\t{}\n\t{}\n".format(idx, example[0], example[1])
            self.search_answer.insert(END, "{}. {}\n  {}\n".format(idx, example[0], example[1]))
        self.search_answer.config(state=DISABLED)
        # self.trans_answer.config(state=DISABLED)
        # self.smart_answer.config(state=DISABLED)

        # self.text.set(text)


if __name__ == "__main__":
    # youdao = Youdao()
    app = Application()
    app.master.title("yantang")
    # app.master.geometry('800x500')
    app.master.minsize(width=400, height=300)
    app.mainloop()
    '''
    bd = Baidu()
    while 1:
        src_word = input("word:")
        if len(src_word) > 0:
            # ans = youdao.translate(src_word)
            ans_dic = bd.translate(src_word)
            ans = bd.get_page(src_word)
            double_example = ans_dic.get("double_example", None)
            for idx, example in enumerate(double_example, 1):
                print("{}.\t{}\n\t{}".format(idx, example[0], example[1]))
            #  print(page)
    '''
