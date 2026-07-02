import tkinter as tk
from tkinter import messagebox, font
import json, os, calendar
from datetime import date, datetime

# ── persistence ───────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.expanduser("~"), ".calendar_reminders.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── palette ───────────────────────────────────────────────────────────────────
BG_DARK     = "#0F0E17"
BG_CARD     = "#1A1830"
BG_CELL     = "#1E1D2E"
BG_CELL_HOV = "#252440"
BG_PANEL    = "#161526"
BORDER      = "#2E2C4A"
BORDER_SEL  = "#A78BFA"

TEXT_PRI    = "#F0EEFF"
TEXT_SEC    = "#9B99B8"
TEXT_DIM    = "#4E4C6A"

ACC_VIOLET  = "#A78BFA"
ACC_PINK    = "#F472B6"
ACC_CYAN    = "#22D3EE"
ACC_AMBER   = "#FBBF24"
ACC_GREEN   = "#34D399"
ACC_RED     = "#F87171"

TODAY_BG    = "#A78BFA"
TODAY_FG    = "#0F0E17"

HIGH_BG, HIGH_FG   = "#3D1A1A", "#F87171"
MED_BG,  MED_FG    = "#3A2D00", "#FBBF24"
LOW_BG,  LOW_FG    = "#0D2E20", "#34D399"
DOT_BG,  DOT_FG    = "#1C1A3A", "#A78BFA"

PRIORITY_META = {
    "High":   (HIGH_BG, HIGH_FG,  ACC_RED),
    "Medium": (MED_BG,  MED_FG,   ACC_AMBER),
    "Low":    (LOW_BG,  LOW_FG,   ACC_GREEN),
}

MONTHS     = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
DAYS_SHORT = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

MONTH_ACCENTS = [
    ACC_VIOLET, ACC_PINK, ACC_CYAN, ACC_AMBER, ACC_GREEN, ACC_RED,
    ACC_VIOLET, ACC_PINK, ACC_CYAN, ACC_AMBER, ACC_GREEN, ACC_RED,
]


