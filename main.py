import requests
from bs4 import BeautifulSoup
import os
import datetime
import re
from groq import Groq

# Load environment variables
e3p_cookie = os.environ["E3P_COOKIE"]
line_notify_token = os.environ["LINE_NOTIFY_TOKEN"]
groq_api_keys = os.environ["GROQ_API_KEY"]
client = Groq(
    api_key=groq_api_keys,
)
model_mapping = {
    "0": "llama2-70b-4096",
    "1": "mixtral-8x7b-32768",
    "2": "gemma-7b-it",
}

current_time = datetime.datetime.now()+datetime.timedelta(hours=8)
current_date = current_time.date()
print(current_date)

def groq_api(llm_prompt: str):
    select_model = "1"
    model = model_mapping[select_model]
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": str(llm_prompt),
                    
                }
            ],
            model=model,temperature = 0.0,
    )
    response = chat_completion.choices[0].message.content
    if model == "gemma-7b-it":
        response = response.replace('*', '').replace('-', '')
    return response
def gemini_api(llm_prompt: str):
    from langchain_google_genai import (
        ChatGoogleGenerativeAI,
        HarmBlockThreshold,
        HarmCategory,
    )
    import google.generativeai as genai
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
    response = gemini_pro.invoke(llm_prompt).content
    response = response.replace('*', '').replace('-', '')
    return response
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


prompt = """
---------------------
{message}
---------------------
Summarize this homework announcement for me in Traditional Chinese and less than 50 words.
Use only bullet points to summarize the announcement.
Don't include any unnecessary information.
公告內容摘要如下:
"""


def send_e3_hw_announcement(url: str):
    """Fetch the page content"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "authority": "e3p.nycu.edu.tw",
        "method": "GET",
        "path": "/my/",
        "scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-TW,zh;q=0.9",
        "Cookie": e3p_cookie,
        "Referer": "https://portal.nycu.edu.tw/",
    }

    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.Session()
    html = session.get(url, headers=headers)
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html.text)

    soup = BeautifulSoup(html.text, "html.parser")
    headlines = soup.find_all(name="h3",
                              attrs={"class": "name d-inline-block"})
    tags = soup.find_all(name="div", attrs={"class": "event mt-3"})
    final_message = ""
    coming_soon_message = ""
    prefix_message = "\n今天日期: " + str(
        current_date) + '\n' "近三日的作業公告\n" + '=' * 16 + '\n'
    more_than_n_days = False
    hw_time_delta = 3
    for i in range(len(tags)):
        block = tags[i]
        headline = headlines[i]
        message = "\n"
        block_title = block.find_all(name="div", attrs={"class": "col-11"})
        message += headline.text + '\n' + '截止時間:\n'
        for title in block_title[:2]:
            if title.text == '課程事件':
                continue
            date_pattern = r"\d{2}月 \d{2}日"
            date_match = re.search(date_pattern, title.text)
            message += title.text + '\n'
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
        
        if block_title[2].text == '\n':
            response = ""
        else:
            llm_prompt = prompt.format(message=block_title[2].text)
            response = gemini_api(llm_prompt)
            message += '\n'+ response + '\n'
        if more_than_n_days:
            if(final_message == ""):
                coming_soon_message = "\n今天日期: " + str(current_date) + "\n恭喜!近三日內無作業公告\n"
                coming_soon_message = "最接近的作業公告是:\n" + message + '\n課程:\n' + block_title[-1].text[12:]+'\n'+'=' * 16 + '\n'
            break
        final_message += (message + '\n課程:\n' + block_title[-1].text[12:]+'\n'+'=' * 16 + '\n')
    if final_message == "":
        final_message = coming_soon_message
    else:
        final_message = prefix_message + '\n' + final_message
    print(final_message)
    #lineNotifyMessage(line_notify_token,  final_message)

url = 'https://e3p.nycu.edu.tw/calendar/view.php?view=upcoming'
send_e3_hw_announcement(url)
