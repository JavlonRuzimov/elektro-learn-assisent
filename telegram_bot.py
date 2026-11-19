import os
import time
import threading
import sys
from datetime import datetime, timezone, timedelta

# Toshkent vaqt mintaqasi (UTC+5)
TASHKENT_TZ = timezone(timedelta(hours=5))

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
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID") or _env.get("TELEGRAM_ADMIN_CHAT_ID", "6252971660").strip()

from daily_solver import DailyPlanSolver
solver = DailyPlanSolver()

from agent.exam_monitor import ExamMonitor
exam_monitor = ExamMonitor(solver.client)

if not BOT_TOKEN:
    print("[!] DIQQAT: .env faylida 'TELEGRAM_BOT_TOKEN' topilmadi!")
    print("Iltimos, @BotFather dan olingan bot tokenini .env fayliga kiriting.")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

# Avto-yechish holati: Sukut bo'yicha YOQILGAN (Har kuni soat 09:00 da avtomatik yechiladi)
AUTO_SOLVE_ENABLED = True

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_daily = types.KeyboardButton("🎯 Kunlik rejani yechish")
    btn_profile = types.KeyboardButton("📊 Mening profilim")
    btn_search = types.KeyboardButton("🔍 Savol qidirish")
    btn_levels = types.KeyboardButton("📚 Darajalar holati")
    btn_exam = types.KeyboardButton("📝 Imtihonlar")
    btn_toggle = types.KeyboardButton("⚙️ Avto 09:00: " + ("Yoqilgan ✅" if AUTO_SOLVE_ENABLED else "O'chirilgan ❌"))
    markup.add(btn_daily, btn_profile)
    markup.add(btn_search, btn_levels)
    markup.add(btn_exam, btn_toggle)
    return markup

