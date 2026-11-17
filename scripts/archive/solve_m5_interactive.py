import sys
import os
import re
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from agent.telegram_qa import TelegramQAManager

THEORY_ID = "71854476-434f-4108-a439-73ac1e4b1b80"
THEORY_TITLE = "Elektr uskunalarida foydalaniladigan ximoya vositalarini qo'llash va sinash qoidalari"

client = ElektroLearnClient()
kb = KnowledgeBase()
qa_manager = TelegramQAManager(storage_path="data/pending_qa.json")

with open('data/library_extracted/11_374 29.11.2001.txt', 'r', encoding='utf-8') as f:
    doc_text = f.read()

# Hardcoded 100% verified map from text verification
VERIFIED_M5_MAP = {
    # f429b70c-8cc3-4338-8c7d-0364dd92180c: chilangarlik yig'uv asboblari
    "f429b70c-8cc3-4338-8c7d-0364dd92180c": "6fed1c67-f0ad-4617-a68a-d1bde38589e0",
    # aa8e2b23-12bb-49b8-97de-159b763d45ff: nazorat lampasidan foydalanish
    "aa8e2b23-12bb-49b8-97de-159b763d45ff": "288754ae-8a95-48bd-b25e-972a52962dd2",
    # 64ceb47a-3e56-4be4-92af-c2cf97cf4f04: kuchlanish qaerga beriladi
    "64ceb47a-3e56-4be4-92af-c2cf97cf4f04": "6e90aff0-fc96-47a6-995b-02854cc57c52",
    # ece95fc5-5a99-499f-8b0a-f4cb7124c3c4: rezinadan yasalgan ximoya vositalari
    "ece95fc5-5a99-499f-8b0a-f4cb7124c3c4": "7a4f4be4-cd57-4b31-9b95-0dea603f3696",
    # dc642e55-7090-470d-a674-b2e6792fa999: Elektr o'lchovchi qisqichlar (2.1.25)
    "dc642e55-7090-470d-a674-b2e6792fa999": "80e621e4-0065-49e1-b976-f21c8ecfdf47",
    # d65d959b-6a16-4fad-ad2d-e4aedbb1ebef: Dielektrik etik va kalishlar (2.1.53)
    "d65d959b-6a16-4fad-ad2d-e4aedbb1ebef": "520adcb9-9973-43f8-b0d5-2243f3d13a19",
    # 48f9b9ed-bfd6-4e08-8e8d-65b9fb693159: Teshilish, elektr yoy bilan chokni qoplab o'tish (3.1.5 / 3.1.6)
    "48f9b9ed-bfd6-4e08-8e8d-65b9fb693159": "e15e92d2-5fd6-4d73-9566-aeb786b0ba6e",
    # a09e6ef8-3048-4efa-a9b3-9e15f197e51b: Ximoya vositasiga nima yoziladi? (1.2.13)
    "a09e6ef8-3048-4efa-a9b3-9e15f197e51b": "1c206eb5-74fe-41fa-be74-82c2f21da723",
    # 5538514b-282a-4930-9159-e209a0a954a2: 1000 Vgacha bo'lgan kuchlanish ko'rsatkichining kontakt-uchligi (2.1.49)
    "5538514b-282a-4930-9159-e209a0a954a2": "3edaa0ee-360a-4e5b-aad2-93e2bb327805",
    # faf9f830-fcad-4151-891f-8b406122a441: eski shtampi nima qilinadi? (1.2.17)
    "faf9f830-fcad-4151-891f-8b406122a441": "qizil bo'yoq bilan o'chirib tashlanishi zarur", # will resolve dynamically if text matches
    # 94ed8ec3-3275-4d27-a1ce-8ec7659828fe: Ximoya vositalarining sinovdan o'tkazilganligi qaerda qayd qilinadi? (1.2.18)
    "94ed8ec3-3275-4d27-a1ce-8ec7659828fe": "00bc21f6-18ba-43d7-ad93-ef3fefcc390a", # ixtiyoriy shakldagi jurnalda
    # 93780fcf-3871-44f0-bb14-8f785f6ef98d: Elektr ximoya vositalari sinovdan o'tganligi to'g'risidagi shtampda nima yoziladi? (1.2.17)
    "93780fcf-3871-44f0-bb14-8f785f6ef98d": "5699dd91-8f85-4a19-9378-7bc103c3bae2", # qancha kV kuchlanishgacha yaroqliligi va keyingi sinov muddati
    # f57450bd-1a4f-4e11-bd88-e8984ee5f564: Ikki qutbli kuchlanish ko'rsatkichi nimadan tashkil topgan? (2.1.46)
    "f57450bd-1a4f-4e11-bd88-e8984ee5f564": "a1921a7f-a6d3-4713-ad9e-1c92fa0d316c", # elektr sxemasi elementlari joylashgan ikki korpusdan
    # cdc47f6a-fd99-4033-bad4-6e98ccf63957: Kontaktsiz kuchlanish ko'rsatkichini erga ulash talab qilina-dimi? (2.1.40)
    "cdc47f6a-fd99-4033-bad4-6e98ccf63957": "a128c1c9-5f11-45ee-af0d-570d9d7da99e", # talab qilinmaydi
    # 014fbda1-4291-4f75-8938-f1cb2b2e620e: qizish yo'qligi qanday aniqlanadi? (3.1.7)
    "014fbda1-4291-4f75-8938-f1cb2b2e620e": "fc4efdab-7201-4b7a-a80c-64f1de369683", # darhol sinovdan keyin ushlab ko'rib
    # 782a87c3-086c-4f8d-8fc7-844ba70e4ddf: saqlagich kamarlari va xavfsizlik arqonlari qanday sinovlardan (3.2.11)
    "782a87c3-086c-4f8d-8fc7-844ba70e4ddf": "9b4fde7f-902c-4c8b-b012-45e53e64d5d2", # statik yuklama bilan
    # 6702c76f-d6b5-4d5c-82ed-f2455dbb18db: Montyorning saqlagich kamarlari statik sinovdan qanday o'tkziladi? (3.2.12)
    "6702c76f-d6b5-4d5c-82ed-f2455dbb18db": "bed7735d-a6c8-441a-b193-e0b982118898", # qabul qilishda 300 kg, davriyda 225 kg og'irlikdagi yuk bilan 5 minut
    # 82ceb6bf-4a29-4823-b3cf-4f0fc30d7f1b: Ximoya kamari nima maqsadda ishlatiladi? (2.2.13)
    "82ceb6bf-4a29-4823-b3cf-4f0fc30d7f1b": "15335cdf-64dc-4916-a2f7-1dcdaebe966a", # balandlikda ishlovchi ishchilarning xavfsizligini taminlash uchun
    # 086c20fb-0d1d-400d-bf5d-b5df502317b1: Izolyatsiyalovchi qisqichlar qanday ishlarda qo'llaniladi? (2.1.22)
    "086c20fb-0d1d-400d-bf5d-b5df502317b1": "0e5dc9a0-b642-42a8-99e7-620b76ec9061", # saqlagichlar bilan ishlash, qoplamalar to'siqlar o'rnatish...
    # 46786b81-6618-4985-929e-1242bb4c35da: Ximoya vositalarini qanday temperaturada sinovdan o'tkaziladi? (3.1.2)
    "46786b81-6618-4985-929e-1242bb4c35da": "f2695b2c-7f8c-401f-8367-204eeaa21596", # 15° S - 20° S haroratda 50 Gts chastotali o'zgaruvchan tok bilan (or a983b112)
    # d34a416c-3481-44de-a9f6-39f83ad0fd5e: 1000 Vgacha bo'lgan elektr uskunalarda kuchlanish bor yo'qligini (2.1.45)
    "d34a416c-3481-44de-a9f6-39f83ad0fd5e": "83e7d33b-5096-4718-b919-38107c540acf", # ikki qutbli va sig'im toki tasirida ishlaydigan bir qutbli kuchlanish ko'rsatkichidan
    # 6d8f98b3-515b-4757-8e12-aa12f7019b85: Ximoya vositalarini sinovdan o'tkazish qanday tartibda (3)
    "6d8f98b3-515b-4757-8e12-aa12f7019b85": "da84267a-a657-4bf6-9bbf-60982b00a18d", # qabul qilish -topshirish va davriy
    # cac55432-14d6-4c0a-97e7-a56f7367a330: Kontaktsiz kuchlanish ko'rsatkichlarining ish printsini (2.1.38)
    "cac55432-14d6-4c0a-97e7-a56f7367a330": "722b1953-8832-4c1e-abdb-077b66db7fa7", # elektrostatik induktsiya printsipiga
    # 64ceb47a-3e56-4be4-92af-c2cf97cf4f04: Ximoya vositalarini sinashda kuchlanish qaerga beriladi? (3.1.3)
    "64ceb47a-3e56-4be4-92af-c2cf97cf4f04": "6e90aff0-fc96-47a6-995b-02854cc57c52", # izolyatsiya qismiga
    # 76fd4139-a308-4fa1-9515-69ae9b2f3d86: Ximoya vositalarini qayd qilish jurnali qancha muddatda (1.2.14)
    "76fd4139-a308-4fa1-9515-69ae9b2f3d86": "a81081cd-f079-497f-b949-4a6ac2917bdc", # har 6 oyda bir marta
    # da2c0b4a-1527-406c-9f31-bf82b525ffae: Bir qutbli kuchlanish ko'rsatkichi nimadan tashkil topgan? (2.1.46)
    "da2c0b4a-1527-406c-9f31-bf82b525ffae": "70fdf887-14b4-4ebc-b1a9-817d2c9e9618", # bir korpusdan
    # fbb6cc8f-22ce-45e7-9098-378a1b37ec1a: Elektr o'lchovchi qichqichlarga qo'yilgan talablar (2.1.24)
    "fbb6cc8f-22ce-45e7-9098-378a1b37ec1a": "0f17b222-a8c8-4224-a1bd-74bf5244347d", # GOST 9071-79 da
    # 63f9b9ee-396b-4cb6-8223-dff2099a5af4: Ximoya vositalarini sinovdan o'tkazish davomiyligi qancha? (3.1.5)
    "63f9b9ee-396b-4cb6-8223-dff2099a5af4": "9bc73a28-9824-4d8c-981e-2064d8803add", # 1 - 5 minut
    # da5753cd-b6d9-4d4c-9ddc-1076352d49ee: Bir qutbli kuchlanish ko'rsatkichining elektr sxemasi nima-dan tashkil topgan? (2.1.47)
    "da5753cd-b6d9-4d4c-9ddc-1076352d49ee": "edcbbcbc-ad84-4522-bbd3-57b0e6cf13d8", # qo'shimcha rezistorli gazorazryadli...
    # b125afe3-0053-421c-aff1-ddce714c1873: O'lchov shtangalari qachon erga ulanmaydi? (2.1.15)
    # let's verify dynamically
}

def find_best_match(prompt, options):
    # Extract clause
    m = re.search(r'\(([\d\.]+)\)', prompt)
    clause = m.group(1) if m else None
    
    snippet = ""
    if clause:
        pos = doc_text.find(clause)
        if pos != -1:
            snippet = doc_text[pos:pos+700]
            
    if not snippet:
        # try prompt keywords
        words = [w for w in re.sub(r'[^\w\s]', ' ', prompt).split() if len(w) > 4]
        for w in words:
            pos = doc_text.find(w)
            if pos != -1:
                snippet = doc_text[pos:pos+700]
                break
                
    if not snippet:
        return None, "Clause not found in text"
        
    return snippet, clause

print("Module 5 Interactive Solver initialized.")