class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Calendar & Reminders")
        self.configure(bg=BG_DARK)
        self.minsize(900, 640)
        self.resizable(True, True)

        self.reminders  = load_data()
        self.today      = date.today()
        self.cur_year   = self.today.year
        self.cur_month  = self.today.month
        self.sel_date   = self.today

        self._build_fonts()
        self._build_ui()
        self._render_calendar()
        self._show_panel(self.sel_date)

    # ── fonts ─────────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_hero   = font.Font(family="Helvetica Neue", size=22, weight="bold")
        self.f_title  = font.Font(family="Helvetica Neue", size=13, weight="bold")
        self.f_head   = font.Font(family="Helvetica Neue", size=11, weight="bold")
        self.f_body   = font.Font(family="Helvetica Neue", size=11)
        self.f_small  = font.Font(family="Helvetica Neue", size=9)
        self.f_day    = font.Font(family="Helvetica Neue", size=11, weight="bold")
        self.f_dot    = font.Font(family="Helvetica Neue", size=8)
        self.f_btn    = font.Font(family="Helvetica Neue", size=10, weight="bold")
        self.f_label  = font.Font(family="Helvetica Neue", size=9,  weight="bold")

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=BG_DARK, padx=20, pady=18)
        outer.pack(fill=tk.BOTH, expand=True)

        self._build_header(outer)

        split = tk.Frame(outer, bg=BG_DARK)
        split.pack(fill=tk.BOTH, expand=True)

        # left – calendar
        left = tk.Frame(split, bg=BG_DARK)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 14))

        hdr = tk.Frame(left, bg=BG_DARK)
        hdr.pack(fill=tk.X, pady=(0, 4))
        for i, d in enumerate(DAYS_SHORT):
            col = ACC_VIOLET if i < 5 else ACC_PINK
            tk.Label(hdr, text=d, font=self.f_label, bg=BG_DARK, fg=col,
                     anchor="center").pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.grid_frame = tk.Frame(left, bg=BG_DARK)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        # right – panel
        right = tk.Frame(split, bg=BG_PANEL, width=272,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)
        self._build_panel(right)

    def _build_header(self, parent):
        bar = tk.Frame(parent, bg=BG_DARK)
        bar.pack(fill=tk.X, pady=(0, 16))

        dot_c = tk.Canvas(bar, width=14, height=14, bg=BG_DARK, highlightthickness=0)
        dot_c.create_oval(2, 2, 12, 12, fill=ACC_VIOLET, outline="")
        dot_c.pack(side=tk.LEFT, padx=(0, 8), pady=6)

        self.lbl_month = tk.Label(bar, text="", font=self.f_hero,
                                  bg=BG_DARK, fg=TEXT_PRI)
        self.lbl_month.pack(side=tk.LEFT)

        self.accent_line = tk.Canvas(bar, height=3, bg=BG_DARK, highlightthickness=0)
        self.accent_line.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=16, pady=10)

        btn_frame = tk.Frame(bar, bg=BG_DARK)
        btn_frame.pack(side=tk.RIGHT)

        for txt, cmd, acc in [("Today", self._go_today, ACC_CYAN),
                               ("◀",    lambda: self._change_month(-1), ACC_VIOLET),
                               ("▶",    lambda: self._change_month(1),  ACC_VIOLET)]:
            b = tk.Button(btn_frame, text=txt, font=self.f_btn,
                          bg=BG_CARD, fg=acc, relief=tk.FLAT, bd=0,
                          padx=12, pady=6, cursor="hand2", command=cmd,
                          highlightbackground=BORDER, highlightthickness=1,
                          activebackground=BG_CELL_HOV, activeforeground=acc)
            b.pack(side=tk.LEFT, padx=3)
            b.bind("<Enter>", lambda e, w=b, a=acc: w.config(bg=BG_CELL_HOV))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=BG_CARD))

        self._draw_accent_line()

    def _draw_accent_line(self):
        acc = MONTH_ACCENTS[(self.cur_month - 1) % 12]
        self.accent_line.delete("all")
        self.accent_line.update_idletasks()
        w = self.accent_line.winfo_width() or 200
        self.accent_line.create_rectangle(0, 1, w, 3, fill=acc, outline="")

    # ── panel ─────────────────────────────────────────────────────────────────
    def _build_panel(self, parent):
        inner = tk.Frame(parent, bg=BG_PANEL, padx=14, pady=14)
        inner.pack(fill=tk.BOTH, expand=True)

        self.lbl_sel_date = tk.Label(inner, text="", font=self.f_head,
                                     bg=BG_PANEL, fg=ACC_VIOLET,
                                     wraplength=230, justify=tk.LEFT)
        self.lbl_sel_date.pack(anchor="w", pady=(0, 10))

        # form card
        form_outer = tk.Frame(inner, bg=BG_CARD,
                              highlightbackground=BORDER, highlightthickness=1)
        form_outer.pack(fill=tk.X, pady=(0, 10))
        fp = tk.Frame(form_outer, bg=BG_CARD, padx=12, pady=10)
        fp.pack(fill=tk.X)

        def lbl(txt):
            tk.Label(fp, text=txt, font=self.f_label,
                     bg=BG_CARD, fg=ACC_VIOLET).pack(anchor="w", pady=(6, 2))

        def ent():
            e = tk.Entry(fp, font=self.f_body, bg=BG_CELL, fg=TEXT_PRI,
                         relief=tk.FLAT, insertbackground=ACC_VIOLET,
                         highlightbackground=BORDER, highlightthickness=1)
            e.pack(fill=tk.X)
            e.bind("<FocusIn>",  lambda ev, w=e: w.config(highlightbackground=ACC_VIOLET))
            e.bind("<FocusOut>", lambda ev, w=e: w.config(highlightbackground=BORDER))
            return e

        lbl("TITLE")
        self.ent_title = ent()
        lbl("TIME  (HH:MM)")
        self.ent_time = ent()
        lbl("NOTE")
        self.txt_note = tk.Text(fp, font=self.f_body, bg=BG_CELL, fg=TEXT_PRI,
                                height=3, relief=tk.FLAT,
                                insertbackground=ACC_VIOLET,
                                highlightbackground=BORDER, highlightthickness=1)
        self.txt_note.pack(fill=tk.X)
        self.txt_note.bind("<FocusIn>",  lambda e: self.txt_note.config(highlightbackground=ACC_VIOLET))
        self.txt_note.bind("<FocusOut>", lambda e: self.txt_note.config(highlightbackground=BORDER))

        lbl("PRIORITY")
        self.var_priority = tk.StringVar(value="Medium")
        pf = tk.Frame(fp, bg=BG_CARD)
        pf.pack(anchor="w", pady=(2, 8))
        for p, col in [("Low", ACC_GREEN), ("Medium", ACC_AMBER), ("High", ACC_RED)]:
            tk.Radiobutton(pf, text=p, variable=self.var_priority, value=p,
                           font=self.f_small, bg=BG_CARD, fg=col,
                           selectcolor=BG_CARD, activebackground=BG_CARD,
                           activeforeground=col).pack(side=tk.LEFT, padx=(0, 10))

        self.add_btn = tk.Button(fp, text="＋  Add Reminder", font=self.f_btn,
                                 bg=ACC_VIOLET, fg=BG_DARK, relief=tk.FLAT, bd=0,
                                 padx=14, pady=7, cursor="hand2",
                                 command=self._add_reminder,
                                 activebackground=ACC_PINK, activeforeground=BG_DARK)
        self.add_btn.pack(fill=tk.X, pady=(4, 0))
        self.add_btn.bind("<Enter>", lambda e: self.add_btn.config(bg=ACC_PINK))
        self.add_btn.bind("<Leave>", lambda e: self.add_btn.config(bg=ACC_VIOLET))

        # list
        tk.Frame(inner, height=1, bg=BORDER).pack(fill=tk.X, pady=(6, 8))
        tk.Label(inner, text="REMINDERS", font=self.f_label,
                 bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", pady=(0, 6))

        wrap = tk.Frame(inner, bg=BG_PANEL)
        wrap.pack(fill=tk.BOTH, expand=True)

        self.rem_canvas = tk.Canvas(wrap, bg=BG_PANEL, highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient=tk.VERTICAL, command=self.rem_canvas.yview)
        self.rem_canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.rem_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.rem_inner = tk.Frame(self.rem_canvas, bg=BG_PANEL)
        self._rem_win  = self.rem_canvas.create_window((0, 0), window=self.rem_inner, anchor="nw")
        self.rem_inner.bind("<Configure>", lambda e: self.rem_canvas.configure(
            scrollregion=self.rem_canvas.bbox("all")))
        self.rem_canvas.bind("<Configure>", lambda e: self.rem_canvas.itemconfig(
            self._rem_win, width=e.width))

    # ── calendar rendering ────────────────────────────────────────────────────
    def _render_calendar(self):
        self.lbl_month.config(text=f"{MONTHS[self.cur_month-1]}  {self.cur_year}")
        self._draw_accent_line()

        for w in self.grid_frame.winfo_children():
            w.destroy()

        accent = MONTH_ACCENTS[(self.cur_month - 1) % 12]
        for week in calendar.monthcalendar(self.cur_year, self.cur_month):
            row = tk.Frame(self.grid_frame, bg=BG_DARK)
            row.pack(fill=tk.X, expand=True, pady=2)
            for col_i, day in enumerate(week):
                self._make_cell(row, col_i, day, accent)

    def _make_cell(self, parent, col_i, day, accent):
        is_other  = (day == 0)
        is_today  = (not is_other and day == self.today.day and
                     self.cur_month == self.today.month and
                     self.cur_year  == self.today.year)
        cell_date = date(self.cur_year, self.cur_month, day) if not is_other else None
        is_sel    = (cell_date == self.sel_date)

        bg    = BG_CELL if not is_other else BG_DARK
        b_col = BORDER_SEL if is_sel else (BORDER if not is_other else BG_DARK)
        b_w   = 2 if is_sel else 1

        cell = tk.Frame(parent, bg=bg,
                        highlightbackground=b_col, highlightthickness=b_w,
                        cursor="hand2" if not is_other else "arrow")
        cell.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, ipadx=4, ipady=4)

        # day number
        num_txt = str(day) if not is_other else ""
        if is_today:
            c = tk.Canvas(cell, width=26, height=26, bg=bg, highlightthickness=0)
            c.create_oval(1, 1, 25, 25, fill=TODAY_BG, outline="")
            c.create_text(13, 13, text=num_txt, font=self.f_day, fill=TODAY_FG)
            c.pack(anchor="ne", padx=4, pady=(4, 2))
        else:
            fg_n = (accent if is_sel else
                    (ACC_PINK if col_i >= 5 else TEXT_PRI) if not is_other else TEXT_DIM)
            tk.Label(cell, text=num_txt, font=self.f_day,
                     bg=bg, fg=fg_n).pack(anchor="ne", padx=4, pady=(4, 2))

        # reminder dots
        if cell_date:
            rems = self.reminders.get(cell_date.strftime("%Y-%m-%d"), [])
            for r in rems[:2]:
                pb, pf, _ = PRIORITY_META.get(r.get("priority","Medium"), (DOT_BG, DOT_FG, ACC_VIOLET))
                txt = (r.get("time","") + " " if r.get("time") else "") + r.get("title","")
                tk.Label(cell, text=txt[:13], font=self.f_dot,
                         bg=pb, fg=pf, anchor="w", padx=4, pady=1
                         ).pack(fill=tk.X, padx=2, pady=1)
            if len(rems) > 2:
                tk.Label(cell, text=f"+{len(rems)-2} more", font=self.f_dot,
                         bg=DOT_BG, fg=DOT_FG, anchor="w", padx=4, pady=1
                         ).pack(fill=tk.X, padx=2, pady=1)

        if not is_other:
            for w in [cell] + cell.winfo_children():
                w.bind("<Button-1>", lambda e, d=cell_date: self._on_day_click(d))
            cell.bind("<Enter>", lambda e, c=cell: c.config(bg=BG_CELL_HOV))
            cell.bind("<Leave>", lambda e, c=cell, b=bg: c.config(bg=b))

    def _on_day_click(self, d):
        self.sel_date = d
        self._render_calendar()
        self._show_panel(d)

    # ── panel refresh ─────────────────────────────────────────────────────────
    def _show_panel(self, d):
        acc = MONTH_ACCENTS[(d.month - 1) % 12]
        self.lbl_sel_date.config(text=d.strftime("%A, %d %B %Y").upper(), fg=acc)
        self._refresh_list(d)

    def _refresh_list(self, d=None):
        if d is None:
            d = self.sel_date
        for w in self.rem_inner.winfo_children():
            w.destroy()

        key  = d.strftime("%Y-%m-%d")
        rems = sorted(self.reminders.get(key, []), key=lambda r: r.get("time","99:99"))

        if not rems:
            tk.Label(self.rem_inner, text="No reminders yet.",
                     font=self.f_small, bg=BG_PANEL, fg=TEXT_DIM).pack(pady=10)
            return

        for r in rems:
            self._make_rem_row(key, r)

    def _make_rem_row(self, key, r):
        pb, pf, stripe = PRIORITY_META.get(r.get("priority","Medium"),
                                           (DOT_BG, DOT_FG, ACC_VIOLET))
        card = tk.Frame(self.rem_inner, bg=BG_CARD,
                        highlightbackground=stripe, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 6))

        tk.Frame(card, bg=stripe, width=4).pack(side=tk.LEFT, fill=tk.Y)

        body = tk.Frame(card, bg=BG_CARD, padx=8, pady=6)
        body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        trow = tk.Frame(body, bg=BG_CARD)
        trow.pack(fill=tk.X)
        tk.Label(trow, text=r.get("title",""), font=self.f_head,
                 bg=BG_CARD, fg=TEXT_PRI, anchor="w").pack(side=tk.LEFT)

        db = tk.Button(trow, text="✕", font=self.f_dot,
                       bg=BG_CARD, fg=TEXT_DIM, relief=tk.FLAT, bd=0,
                       cursor="hand2",
                       command=lambda k=key, rem=r: self._delete_reminder(k, rem),
                       activebackground=BG_CARD, activeforeground=ACC_RED)
        db.pack(side=tk.RIGHT)
        db.bind("<Enter>", lambda e, b=db: b.config(fg=ACC_RED))
        db.bind("<Leave>", lambda e, b=db: b.config(fg=TEXT_DIM))

        meta = tk.Frame(body, bg=BG_CARD)
        meta.pack(fill=tk.X, pady=(2, 0))
        tk.Label(meta, text=r.get("time","") or "—",
                 font=self.f_small, bg=BG_CARD, fg=ACC_CYAN).pack(side=tk.LEFT)
        tk.Label(meta, text=r.get("priority",""), font=self.f_dot,
                 bg=pb, fg=pf, padx=6, pady=2).pack(side=tk.RIGHT)

        if r.get("note"):
            tk.Label(body, text=r["note"], font=self.f_small,
                     bg=BG_CARD, fg=TEXT_SEC, anchor="w",
                     wraplength=200, justify=tk.LEFT).pack(anchor="w", pady=(3, 0))

    # ── actions ───────────────────────────────────────────────────────────────
    def _add_reminder(self):
        title = self.ent_title.get().strip()
        if not title:
            self.ent_title.config(highlightbackground=ACC_RED, highlightthickness=2)
            self.after(1200, lambda: self.ent_title.config(
                highlightbackground=BORDER, highlightthickness=1))
            return

        time_val = self.ent_time.get().strip()
        if time_val:
            try:
                datetime.strptime(time_val, "%H:%M")
            except ValueError:
                messagebox.showerror("Invalid Time", "Use HH:MM format, e.g. 09:30")
                return

        key = self.sel_date.strftime("%Y-%m-%d")
        self.reminders.setdefault(key, []).append({
            "title":    title,
            "time":     time_val,
            "note":     self.txt_note.get("1.0", tk.END).strip(),
            "priority": self.var_priority.get(),
        })
        save_data(self.reminders)

        self.ent_title.delete(0, tk.END)
        self.ent_time.delete(0, tk.END)
        self.txt_note.delete("1.0", tk.END)
        self.var_priority.set("Medium")

        self._render_calendar()
        self._refresh_list()

    def _delete_reminder(self, key, reminder):
        if messagebox.askyesno("Delete", f"Delete '{reminder.get('title')}'?"):
            self.reminders[key] = [r for r in self.reminders[key] if r is not reminder]
            if not self.reminders[key]:
                del self.reminders[key]
            save_data(self.reminders)
            self._render_calendar()
            self._refresh_list()

    def _change_month(self, delta):
        m, y = self.cur_month + delta, self.cur_year
        if m > 12: m, y = 1,  y + 1
        if m < 1:  m, y = 12, y - 1
        self.cur_month, self.cur_year = m, y
        self._render_calendar()

    def _go_today(self):
        self.cur_year, self.cur_month = self.today.year, self.today.month
        self.sel_date = self.today
        self._render_calendar()
        self._show_panel(self.today)


if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()