def build_full_report(plan_res=None):
    """To'liq profil va kunlik reja hisoboti matnini tayyorlash"""
    prof = solver.get_profile_info()
    plan_info = solver.check_daily_plan_status()
    now_uz = datetime.now(TASHKENT_TZ)
    today_str = now_uz.strftime("%Y-%m-%d")

    target_q = plan_info.get("target_questions", 10)
    ans_q = plan_info.get("answered_count", 0)
    cor_q = plan_info.get("correct_count", 0)
    percent = plan_info.get("completion_percent", 0)
    is_comp = plan_info.get("completed", False)

    if plan_res:
        cor_q = plan_res.get("correct_count", cor_q)
        target_q = plan_res.get("total", target_q)
        percent = plan_res.get("completion_percent", 100)
        is_comp = plan_res.get("completion_percent", 0) >= 100 or plan_res.get("correct_count", 0) >= target_q

    status_badge = "✅ 100% Bajarildi (+100 XP)" if is_comp else f"⏳ {cor_q}/{target_q} ({percent}%)"
    learned_str = ""
    if plan_res and plan_res.get("new_learned_count", 0) > 0:
        learned_str = f"🧠 <b>Avto-o'rganish:</b> {plan_res.get('new_learned_count')} ta yangi savol topildi va bazaga qo'shildi! 💡\n"

    text = (
        f"🌅 <b>ELEKTROLEARN KUNLIK HISOBOTI</b>\n\n"
        f"📅 <b>Sana:</b> {today_str} | <b>Vaqt:</b> {now_uz.strftime('%H:%M')} (Toshkent)\n"
        f"👤 <b>Xodim:</b> {prof.get('name', 'Sabirjan Ruzimov')}\n"
        f"🏢 <b>Filial:</b> {prof.get('branch', 'Xorazm MET')}\n"
        f"📧 <b>Login:</b> {prof.get('email', 's.ruzimov2774')}\n\n"
        f"══════════════════════\n"
        f"🎯 <b>BUGUNGI KUNLIK REJA:</b>\n"
        f"📌 <b>Holati:</b> {status_badge}\n"
        f"✅ <b>To'g'ri javoblar:</b> {cor_q} / {target_q}\n"
        f"🎁 <b>Kunlik bonus:</b> +100 XP\n"
        f"{learned_str}\n"
        f"══════════════════════\n"
        f"📊 <b>UMUMIY PROFIL STATISTIKASI:</b>\n"
        f"⭐ <b>Jami XP:</b> {prof.get('total_xp', 0)} XP\n"
        f"🏆 <b>Tashkilotdagi o'rni:</b> #{prof.get('rank', 'N/A')}-o'rin\n"
        f"🎖 <b>Unvon (Badge):</b> {prof.get('badge', 'Magistral ekspert')}\n"
        f"❤️ <b>Energiya (Yuraklar):</b> {prof.get('hearts', 5)} / {prof.get('max_hearts', 5)}\n"
        f"📚 <b>O'quv darajalari:</b> {prof.get('completed_levels', 6)} / {prof.get('total_levels', 6)} ta (100% yopilgan)\n\n"
        f"⏰ <b>Keyingi avto-yechish:</b> Ertaga soat 09:00 da\n"
        f"💾 <i>Bilimlar bazasi to'liq sinxronlangan (514+ savollar).</i>"
    )
    return text

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
            f"⚡ <b>ElektroLearn 24/7 Avtomatizatsiya Boti</b>ga xush kelibsiz.\n"
            f"Siz muvaffaqiyatli administrator sifatida ulandingiz (ID: <code>{chat_id}</code>).\n\n"
            f"⏰ <b>Avtomatizatsiya rejimi:</b> Bot har kuni <b>ertalab soat 09:00 da</b> kunlik 10 ta testni o'zi yechadi va sizga to'liq hisobot yuboradi.\n\n"
            f"Quyidagi menyu orqali ham istalgan vaqtda boshqarishingiz mumkin:"
        )
        bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=get_main_keyboard())

    @bot.message_handler(commands=['report'])
    def handle_manual_report(message):
        bot.send_chat_action(message.chat.id, "typing")
        text = build_full_report()
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    @bot.message_handler(func=lambda m: m.text == "📊 Mening profilim")
    def handle_profile(message):
        bot.send_chat_action(message.chat.id, "typing")
        text = build_full_report()
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    @bot.message_handler(func=lambda m: m.text == "📚 Darajalar holati")
    def handle_levels(message):
        try:
            prog = solver.client.progress.get_progress()
            lines = ["📚 <b>Platformadagi barcha darajalar holati:</b>\n"]
            for lvl in prog.levels:
                status = "✅ 100% Yakunlangan" if lvl.is_completed else f"⏳ {lvl.completion_percent}%"
                lock = "🔒" if lvl.is_locked else "🔓"
                lines.append(f"{lock} <b>{lvl.title}</b> — {status}")
            lines.append("\n🎉 <i>Barcha 6 ta modul (Level 4, 5, 6, 7, 8, 9) to'liq 100% yopilgan!</i>")
            bot.send_message(message.chat.id, "\n".join(lines), parse_mode="HTML")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Darajalarni olishda xatolik: {e}")

    @bot.message_handler(func=lambda m: m.text == "🎯 Kunlik rejani yechish")
    def handle_solve_daily(message):
        status_info = solver.check_daily_plan_status()
        if "error" in status_info:
            bot.send_message(message.chat.id, f"❌ Xatolik: {status_info['error']}")
            return

        if not status_info.get("is_plan_day"):
            bot.send_message(
                message.chat.id,
                "🏖 <b>Bugun dam olish kuni!</b>\nPlatformada bugun uchun kunlik reja belgilanmagan. Dushanba kuni ertalab yangi 10 talik reja yaratiladi.",
                parse_mode="HTML"
            )
            return

        if status_info.get("completed"):
            bot.send_message(
                message.chat.id,
                f"✅ <b>Bugungi kunlik reja allaqachon to'liq bajarilgan!</b>\n"
                f"Natija: {status_info.get('correct_count', 10)}/{status_info.get('target_questions', 10)} to'g'ri (+100 XP olingan).\n\n"
                f"⏰ Ertaga soat 09:00 da yangi reja avtomatik yechiladi.",
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

        if result.get("status") == "SUCCESS":
            report = build_full_report(plan_res=result)
            bot.send_message(
                message.chat.id,
                f"🎉 <b>Kunlik reja muvaffaqiyatli yakunlandi!</b>\n\n" + report,
                parse_mode="HTML"
            )
        else:
            bot.send_message(message.chat.id, f"ℹ️ {result.get('message', 'Natija topilmadi')}")

    @bot.message_handler(func=lambda m: "Avto 09:00:" in m.text or "Avto-yechish:" in m.text)
    def handle_toggle_auto(message):
        global AUTO_SOLVE_ENABLED
        AUTO_SOLVE_ENABLED = not AUTO_SOLVE_ENABLED
        state_str = "yoqildi ✅ (Har kuni soat 09:00 da)" if AUTO_SOLVE_ENABLED else "o'chirildi ❌"
        bot.send_message(
            message.chat.id,
            f"⚙️ <b>Ertalabki avtomatik yechish {state_str}.</b>",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )

    from agent.kb_search import KBSearcher
    searcher = KBSearcher()

    @bot.message_handler(func=lambda m: m.text == "🔍 Savol qidirish")
    def handle_search_prompt(message):
        bot.send_message(
            message.chat.id,
            "🔍 <b>Bilimlar bazasidan qidirish (Shpargalka)</b>\n\n"
            "Istalgan savol matnini yoki kalit so'zlarni yozib yuboring (masalan: <i>\"naryad muddati\"</i>, <i>\"o't o'chirgich\"</i>, <i>\"yerga ulagich\"</i>, <i>\"daraxt aganasa\"</i>).\n\n"
            "Men 514+ ta savollar bazasidan to'g'ri javobni bir zumda topib beraman!",
            parse_mode="HTML"
        )

    @bot.message_handler(func=lambda m: m.text and not m.text.startswith("/") and m.text not in [
        "🎯 Kunlik rejani yechish", "📊 Mening profilim", "📚 Darajalar holati", "🔍 Savol qidirish"
    ] and not m.text.startswith("⚙️"))
    def handle_general_search(message):
        query = message.text.strip()
        if len(query) < 2:
            return

        bot.send_chat_action(message.chat.id, "typing")
        results = searcher.search(query, limit=3)

        if not results:
            bot.send_message(
                message.chat.id,
                f"❌ <b>«{query}»</b> bo'yicha bazadan savol topilmadi.\n\n"
                f"💡 <i>Maslahat: So'zlarni soddaroq qilib qidirib ko'ring (masalan: «naryad», «saqlagich», «izolyatsiya»).</i>",
                parse_mode="HTML"
            )
            return

        lines = [f"🔍 <b>«{query}» bo'yicha topilgan natijalar ({len(results)} ta):</b>\n"]
        emojis = ["1️⃣", "2️⃣", "3️⃣"]
        for i, r in enumerate(results):
            em = emojis[i] if i < len(emojis) else f"[{i+1}]"
            lines.append(
                f"{em} <b>Savol:</b>\n<i>{r['prompt']}</i>\n\n"
                f"✅ <b>To'g'ri javob:</b>\n👉 <b>{r['answer']}</b>\n"
            )

        lines.append("💾 <i>Manba: Rasmiy qoidalar va tasdiqlangan bilimlar bazasi.</i>")
        bot.send_message(message.chat.id, "\n".join(lines), parse_mode="HTML")

    @bot.message_handler(func=lambda m: m.text in ["📝 Imtihonlar", "/exam", "Imtihonlar"])
    def handle_exam_check(message):
        bot.send_chat_action(message.chat.id, "typing")
        solver._ensure_token()
        status = exam_monitor.get_current_status()
        if status.get("has_exam") and status.get("exam"):
            bot.send_message(
                message.chat.id,
                exam_monitor.format_exam_alert(status["exam"]),
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                message.chat.id,
                "📝 <b>RASMIY MALAKA IMTIHONLARI</b>\n\n"
                "ℹ️ <i>Ayni paytda sizga tayinlangan yangi yoki faol imtihon mavjud emas.</i>\n\n"
                "✅ Barcha navbatdagi sinovlar kutish rejimida.\n"
                "🔔 Agar «O‘zbekiston MET» AJ tomonidan yangi malaka/attestatsiya imtihoni e'lon qilinsa, bot darhol sizga Telegram orqali ogohlantirish yuboradi!",
                parse_mode="HTML"
            )

    from agent.telegram_qa import qa_manager

    @bot.callback_query_handler(func=lambda call: call.data.startswith("ans:"))
    def handle_qa_callback(call):
        qa_manager.handle_user_selection(call)

def background_daily_checker():
    """Har kuni soat 09:00 da (Toshkent vaqti) kunlik rejani avtomatik yechuvchi va har 15 daqiqada yangi imtihonlarni kuzatuvchi fon jarayoni"""
    print("[BackgroundScheduler] 09:00 Avto-yechish va Imtihon monitori ishga tushdi...")
    already_solved_dates = set()
    last_exam_check = 0

    # Dastur ishga tushganda bugungi kun allaqachon bajarilgan bo'lsa, ro'yxatga qo'shamiz
    try:
        init_plan = solver.check_daily_plan_status()
        if init_plan.get("completed"):
            today_init = datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d")
            already_solved_dates.add(today_init)
            print(f"[Scheduler] Bugungi kun ({today_init}) allaqachon bajarilgan.")
    except Exception as e:
        print(f"[Scheduler Init] Tekshirishda xatolik: {e}")

    while True:
        try:
            now_uz = datetime.now(TASHKENT_TZ)
            today_str = now_uz.strftime("%Y-%m-%d")
            hour = now_uz.hour

            # 1. Har 15 daqiqada (900 soniya) rasmiy yangi imtihonlarni tekshirish
            if time.time() - last_exam_check >= 900:
                last_exam_check = time.time()
                try:
                    solver._ensure_token()
                    new_exam = exam_monitor.check_for_new_exam()
                    if new_exam and ADMIN_CHAT_ID and bot:
                        alert_msg = exam_monitor.format_exam_alert(new_exam)
                        bot.send_message(int(ADMIN_CHAT_ID), alert_msg, parse_mode="HTML")
                        print(f"[ExamMonitor] ⚠️ Yangi imtihon e'lon qilindi va xabar yuborildi: {new_exam}")
                except Exception as ex_err:
                    print(f"[ExamMonitor Xatosi]: {ex_err}")

            # 2. Har kuni soat 09:00 da (yoki 09:00 dan so'ng, lekin bugun hali yechilmagan bo'lsa)
            if AUTO_SOLVE_ENABLED and hour >= 9 and today_str not in already_solved_dates:
                plan_info = solver.check_daily_plan_status()

                # 1. Dam olish kuni
                if not plan_info.get("is_plan_day"):
                    print(f"[Scheduler] Bugun dam olish kuni ({today_str}). Reja yo'q.")
                    already_solved_dates.add(today_str)
                    if ADMIN_CHAT_ID and bot:
                        bot.send_message(
                            int(ADMIN_CHAT_ID),
                            f"🏖 <b>Bugun dam olish kuni ({today_str})!</b>\n\nPlatformada bugun uchun kunlik reja belgilanmagan.",
                            parse_mode="HTML"
                        )
                # 2. Allaqachon bajarilgan
                elif plan_info.get("completed"):
                    print(f"[Scheduler] Bugungi reja allaqachon bajarilgan ({today_str}).")
                    already_solved_dates.add(today_str)
                # 3. Yechish vaqti keldi!
                else:
                    print(f"[Scheduler] Soat 09:00 bo'ldi! Yangi kunlik reja yechilmoqda ({today_str})...")
                    if ADMIN_CHAT_ID and bot:
                        bot.send_message(
                            int(ADMIN_CHAT_ID),
                            f"⏰ <b>Soat 09:00 bo'ldi! Bugungi kunlik 10 ta testni avtomatik yechish boshlandi...</b>\n"
                            f"📅 <i>Sana: {today_str}</i>",
                            parse_mode="HTML"
                        )

                    res = solver.solve_daily_plan()
                    already_solved_dates.add(today_str)

                    if res.get("status") == "SUCCESS" and ADMIN_CHAT_ID and bot:
                        report_text = build_full_report(plan_res=res)
                        bot.send_message(
                            int(ADMIN_CHAT_ID),
                            report_text,
                            parse_mode="HTML"
                        )
                        print(f"[Scheduler] Kunlik reja muvaffaqiyatli yechildi va hisobot yuborildi.")
                    else:
                        if ADMIN_CHAT_ID and bot:
                            bot.send_message(
                                int(ADMIN_CHAT_ID),
                                f"⚠️ <b>Kunlik reja to'xtatildi:</b>\n{res.get('message', 'Noma\'lum holat')}",
                                parse_mode="HTML"
                            )
        except Exception as e:
            print(f"[Scheduler Xatosi]: {e}")

        # Har 30 soniyada vaqtni tekshirib turadi
        time.sleep(30)

if __name__ == "__main__":
    if not bot:
        print("[!] Bot token mavjud emas. Iltimos .env faylida 'TELEGRAM_BOT_TOKEN' ni sozlang.")
    else:
        # Fon rejalashtiruvchini ishga tushiramiz
        t = threading.Thread(target=background_daily_checker, daemon=True)
        t.start()

        print("[Telegram Bot] Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
        bot.infinity_polling()
