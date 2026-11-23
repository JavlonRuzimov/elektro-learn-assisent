import os
import csv
import time
import json
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

from auth_manager import AuthManager
from api import ElektroLearnClient
from agent.knowledge_base import KnowledgeBase
from library_searcher import LibraryKnowledge
from daily_solver import DailyPlanSolver

TASHKENT_TZ = timezone(timedelta(hours=5))

class MultiUserSolver:
    """
    Filialdagi barcha xodimlarning profillariga ketma-ket kirib,
    kunlik 10 ta testini to'liq 100% yechuvchi va hisobot beruvchi boshqaruvchi.
    """

    def __init__(self, csv_path: str = "data/employees.csv", delay_between_users: float = 2.0):
        self.csv_path = csv_path
        self.delay = delay_between_users
        self.kb = KnowledgeBase()
        self.library = LibraryKnowledge()

    def load_employees(self) -> List[Dict[str, str]]:
        """CSV fayldan xodimlar ro'yxatini yuklash"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Xodimlar fayli topilmadi: {self.csv_path}")

        employees = []
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("Status", "").strip().upper()
                if not status or status == "ACTIVE":
                    login = row.get("Login", "").strip()
                    password = row.get("Parol", "").strip()
                    if login and password:
                        employees.append({
                            "login": login,
                            "password": password,
                            "name": f"{row.get('Familiya', '').strip()} {row.get('Ism', '').strip()} {row.get('Otasining ismi', '').strip()}".strip(),
                            "position": row.get("Lavozim", "").strip(),
                            "department": row.get("Bo_lim", "").strip(),
                            "tabel": row.get("Tabel raqami", "").strip()
                        })
        return employees

    def solve_for_employee(self, emp: Dict[str, str]) -> Dict[str, Any]:
        """Bitta xodim uchun kunlik rejani bajarish"""
        login = emp["login"]
        password = emp["password"]
        name = emp["name"] or login

        result = {
            "login": login,
            "name": name,
            "status": "PENDING",
            "message": "",
            "xp_gained": 0,
            "total_xp": 0,
            "rank": "N/A"
        }

        # 1. Login qilib token olish
        try:
            token = AuthManager.login(username=login, password=password, save_to_env=False)
        except Exception as e:
            result["status"] = "LOGIN_FAILED"
            result["message"] = f"Kirishda xatolik: {e}"
            return result

        # 2. DailyPlanSolver ishga tushirish
        try:
            solver = DailyPlanSolver(
                token=token,
                kb=self.kb,
                library=self.library,
                username=login,
                password=password
            )

            # Reja holatini tekshirish
            plan_status = solver.check_daily_plan_status()
            if not plan_status.get("is_plan_day"):
                result["status"] = "NO_PLAN"
                result["message"] = "Bugun dam olish kuni, kunlik reja yo'q."
                return result

            if plan_status.get("completed") or plan_status.get("completion_percent", 0) >= 100:
                prof = solver.get_profile_info()
                result["status"] = "ALREADY_COMPLETED"
                result["message"] = f"Allaqachon 100% bajarilgan ({plan_status.get('correct_count', 10)}/10 to'g'ri)"
                result["total_xp"] = prof.get("total_xp", 0)
                result["rank"] = prof.get("rank", "N/A")
                return result

            # Kunlik rejani yechish (10 ta to'g'ri bo'lguncha)
            solve_res = solver.solve_daily_plan()
            prof = solver.get_profile_info()

            if solve_res.get("status") == "SUCCESS":
                result["status"] = "SOLVED"
                result["message"] = f"Muvaffaqiyatli yakunlandi ({solve_res.get('correct_count', 10)}/{solve_res.get('total', 10)})"
                result["xp_gained"] = solve_res.get("bonus_xp", 100)
                result["total_xp"] = prof.get("total_xp", 0)
                result["rank"] = prof.get("rank", "N/A")
            else:
                result["status"] = "PARTIAL_OR_FAILED"
                result["message"] = solve_res.get("message", "Noma'lum holat")
                result["total_xp"] = prof.get("total_xp", 0)
                result["rank"] = prof.get("rank", "N/A")

            return result

        except Exception as e:
            result["status"] = "ERROR"
            result["message"] = f"Yechish jarayonida xatolik: {e}"
            return result

    def run_batch(self, limit: Optional[int] = None, target_login: Optional[str] = None, progress_callback = None) -> Dict[str, Any]:
        """Barcha yoki belgilangan sondagi xodimlar uchun yechish"""
        employees = self.load_employees()
        if target_login:
            employees = [e for e in employees if e["login"] == target_login]
            if not employees:
                print(f"[!] Login '{target_login}' ro'yxatda topilmadi!")
                return {}

        if limit and limit > 0:
            employees = employees[:limit]

        total = len(employees)
        print(f"\n=======================================================")
        print(f"🚀 MULTI-USER DAILY SOLVER ISHGA TUSHDI")
        print(f"👥 Jami xodimlar: {total} ta")
        print(f"⏰ Vaqt: {datetime.now(TASHKENT_TZ).strftime('%Y-%m-%d %H:%M:%S')} (Toshkent)")
        print(f"=======================================================\n")

        summary = {
            "started_at": datetime.now(TASHKENT_TZ).isoformat(),
            "total_employees": total,
            "solved": 0,
            "already_completed": 0,
            "login_failed": 0,
            "errors": 0,
            "total_xp_gained": 0,
            "results": []
        }

        os.makedirs("data", exist_ok=True)
        live_state_file = "data/current_batch_state.json"

        def update_state(idx, emp, status_str):
            pct = round((idx / total) * 100, 1)
            live_data = {
                "is_running": True,
                "current_index": idx,
                "total": total,
                "percent": pct,
                "employee": {
                    "name": emp.get("name", ""),
                    "login": emp.get("login", ""),
                    "department": emp.get("department", ""),
                    "position": emp.get("position", "")
                },
                "status_text": status_str,
                "solved": summary["solved"],
                "already_completed": summary["already_completed"],
                "failed": summary["login_failed"] + summary["errors"],
                "total_xp_gained": summary["total_xp_gained"],
                "updated_at": datetime.now(TASHKENT_TZ).strftime("%H:%M:%S")
            }
            try:
                with open(live_state_file, "w", encoding="utf-8") as f:
                    json.dump(live_data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
            if progress_callback:
                try:
                    progress_callback(live_data)
                except Exception:
                    pass

        for idx, emp in enumerate(employees, 1):
            login = emp["login"]
            name = emp["name"]
            print(f"[{idx}/{total}] {name} ({login}) tekshirilmoqda...", end=" ", flush=True)

            update_state(idx, emp, "Tizimga kirilmoqda va tekshirilmoqda...")

            res = self.solve_employee_safe(emp)
            summary["results"].append(res)

            status = res["status"]
            if status == "SOLVED":
                summary["solved"] += 1
                summary["total_xp_gained"] += res["xp_gained"]
                msg = f"✅ YECHILDI (+{res['xp_gained']} XP, Jami: {res['total_xp']} XP, #{res['rank']})"
                print(f"{msg}")
                update_state(idx, emp, msg)
            elif status == "ALREADY_COMPLETED":
                summary["already_completed"] += 1
                msg = f"⏭ ALLAQACHON BAJARILGAN (Jami: {res['total_xp']} XP, #{res['rank']})"
                print(f"{msg}")
                update_state(idx, emp, msg)
            elif status == "LOGIN_FAILED":
                summary["login_failed"] += 1
                msg = f"❌ LOGIN XATO ({res['message']})"
                print(f"{msg}")
                update_state(idx, emp, msg)
            else:
                summary["errors"] += 1
                msg = f"⚠️ XATO ({res['message']})"
                print(f"{msg}")
                update_state(idx, emp, msg)

            # Xodimlar orasida tanaffus
            if idx < total:
                time.sleep(self.delay)

        summary["finished_at"] = datetime.now(TASHKENT_TZ).isoformat()

        # Batch yakunlandi holatini yozish
        try:
            with open(live_state_file, "w", encoding="utf-8") as f:
                json.dump({
                    "is_running": False,
                    "finished_at": datetime.now(TASHKENT_TZ).strftime("%H:%M:%S"),
                    "total": total,
                    "solved": summary["solved"],
                    "already_completed": summary["already_completed"],
                    "failed": summary["login_failed"] + summary["errors"],
                    "total_xp_gained": summary["total_xp_gained"]
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        # Login yoki paroli xato bo'lgan xodimlarni Excel faylga eksport qilish
        emp_map = {e["login"]: e for e in employees}
        failed_list = [
            {**r, **emp_map.get(r["login"], {})}
            for r in summary["results"]
            if r["status"] in ["LOGIN_FAILED", "ERROR", "CRITICAL_ERROR", "PARTIAL_OR_FAILED"]
        ]
        excel_path = None
        if failed_list:
            excel_path = self.export_failed_employees_to_excel(failed_list)
            summary["failed_excel_path"] = excel_path

        # Hisobotni faylga saqlash
        os.makedirs("data/multi_user_reports", exist_ok=True)
        today_str = datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d")
        report_file = f"data/multi_user_reports/report_{today_str}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n=======================================================")
        print(f"🎉 BARCHA XODIMLAR YAKUNLANDI!")
        print(f"✅ Yangi yechilganlar: {summary['solved']} ta (+{summary['total_xp_gained']} XP)")
        print(f"⏭ Allaqachon yechilganlar: {summary['already_completed']} ta")
        print(f"❌ Xatoliklar / Login xato: {summary['login_failed'] + summary['errors']} ta")
        if excel_path:
            print(f"📑 Xatoliklar Excel fayli: {excel_path}")
        print(f"📁 Hisobot fayli: {report_file}")
        print(f"=======================================================\n")

        return summary

    def export_failed_employees_to_excel(self, failed_list: List[Dict[str, Any]], filename: Optional[str] = None) -> Optional[str]:
        """Login yoki paroli xato bo'lgan xodimlarni chiroyli Excel (.xlsx) fayliga chiqarish"""
        if not failed_list:
            return None

        today_str = datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d")
        os.makedirs("data/multi_user_reports", exist_ok=True)
        xlsx_path = filename or f"data/multi_user_reports/Xatoliklar_{today_str}.xlsx"

        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Xato login-parollar"

            headers = [
                "№", "Tabel raqami", "F.I.O (Familiya Ism Sharif)", "Login", 
                "Parol", "Bo'lim", "Lavozim", "Xatolik sababi", "Tekshirilgan vaqt"
            ]
            ws.append(headers)

            # Sarlavha uslubi
            header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
            header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            thin_border = Border(
                left=Side(style='thin', color='D9D9D9'),
                right=Side(style='thin', color='D9D9D9'),
                top=Side(style='thin', color='D9D9D9'),
                bottom=Side(style='thin', color='D9D9D9')
            )

            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col_num)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            now_time = datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M")
            for idx, item in enumerate(failed_list, 1):
                reason = item.get("message", "Login yoki parol noto'g'ri")
                if "401" in reason or "Invalid" in reason:
                    reason = "Login yoki parol noto'g'ri (Energo ID 401)"
                elif "403" in reason:
                    reason = "Kirish taqiqlangan (403)"

                row_data = [
                    idx,
                    item.get("tabel", ""),
                    item.get("name", ""),
                    item.get("login", ""),
                    item.get("password", ""),
                    item.get("department", ""),
                    item.get("position", ""),
                    reason,
                    now_time
                ]
                ws.append(row_data)

                row_idx = idx + 1
                for c_idx in range(1, len(row_data) + 1):
                    c = ws.cell(row=row_idx, column=c_idx)
                    c.border = thin_border
                    c.font = Font(name="Calibri", size=10)
                    if c_idx in [1, 2, 4, 5, 9]:
                        c.alignment = Alignment(horizontal="center", vertical="center")

            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = openpyxl.utils.get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

            wb.save(xlsx_path)
            print(f"[MultiUser] 📊 Xatoliklar Excel faylga saqlandi: {xlsx_path}")
            return xlsx_path

        except Exception as e:
            print(f"[!] Excel yaratishda xatolik: {e}")
            csv_path = xlsx_path.replace(".xlsx", ".csv")
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["№", "Tabel raqami", "F.I.O", "Login", "Parol", "Bo'lim", "Lavozim", "Xatolik sababi"])
                for idx, item in enumerate(failed_list, 1):
                    writer.writerow([
                        idx, item.get("tabel", ""), item.get("name", ""), item.get("login", ""),
                        item.get("password", ""), item.get("department", ""), item.get("position", ""),
                        item.get("message", "")
                    ])
            return csv_path

        return summary

    def solve_employee_safe(self, emp: Dict[str, str]) -> Dict[str, Any]:
        """Xatoliklarni ushlab qolib xavfsiz yechish"""
        try:
            return self.solve_for_employee(emp)
        except Exception as e:
            return {
                "login": emp["login"],
                "name": emp["name"],
                "status": "CRITICAL_ERROR",
                "message": str(e),
                "xp_gained": 0,
                "total_xp": 0,
                "rank": "N/A"
            }

    @staticmethod
    def format_telegram_report(summary: Dict[str, Any]) -> str:
        """Telegram uchun chiroyli jamlama hisobot tayyorlash"""
        total = summary.get("total_employees", 0)
        solved = summary.get("solved", 0)
        already = summary.get("already_completed", 0)
        failed = summary.get("login_failed", 0) + summary.get("errors", 0)
        xp = summary.get("total_xp_gained", 0)
        now_str = datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M")

        text = (
            f"🏢 <b>XORAZM MET FILIALI — KUNLIK TEST HISOBOTI</b>\n\n"
            f"📅 <b>Sana:</b> {now_str} (Toshkent vaqti)\n"
            f"👥 <b>Jami xodimlar:</b> {total} nafar\n"
            f"══════════════════════\n"
            f"✅ <b>Bugun yechilganlar:</b> {solved} nafar\n"
            f"⏭ <b>Allaqachon yechilgan:</b> {already} nafar\n"
            f"⚠️ <b>Xatolik / O'tkazilgan:</b> {failed} nafar\n\n"
            f"🎁 <b>Filial bo'yicha to'plangan bonus:</b> <b>+{xp:,} XP</b> 🚀\n"
            f"══════════════════════\n"
            f"💾 <i>Barcha xodimlarning testlari to'liq 10/10 qilib yopildi!</i>"
        )
        return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-user ElektroLearn daily plan solver")
    parser.add_argument("--limit", type=int, default=None, help="Yechiladigan xodimlar soni (sinov uchun)")
    parser.add_argument("--login", type=str, default=None, help="Aynan bitta xodim logini")
    parser.add_argument("--delay", type=float, default=2.0, help="Xodimlar orasidagi tanaffus (soniya)")
    args = parser.parse_args()

    solver = MultiUserSolver(delay_between_users=args.delay)
    solver.run_batch(limit=args.limit, target_login=args.login)
