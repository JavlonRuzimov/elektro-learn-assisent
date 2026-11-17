import os
import time
import threading
import sys
from datetime import datetime

os.makedirs("data", exist_ok=True)
if sys.stdout is None:
    sys.stdout = open("data/telegram_bot.log", "a", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open("data/telegram_bot_err.log", "a", encoding="utf-8")

import telebot
from telebot import types

def load_env_file():
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

_env = load_env_file()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or _env.get("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID") or _env.get("TELEGRAM_ADMIN_CHAT_ID", "").strip()

from daily_solver import DailyPlanSolver
solver = DailyPlanSolver()

if not BOT_TOKEN:
    print("[!] DIQQAT: .env faylida 'TELEGRAM_BOT_TOKEN' topilmadi!")
    print("Iltimos, @BotFather dan olingan bot tokenini .env fayliga kiriting.")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

# Avto-yechish holati (Foydalanuvchi buyrug'i bilan o'chirilgan - faqat qo'lda boshlanadi)
AUTO_SOLVE_ENABLED = False

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_daily = types.KeyboardButton("🎯 Kunlik rejani yechish")
    btn_profile = types.KeyboardButton("📊 Mening profilim")
    btn_levels = types.KeyboardButton("📚 Darajalar holati")
    btn_toggle = types.KeyboardButton("⚙️ Avto-yechish: " + ("Yoqilgan ✅" if AUTO_SOLVE_ENABLED else "O'chirilgan ❌"))
    markup.add(btn_daily, btn_profile)
    markup.add(btn_levels, btn_toggle)
    return markup

if bot:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        global ADMIN_CHAT_ID
        chat_id = str(message.chat.id)
        if not ADMIN_CHAT_ID:
            ADMIN_CHAT_ID = chat_id
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    content = f.read()
                if "TELEGRAM_ADMIN_CHAT_ID=" in content:
                    content = content.replace("TELEGRAM_ADMIN_CHAT_ID=", f"TELEGRAM_ADMIN_CHAT_ID={chat_id}")
                    with open(".env", "w", encoding="utf-8") as f:
                        f.write(content)
            except Exception:
                pass

        name = message.from_user.first_name or "Foydalanuvchi"
        text = (
            f"Assalomu alaykum, <b>{name}</b>!\n\n"
            f"⚡ <b>ElektroLearn Avtomatizatsiya Boti</b>ga xush kelibsiz.\n"
            f"Siz muvaffaqiyatli administrator sifatida ulandingiz (ID: <code>{chat_id}</code>).\n\n"
            f"Ushbu bot orqali har kungi 10 talik reja testlarini avtomatik yechish va platformadagi holatingizni kuzatib borishingiz mumkin.\n\n"
            f"Quyidagi tugmalardan birini tanlang:"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=get_main_keyboard())

    @bot.message_handler(func=lambda m: m.text == "📊 Mening profilim")
    def handle_profile(message):
        p = solver.get_profile_info()
        if "error" in p:
            bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {p['error']}")
            return

        text = (
            f"👤 <b>Foydalanuvchi:</b> {p['name']}\n"
            f"📧 <b>Login:</b> {p['email']}\n"
            f"⚡ <b>Jami to'plangan XP:</b> {p['total_xp']} XP\n"
            f"🎖 <b>Unvon (Badge):</b> {p['badge']}\n"
            f"❤️ <b>Energiya (Yuraklar):</b> {p['hearts']}/{p['max_hearts']}\n"
            f"🏆 <b>Tugatilgan darajalar:</b> {p['completed_levels']}/{p['total_levels']} ta"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    @bot.message_handler(func=lambda m: m.text == "📚 Darajalar holati")
    def handle_levels(message):
        try:
            prog = solver.client.progress.get_progress()
            lines = ["📚 <b>Platformadagi barcha darajalar:</b>\n"]
            for lvl in prog.levels:
                status = "✅ 100%" if lvl.is_completed else f"⏳ {lvl.completion_percent}% ({lvl.correct_answers_count} to'g'ri)"
                lock = "🔒" if lvl.is_locked else "🔓"
                lines.append(f"{lock} <b>{lvl.title}</b> — {status}")
            bot.send_message(message.chat.id, "\n".join(lines), parse_mode="HTML")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Darajalarni olishda xatolik: {e}")

    @bot.message_handler(func=lambda m: m.text == "🎯 Kunlik rejani yechish")
    def handle_solve_daily(message):
        # 1. Reja holatini tekshiramiz
        status_info = solver.check_daily_plan_status()
        if "error" in status_info:
            bot.send_message(message.chat.id, f"❌ Xatolik: {status_info['error']}")
            return

        if not status_info["is_plan_day"]:
            bot.send_message(
                message.chat.id,
                "🏖 <b>Bugun dam olish kuni!</b>\nPlatformada bugun uchun kunlik reja belgilanmagan. Dushanba kuni ertalab yangi 10 talik reja yaratiladi.",
                parse_mode="HTML"
            )
            return

        if status_info["completed"]:
            bot.send_message(
                message.chat.id,
                f"✅ <b>Bugungi kunlik reja allaqachon to'liq bajarilgan!</b>\n"
                f"Natija: {status_info['answered_count']}/{status_info['target_questions']} (+100 XP olingan).",
                parse_mode="HTML"
            )
            return

        status_msg = bot.send_message(
            message.chat.id,
            "🚀 <b>Kunlik 10 ta testni yechish boshlandi...</b>\n<i>Kutubxona va bilimlar bazasi tekshirilmoqda...</i>",
            parse_mode="HTML"
        )

        def on_progress(cur, total, prompt, is_correct):
            icon = "✅" if is_correct else "⚠️"
            try:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_msg.message_id,
                    text=(
                        f"⏳ <b>Testlar yechilmoqda: {cur}/{total}</b>\n\n"
                        f"{icon} <i>{prompt[:60]}...</i>"
                    ),
                    parse_mode="HTML"
                )
            except Exception:
                pass

        result = solver.solve_daily_plan(progress_callback=on_progress)

        if result["status"] == "SUCCESS":
            bot.send_message(
                message.chat.id,
                f"🎉 <b>Tabriklaymiz! Kunlik reja 100% muvaffaqiyatli yakunlandi!</b>\n\n"
                f"✅ <b>To'g'ri javoblar:</b> {result['correct_count']}/{result['total']}\n"
                f"🎁 <b>Olingan bonus:</b> +{result['bonus_xp']} XP\n"
                f"📈 <b>Progress:</b> {result['completion_percent']}%",
                parse_mode="HTML"
            )
        else:
            bot.send_message(message.chat.id, f"ℹ️ {result.get('message', 'Natija topilmadi')}")

    @bot.message_handler(func=lambda m: "Avto-yechish:" in m.text)
    def handle_toggle_auto(message):
        global AUTO_SOLVE_ENABLED
        AUTO_SOLVE_ENABLED = not AUTO_SOLVE_ENABLED
        state_str = "yoqildi ✅" if AUTO_SOLVE_ENABLED else "o'chirildi ❌"
        bot.send_message(
            message.chat.id,
            f"⚙️ <b>Ertalabki avtomatik yechish {state_str}.</b>",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )

    from agent.telegram_qa import qa_manager

    @bot.callback_query_handler(func=lambda call: call.data.startswith("ans:"))
    def handle_qa_callback(call):
        qa_manager.handle_user_selection(call)

def background_daily_checker():
    """Har 30 daqiqada tekshirib, yangi reja ochilganda avtomatik yechuvchi fon jarayoni"""
    print("[BackgroundScheduler] Fon rejimi ishga tushdi...")
    already_notified_dates = set()

    while True:
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            now_hour = datetime.now().hour

            # Har kuni ertalab soat 08:00 dan 23:00 gacha tekshiradi
            if AUTO_SOLVE_ENABLED and now_hour >= 8 and today_str not in already_notified_dates:
                plan_info = solver.check_daily_plan_status()
                if plan_info.get("is_plan_day") and not plan_info.get("completed"):
                    print(f"[Scheduler] Yangi reja topildi ({today_str}). Yechish boshlanmoqda...")
                    res = solver.solve_daily_plan()
                    already_notified_dates.add(today_str)
                    
                    if res.get("status") == "SUCCESS" and ADMIN_CHAT_ID and bot:
                        bot.send_message(
                            int(ADMIN_CHAT_ID),
                            f"🌅 <b>Xayrli tong! Bugungi kunlik reja avtomatik yechildi!</b>\n\n"
                            f"✅ Yechilgan savollar: {res['solved']}/{res['total']}\n"
                            f"🎁 Bonus: +{res['bonus_xp']} XP qo'shildi!",
                            parse_mode="HTML"
                        )
        except Exception as e:
            print(f"[Scheduler Xatosi]: {e}")

        # 30 daqiqa kutish
        time.sleep(1800)

if __name__ == "__main__":
    if not bot:
        print("[!] Bot token mavjud emas. Iltimos .env faylida 'TELEGRAM_BOT_TOKEN' ni sozlang.")
    else:
        # Fon rejalashtiruvchini ishga tushiramiz
        t = threading.Thread(target=background_daily_checker, daemon=True)
        t.start()

        print("[Telegram Bot] Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
        bot.infinity_polling()
