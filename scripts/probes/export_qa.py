import json

with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions = data.get("questions", {})

md_content = "# ElektroLearn — Barcha Savollar va To'g'ri Javoblar Bazasi\n\n"
md_content += f"> Jami to'plangan va tasdiqlangan savollar soni: **{len(questions)} ta**\n\n"
md_content += "| № | Savol | To'g'ri javob |\n"
md_content += "|---|---|---|\n"

for idx, (q_id, item) in enumerate(questions.items(), 1):
    prompt = item.get("prompt", "").replace("\n", " ").replace("|", "\\|").strip()
    opt_text = item.get("option_text", "").replace("\n", " ").replace("|", "\\|").strip()
    md_content += f"| {idx} | {prompt} | **{opt_text}** |\n"

with open("data/savollar_va_javoblar.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Eksport muvaffaqiyatli yakunlandi! {len(questions)} ta savol data/savollar_va_javoblar.md fayliga yozildi.")

