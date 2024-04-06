# E3 HW Reminder
**Star My Repo if you think it is useful, THX**

## Demo Result
Turn annoucement on the website ![image](https://github.com/hac-ohmygod0193/E3_HW_Reminder/assets/62164142/d41127a8-4230-4b93-a03c-5845cc4506fc)

Into Line Notification
![image](https://github.com/hac-ohmygod0193/E3_HW_Reminder/assets/62164142/c950f5a1-1d50-4a85-817b-f71a127e20b1)

## Source of Inspiration
Too Lazy to login E3 to Check hw announcement lol. 

## Getting Start 
Clone all files to your
```
git clone https://github.com/hac-ohmygod0193/auto-e3.git
```
```
pip install -r requirements.txt
```
Here you need to paste your own secret key to enable the power of E3 HW Reminder
![image](https://github.com/hac-ohmygod0193/E3_HW_Reminder/assets/62164142/1b3f4133-b620-4ef9-9b14-2a33a16e1b52)

### Setup Gemini APi secret token
1. Head over to makersuite.google.com/app/apikey [visit](https://makersuite.google.com/app/apikey) and sign in with your Google account.

2. Under API keys, click the “Create API key in new project” button.
![image](https://github.com/hac-ohmygod0193/auto-e3/assets/62164142/26c6a39c-3ef4-4e7f-a10f-09b25a8df063)

3. generate google gemini api key
4. Copy the API key and keep it private. Do not publish or share the API key publicly.
![image](https://github.com/hac-ohmygod0193/auto-e3/assets/62164142/9f6ccf15-9fec-41e9-9e32-a1c1c8776679)

5. New Repository secrets `Name` called `GOOGLE_API_KEY` and paste the API key to `Secret` below

### Setup Line Notify Token secret token
1. Follow this [website](https://notify-bot.line.me/my/) to get the token as Secret
2. New Repository secrets `Name` called `LINE_NOTIFY_TOKEN` and paste the API key to `Secret` below

### Set up E3p cookie secret token
1. Login to your [E3](https://e3p.nycu.edu.tw/my/) first
2. Press F12, Click Network and press F5 to refresh your page.
3. Then Click the same icon web as below
   ![image](https://github.com/hac-ohmygod0193/E3_HW_Reminder/assets/62164142/bbfd2012-3339-46b3-ace7-9f6eb102102c)
4. Scroll down to the Requests Headers part and find the Cookie as below.
   ![image](https://github.com/hac-ohmygod0193/E3_HW_Reminder/assets/62164142/ba4bbd68-2262-482a-ae55-d8b787c9d94b)
5. New Repository secrets `Name` called `LINE_NOTIFY_TOKEN` and paste the Cookie you find to `Secret` below.

## Deploy scheduled bot with Github Actions
1. Create a `.github/workflows` directory in your repository on GitHub if this directory does not already exist.
2. In the `.github/workflows` directory, create a file named `actions.yml`. For more information, see "Creating new files."
3. Copy my actions.yml [here](https://github.com/hac-ohmygod0193/auto-e3/blob/main/.github/workflows/actions.yml)
<img width="952" alt="image" src="https://github.com/hac-ohmygod0193/auto-e3/assets/62164142/4b7685bc-bdbd-44ba-8c08-0acc230dbb6e">

4. You can set up your desired running schedule by changing this line `- cron: `0 6 * * *` # run every day at 6:00`. For more crontab settings , see [here](https://crontab.guru/)

## Reference
[Send LINE Notifications using Python](https://bustlec.github.io/note/2018/07/10/line-notify-using-python/)
[Line Notfiy Bot](https://notify-bot.line.me/my/)
