import os
import json
import time
import threading
import telebot
from telebot import types
from api.client import BaseClient

def load_env():
    env = {}
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

_env = load_env()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or _env.get("TELEGRAM_BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID") or _env.get("TELEGRAM_ADMIN_CHAT_ID", "6252971660").strip()

class TelegramQAManager:
    def __init__(self):
        self.token = BOT_TOKEN
        self.admin_chat_id = ADMIN_CHAT_ID
        self.bot = telebot.TeleBot(self.token) if self.token else None
        self.client = BaseClient()
        self.pending = {}
        self._load_pending()

    def _load_pending(self):
        if os.path.exists("data/pending_qa.json"):
            try:
                with open("data/pending_qa.json", "r", encoding="utf-8") as f:
                    self.pending = json.load(f)
            except Exception:
                self.pending = {}

    def _save_pending(self):
        os.makedirs("data", exist_ok=True)
        with open("data/pending_qa.json", "w", encoding="utf-8") as f:
            json.dump(self.pending, f, indent=2, ensure_ascii=False)

    def send_question(self, q, theory_title="", source="LESSON"):
        """
        Noma'lum savolni Telegram bot orqali foydalanuvchiga yuboradi.
        Variantlarni inline tugmalar ko'rinishida chiqaradi.
        """
        if not self.bot or not self.admin_chat_id:
            print("[TelegramQA] Bot yoki admin chat ID mavjud emas!")
            return False

        qid = q["id"]
        prompt = q.get("prompt", "")
        options = q.get("options", [])

        # Store in pending
        self.pending[qid] = {
            "qid": qid,
            "prompt": prompt,
            "options": options,
            "theory_title": theory_title,
            "source": source,
            "status": "WAITING_USER",
            "created_at": time.time()
        }
        self._save_pending()

        # Build message
        letters = ["A", "B", "C", "D", "E", "F"]
        emojis = ["🅰️", "🅱️", "🅲", "🅳", "🅴", "🅵"]

        lines = [
            "❓ <b>NOMA'LUM SAVOL UCHRADI!</b>",
            f"📚 <b>Modul:</b> <i>{theory_title}</i>\n" if theory_title else "",
            f"📝 <b>Savol:</b>\n{prompt}\n",
            "<b>Variantlar:</b>"
        ]

        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []

        for i, opt in enumerate(options):
            let = letters[i] if i < len(letters) else str(i+1)
            emoji = emojis[i] if i < len(emojis) else f"[{let}]"
            opt_id = opt.get("id")
            opt_text = opt.get("optionText") or opt.get("text", "")
            lines.append(f"{emoji} <b>{let})</b> {opt_text}")
            buttons.append(types.InlineKeyboardButton(
                text=f"{emoji} {let}",
                callback_data=f"ans:{qid[:12]}:{i}"
            ))

        markup.add(*buttons)
        text = "\n".join([line for line in lines if line])

        msg = self.bot.send_message(
            int(self.admin_chat_id),
            text,
            parse_mode="HTML",
            reply_markup=markup
        )
        self.pending[qid]["message_id"] = msg.message_id
        self._save_pending()
        print(f"[TelegramQA] Savol Telegramga yuborildi (QID: {qid})")
        return msg.message_id

    def handle_user_selection(self, call):
        """
        Foydalanuvchi tugmani bosganda ishlaydigan callback funksiya.
        """
        data = call.data
        if not data.startswith("ans:"):
            return

        parts = data.split(":")
        short_qid = parts[1]
        opt_idx = int(parts[2])

        # Find full qid in pending
        target_q = None
        target_qid = None
        for qid, qdata in self.pending.items():
            if qid.startswith(short_qid):
                target_q = qdata
                target_qid = qid
                break

        if not target_q:
            self.bot.answer_callback_query(call.id, "❌ Ushbu savol muddati o'tgan yoki topilmadi.")
            return

        selected_opt = target_q["options"][opt_idx]
        selected_opt_id = selected_opt.get("id")
        selected_text = selected_opt.get("optionText") or selected_opt.get("text", "")

        # Submit answer to ElektroLearn API
        self.bot.answer_callback_query(call.id, f"Variant tanlandi: {selected_text[:30]}...")

        print(f"[TelegramQA] Foydalanuvchi javob tanladi: {selected_opt_id}")
        source = target_q.get("source", "LESSON")
        res = self.client.post("/progress/answer", data={
            "questionId": target_qid,
            "selectedOptionId": selected_opt_id,
            "source": source
        })

        is_correct = res.get("isCorrect", False)
        hearts_count = res.get("hearts", {}).get("heartsCount", "Noma'lum")
        earned_xp = res.get("earnedXp", 0)

        # Update Knowledge Base if correct
        if is_correct:
            with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
                kb = json.load(f)
            kb.setdefault("questions", {})[target_qid] = {
                "correct_option_id": selected_opt_id,
                "correctOptionId": selected_opt_id,
                "prompt": target_q.get("prompt", ""),
                "option_text": selected_text,
                "verified": True,
                "source": "TELEGRAM_USER_SELECTION",
                "note": target_q.get("prompt", "")[:100]
            }
            with open("data/knowledge_base.json", "w", encoding="utf-8") as f:
                json.dump(kb, f, indent=2, ensure_ascii=False)
            print(f"[TelegramQA] ✅ To'g'ri javob KB ga saqlandi! Total KB: {len(kb.get('questions', {}))}")

            result_text = (
                f"✅ <b>TO'G'RI JAVOB! BARAKALLA!</b> 🎉\n\n"
                f"📝 <b>Savol:</b> {target_q['prompt']}\n"
                f"🎯 <b>Tanlangan to'g'ri javob:</b> {selected_text}\n\n"
                f"💾 <i>Javoblar bazasiga muvaffaqiyatli qo'shildi.</i>\n"
                f"⚡ <b>Olingan XP:</b> +{earned_xp} XP\n"
                f"❤️ <b>Hozirgi yuraklar:</b> {hearts_count}/5"
            )
        else:
            result_text = (
                f"❌ <b>NOTO'G'RI JAVOB BO'LDI!</b> ⚠️\n\n"
                f"📝 <b>Savol:</b> {target_q['prompt']}\n"
                f"⚠️ <b>Tanlangan javob:</b> {selected_text}\n\n"
                f"🛑 <b>Qat'iy qoidaga ko'ra test to'xtatildi!</b>\n"
                f"❤️ <b>Qolgan yuraklar:</b> {hearts_count}/5\n"
                f"<i>(Iltimos, keyingi harakatni tanlang yoki tiklanishni kuting)</i>"
            )

        # Update Telegram message
        try:
            self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=result_text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"[TelegramQA] Edit message error: {e}")

        # Mark done
        target_q["status"] = "RESOLVED"
        target_q["is_correct"] = is_correct
        target_q["hearts_after"] = hearts_count
        self._save_pending()

qa_manager = TelegramQAManager()
