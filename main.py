import sys
import argparse
from config import Config
from api import ElektroLearnClient
from agent import AgentRunner, KnowledgeBase

def print_banner():
    print("=" * 65)
    print("        ELEKTROLEARN - AVTOMATLASHTIRILGAN AGENT TIZIMI        ")
    print("=" * 65)

def show_status(client: ElektroLearnClient):
    print("\n[1] FOYDALANUVCHI PROFILI:")
    try:
        user = client.auth.get_me()
        print(f"  Ism-familiya : {user.full_name}")
        print(f"  Email/Login  : {user.email}")
        print(f"  Roli         : {user.role}")
        if user.organizations:
            print(f"  Tashkilot    : {user.organizations[0].name}")
    except Exception as e:
        print(f"  Xatolik: {e}")

    print("\n[2] BUGUNGI KUNLIK REJA:")
    try:
        plan = client.daily_plan.get_today()
        print(f"  Sana         : {plan.plan_date}")
        print(f"  Holati       : {plan.correct_count}/{plan.daily_goal_correct} to'g'ri ({plan.completion_percent}%)")
        is_done = "HA (100%)" if plan.completed else "YO'Q"
        print(f"  Yakunlangan  : {is_done}")
    except Exception as e:
        print(f"  Xatolik: {e}")

    print("\n[3] BOSQICHLAR (LEVELS) VA PROGRESS:")
    try:
        prog = client.progress.get_progress()
        print(f"  Jami XP      : {prog.total_xp} XP")
        print(f"  Unvon        : {prog.badge_label} (Chaqmoqlar: {prog.badge_bolts})")
        print(f"  Tugatilgan   : {prog.completed_levels} ta daraja")
        print("\n  Darajalar ro'yxati:")
        for idx, lvl in enumerate(prog.levels, 1):
            lock_status = "🔒 Qulflangan" if lvl.is_locked else "🔓 Ochiq"
            print(f"    {idx}. [{lvl.order_index}] {lvl.title}")
            print(f"       Holat: {lock_status} | Progress: {lvl.completion_percent}% ({lvl.correct_answers_count} to'g'ri / {lvl.attempts_count} urinish)")
            print(f"       ID: {lvl.id}")
    except Exception as e:
        print(f"  Xatolik: {e}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="ElektroLearn Avtomatlashtirilgan Agent")
    parser.add_argument("--status", action="store_true", help="Profil va progress holatini ko'rish")
    parser.add_argument("--plan", action="store_true", help="Bugungi kunlik rejani avtomat bajarish")
    parser.add_argument("--level", type=str, help="Berilgan level ID bo'yicha savollarni yechish")
    parser.add_argument("--all-levels", action="store_true", help="Barcha mavjud level-larni ketma-ket 100 foiz bajarish")
    args = parser.parse_args()

    print_banner()

    client = ElektroLearnClient()
    kb = KnowledgeBase()
    runner = AgentRunner(client=client, kb=kb)

    if args.status:
        show_status(client)
    elif args.plan:
        runner.complete_daily_plan()
    elif args.level:
        runner.complete_active_level(args.level)
    elif args.all_levels:
        runner.complete_all_levels()
    else:
        show_status(client)
        print("\nFOYDALANISH UCHUN BUYRUQLAR:")
        print("  python main.py --status         -> Umumiy profil va ochiq darajalar holati")
        print("  python main.py --plan           -> Bugungi kunlik 10 ta savolni avtomatik yechish")
        print("  python main.py --all-levels     -> Barcha level topshiriqlarini 100% bajarish")
        print("  python main.py --level <ID>     -> Bitta aniq levelni yechish")

if __name__ == "__main__":
    main()
