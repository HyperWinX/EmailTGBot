# EmailTGBot
EmailTGBot is a simple Python bot powered by **telebot** library. Bot forwards all the messages from the email to registered telegram chats. Topics are supported too.
- Configurable timeout
- Logging

## Installation
1. Clone this repo
```bash
git clone https://github.com/HyperWinX/EmailTGBot.git && cd EmailTGBot
```
2. Build docker image
```bash
docker build -t emailtgbot .
```
3. Run it
```bash
docker run --env EMAIL="example@email.com" --env PASSWORD="app_password_for_account" --env TOKEN="tg_bot_token" ROOT="root_user_id" --mount type=bind,source=$(pwd)/data,target=/app/data --detach -it emailtgbot
```
4. It should work now!

> [!IMPORTANT]
> I created this project for personal needs. It is not intented to be actually used by everyone, and it's not configurable at all. Feel free to submit any fixes or improvements! And, if you will spot some issues, i'll do my best to fix them.