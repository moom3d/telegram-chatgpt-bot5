import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from collections import defaultdict

# 设置 OpenAI API 密钥
openai.api_key = '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'

# Telegram 机器人 Token
TELEGRAM_TOKEN = '7013947240:AAHx4fM4_4gXLGGSKpcXKMwiXdjW-8t8fy0'

# 用来保存每个用户的对话历史
user_contexts = defaultdict(list)

# 定义一个函数来与 OpenAI 接口交互
def chat_with_gpt(user_id: int, message: str) -> str:
    # 获取当前用户的上下文
    user_messages = user_contexts[user_id]

    # 限制上下文大小，防止过多历史消息影响响应
    if len(user_messages) > 10:

         user_messages = user_messages[-10:]

    # 添加用户输入的消息
    user_messages.append({"role": "user", "content": message})

    # 调用 OpenAI 接口
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 或者使用 gpt-4
        messages=user_messages,
        max_tokens=150
    )

    # 获取 GPT 回复的内容
    bot_response = response.choices[0].message['content'].strip()

    # 将机器人回复添加到上下文
    user_messages.append({"role": "assistant", "content": bot_response})

    # 更新上下文
    user_contexts[user_id] = user_messages

    return bot_response

# 处理用户发送的消息
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id  # 获取用户ID
    user_message = update.message.text  # 获取用户输入的消息

    print(f"Received message from user {user_id}: {user_message}")  # 打印调试信息

    # 获取机器人的回复
    bot_response = chat_with_gpt(user_id, user_message)

    # 回复用户
    await update.message.reply_text(bot_response)

# 启动 Telegram 机器人
def main() -> None:
    # 使用 Application 类替代 Updater
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加消息处理器，确保过滤所有文本消息
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # 启动机器人
    application.run_polling()

if __name__ == '__main__':
    main()
