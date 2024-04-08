import requests
from bs4 import BeautifulSoup
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
import google.generativeai as genai
import os
import datetime
import re
current_time = datetime.datetime.now()
current_date = current_time.date()
print(current_time)
# Load environment variables
e3p_cookie = os.environ["E3P_COOKIE"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
line_notify_token = os.environ["LINE_NOTIFY_TOKEN"]

# Configure generative AI
genai.configure()
gemini_pro = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.1,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


prompt = """
Announcement:
---------------------
{message}
---------------------

Summarize this homework announcement for me,
highlighting deadlines and extracting important information as clearly and concisely as possible.
Use only headers and bullet points in your summary.
Use Traditional Chinese only.
"""

def send_e3_hw_announcement(url: str):
    """Fetch the page content"""
    headers = {
        "Cookie": e3p_cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    requests.adapters.DEFAULT_RETRIES = 5
    html = requests.get(url, headers=headers).text

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find_all(name="h3", attrs={"class": "name d-inline-block"})
    tags = soup.find_all(name="div", attrs={"class": "event mt-3"})
    final_message = ""
    final_message += "今天日期: " + str(current_date) + '\n' + "近三日的作業公告\n" + '=' * 16 + '\n'
    more_than_n_days = False
    hw_time_delta = 7
    for i in range(len(tags)):
        block = tags[i]
        headline = headlines[i]
        message = "\n"
        block_title = block.find_all(name="div", attrs={"class": "col-11"})
        message += headline.text + '\n' + '截止時間:\n'
        for title in block_title:
            if title.text == '課程事件':
                continue
            date_pattern = r"\d{2}月 \d{2}日"
            date_match = re.search(date_pattern, title.text)
            if date_match:
                date = date_match.group(0)
                date_obj = datetime.datetime.strptime(date, "%m月 %d日")
                date_obj = date_obj.replace(year=current_date.year)
                delta = date_obj.date() - current_date
                if 0 <= delta.days <= hw_time_delta:
                    pass
                else:
                    date_obj = date_obj.replace(year=current_date.year + 1)
                    delta = date_obj.date() - current_date
                    if 0 <= delta.days <= hw_time_delta:
                        pass
                    else:
                        more_than_n_days = True
                        break
            message += title.text + '\n'
        if more_than_n_days:
            break
        print(message)
        llm_prompt = prompt.format(message=message)
        response = gemini_pro.invoke(llm_prompt).content
        response = response.replace('*', '').replace('-', '')
        final_message += (message + '\n'+ '=' * 16 + '\n')
    lineNotifyMessage(line_notify_token, '\n' + final_message)

url = 'https://e3p.nycu.edu.tw/calendar/view.php?view=upcoming'
send_e3_hw_announcement(url)
