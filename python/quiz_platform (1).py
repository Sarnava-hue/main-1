import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os, time, random, datetime, math


# ─────────────────────────── THEME ──────────────────────────────────────────
BG        = "#0b0c10"
SURFACE   = "#13141a"
CARD      = "#1c1e28"
CARD2     = "#22253a"
BORDER    = "#2e3250"

NEON      = "#00e5ff"      
NEON2     = "#ff6b9d"      
GOLD      = "#ffd166"      
GREEN     = "#06d6a0"      
RED       = "#ef476f"      
PURPLE    = "#9b5de5"      
TEXT      = "#e8eaf6"
SUBTEXT   = "#6b7094"
MUTED     = "#3d4166"

F_HERO    = ("Trebuchet MS", 42, "bold")
F_TITLE   = ("Trebuchet MS", 18, "bold")
F_SECTION = ("Trebuchet MS", 13, "bold")
F_BODY    = ("Trebuchet MS", 11)
F_SMALL   = ("Trebuchet MS", 9)
F_MONO    = ("Courier New",  10)
F_SCORE   = ("Courier New",  28, "bold")
F_BTN     = ("Trebuchet MS", 11, "bold")
F_OPTION  = ("Trebuchet MS", 12)

DATA_FILE = os.path.join(os.path.dirname(__file__), "quizforge_data.json")


# ─────────────────────────── DATA LAYER ─────────────────────────────────────
BUILTIN_QUIZZES = [
    {
        "id": "sci_basics",
        "title": "Science Basics",
        "category": "Science",
        "description": "Fundamental science questions covering physics, chemistry & biology.",
        "time_per_q": 30,
        "questions": [
            {"q": "What is the chemical symbol for Gold?",
             "options": ["Au", "Ag", "Fe", "Gd"], "answer": 0,
             "explanation": "Au comes from the Latin 'Aurum'."},
            {"q": "Which planet is known as the Red Planet?",
             "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": 1,
             "explanation": "Mars appears red due to iron oxide on its surface."},
            {"q": "What is the speed of light in a vacuum?",
             "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "1,080,000 km/h"], "answer": 0,
             "explanation": "Light travels at ~299,792 km/s in a vacuum."},
            {"q": "What gas do plants absorb during photosynthesis?",
             "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2,
             "explanation": "Plants absorb CO₂ and release O₂ during photosynthesis."},
            {"q": "What is the powerhouse of the cell?",
             "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi Apparatus"], "answer": 2,
             "explanation": "Mitochondria produce ATP — the cell's energy currency."},
            {"q": "What is the atomic number of Carbon?",
             "options": ["6", "12", "14", "8"], "answer": 0,
             "explanation": "Carbon has 6 protons, giving it atomic number 6."},
            {"q": "Which law states F = ma?",
             "options": ["Newton's 1st Law", "Newton's 2nd Law", "Newton's 3rd Law", "Hooke's Law"], "answer": 1,
             "explanation": "Newton's Second Law relates force, mass and acceleration."},
            {"q": "What is the most abundant gas in Earth's atmosphere?",
             "options": ["Oxygen", "Carbon Dioxide", "Argon", "Nitrogen"], "answer": 3,
             "explanation": "Nitrogen makes up ~78% of Earth's atmosphere."},
        ]
    },
    {
        "id": "world_geo",
        "title": "World Geography",
        "category": "Geography",
        "description": "Test your knowledge of capitals, countries and landmarks.",
        "time_per_q": 25,
        "questions": [
            {"q": "What is the capital of Australia?",
             "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "answer": 2,
             "explanation": "Canberra has been Australia's capital since 1927."},
            {"q": "Which is the longest river in the world?",
             "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": 1,
             "explanation": "The Nile stretches ~6,650 km through northeast Africa."},
            {"q": "Which country has the most natural lakes?",
             "options": ["Russia", "USA", "Brazil", "Canada"], "answer": 3,
             "explanation": "Canada contains over 60% of the world's freshwater lakes."},
            {"q": "Mount Everest is located in which mountain range?",
             "options": ["Andes", "Alps", "Himalayas", "Rockies"], "answer": 2,
             "explanation": "Everest sits on the Nepal–Tibet border in the Himalayas."},
            {"q": "What is the smallest country in the world?",
             "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"], "answer": 2,
             "explanation": "Vatican City covers just 0.44 km²."},
            {"q": "Which ocean is the largest?",
             "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": 3,
             "explanation": "The Pacific Ocean covers more than 165 million km²."},
        ]
    },
    {
        "id": "pop_culture",
        "title": "Pop Culture Blast",
        "category": "Entertainment",
        "description": "Movies, music and internet trends — how tuned in are you?",
        "time_per_q": 20,
        "questions": [
            {"q": "Which film won the first ever Academy Award for Best Picture?",
             "options": ["Wings", "Sunrise", "The Jazz Singer", "Chang"], "answer": 0,
             "explanation": "'Wings' (1927) won the first Best Picture Oscar."},
            {"q": "How many strings does a standard guitar have?",
             "options": ["4", "5", "6", "7"], "answer": 2,
             "explanation": "A standard guitar has 6 strings tuned E-A-D-G-B-e."},
            {"q": "Which streaming service produced 'Stranger Things'?",
             "options": ["HBO", "Amazon Prime", "Netflix", "Disney+"], "answer": 2,
             "explanation": "Stranger Things premiered on Netflix in July 2016."},
            {"q": "What does 'GIF' stand for?",
             "options": ["Graphical Image Format", "Graphics Interchange Format",
                         "General Image File", "Global Image Frame"], "answer": 1,
             "explanation": "GIF = Graphics Interchange Format, created in 1987."},
            {"q": "Which video game franchise features the character Master Chief?",
             "options": ["Call of Duty", "Halo", "Destiny", "Titanfall"], "answer": 1,
             "explanation": "Master Chief (John-117) is the iconic hero of Halo."},
        ]
    },
    {
        "id": "math_blitz",
        "title": "Math Blitz",
        "category": "Mathematics",
        "description": "Quick-fire arithmetic and logic. No calculators!",
        "time_per_q": 20,
        "questions": [
            {"q": "What is 17 × 13?",
             "options": ["201", "221", "211", "231"], "answer": 1,
             "explanation": "17 × 13 = 17 × 10 + 17 × 3 = 170 + 51 = 221."},
            {"q": "What is the square root of 144?",
             "options": ["11", "12", "13", "14"], "answer": 1,
             "explanation": "12 × 12 = 144."},
            {"q": "How many degrees are in a right angle?",
             "options": ["45°", "180°", "90°", "360°"], "answer": 2,
             "explanation": "A right angle is exactly 90 degrees."},
            {"q": "What is the next prime number after 13?",
             "options": ["15", "17", "16", "19"], "answer": 1,
             "explanation": "14, 15, 16 are not prime. 17 is the next prime after 13."},
            {"q": "If a triangle has angles 60° and 80°, what is the third angle?",
             "options": ["30°", "40°", "50°", "60°"], "answer": 1,
             "explanation": "Angles sum to 180°: 180 - 60 - 80 = 40°."},
            {"q": "What is 2⁸?",
             "options": ["128", "256", "512", "64"], "answer": 1,
             "explanation": "2⁸ = 256."},
            {"q": "What is 15% of 200?",
             "options": ["25", "30", "35", "40"], "answer": 1,
             "explanation": "15% of 200 = 0.15 × 200 = 30."},
        ]
    },
]

CAT_COLORS = {
    "Science":       "#00e5ff",
    "Geography":     "#06d6a0",
    "Entertainment": "#ff6b9d",
    "Mathematics":   "#ffd166",
    "History":       "#9b5de5",
    "Technology":    "#4cc9f0",
    "Custom":        "#f8961e",
}

def cat_color(cat):
    return CAT_COLORS.get(cat, PURPLE)


# ─────────────────────────── PERSISTENCE ────────────────────────────────────
def load_data():
    default = {"custom_quizzes": [], "scores": [], "username": "Player"}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                d = json.load(f)
                for k, v in default.items():
                    d.setdefault(k, v)
                return d
        except Exception:
            pass
    return default

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────── HELPERS ────────────────────────────────────────
def all_quizzes(data):
    return BUILTIN_QUIZZES + data.get("custom_quizzes", [])

def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r, x2,y2,
           x2-r,y2, x1+r,y2, x1,y2, x1,y2-r, x1,y1+r, x1,y1]
    return canvas.create_polygon(pts, smooth=True, **kw)


# ═══════════════════════════ MAIN APP ═══════════════════════════════════════
class QuizForge(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QuizForge")
        self.configure(bg=BG)
        self.geometry("960x680")
        self.resizable(True, True)
        self.minsize(800, 580)

        
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Vertical.TScrollbar",
                        background=SURFACE, troughcolor=BG,
                        bordercolor=BG, arrowcolor=SUBTEXT, relief="flat")
        style.configure("TCombobox",
                        fieldbackground=CARD, background=CARD,
                        foreground=TEXT, selectbackground=PURPLE,
                        selectforeground=TEXT, bordercolor=BORDER,
                        arrowcolor=NEON, relief="flat")

        self.data = load_data()
        self._active_frame = None
        self._quiz_state   = {}

        self._build_shell()
        self.show_home()

    # ── Shell layout ─────────────────────────────────────────────────────────
    def _build_shell(self):
        
        self.nav = tk.Frame(self, bg=SURFACE, width=200)
        self.nav.pack(side="left", fill="y")
        self.nav.pack_propagate(False)

        
        logo_f = tk.Frame(self.nav, bg=SURFACE)
        logo_f.pack(fill="x", pady=(24, 8), padx=16)
        tk.Label(logo_f, text="⬡", font=("Trebuchet MS", 28, "bold"),
                 bg=SURFACE, fg=NEON).pack(side="left")
        tk.Label(logo_f, text="QuizForge", font=("Trebuchet MS", 15, "bold"),
                 bg=SURFACE, fg=TEXT).pack(side="left", padx=6)

        tk.Frame(self.nav, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        
        self._nav_btns = {}
        nav_items = [
            ("🏠", "Home",       self.show_home),
            ("📚", "Quizzes",    self.show_quiz_list),
            ("✏️",  "Create",    self.show_create),
            ("🏆", "Leaderboard",self.show_leaderboard),
        ]
        for icon, label, cmd in nav_items:
            btn = self._nav_btn(self.nav, icon, label, cmd)
            self._nav_btns[label] = btn

        
        tk.Frame(self.nav, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0,8), side="bottom")
        user_f = tk.Frame(self.nav, bg=SURFACE)
        user_f.pack(side="bottom", fill="x", padx=16, pady=8)
        self._user_lbl = tk.Label(user_f,
            text=f"👤  {self.data['username']}",
            font=F_SMALL, bg=SURFACE, fg=SUBTEXT, cursor="hand2")
        self._user_lbl.pack(anchor="w")
        self._user_lbl.bind("<Button-1>", self._change_username)

        
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _nav_btn(self, parent, icon, label, cmd):
        f = tk.Frame(parent, bg=SURFACE, cursor="hand2")
        f.pack(fill="x", padx=10, pady=2)
        ico = tk.Label(f, text=icon, font=("Trebuchet MS", 13),
                       bg=SURFACE, fg=SUBTEXT, padx=8)
        ico.pack(side="left")
        lbl = tk.Label(f, text=label, font=F_BODY, bg=SURFACE, fg=SUBTEXT)
        lbl.pack(side="left")

        def on_enter(e, fr=f):
            if fr.cget("bg") != CARD2:
                fr.config(bg=CARD); ico.config(bg=CARD); lbl.config(bg=CARD)
        def on_leave(e, fr=f):
            if fr.cget("bg") != CARD2:
                fr.config(bg=SURFACE); ico.config(bg=SURFACE); lbl.config(bg=SURFACE)

        def click(e=None, fr=f, ic=ico, lb=lbl, c=cmd, la=label):
            for n, b in self._nav_btns.items():
                b[0].config(bg=SURFACE); b[1].config(bg=SURFACE, fg=SUBTEXT)
                b[2].config(bg=SURFACE)
            fr.config(bg=CARD2); ic.config(bg=CARD2, fg=NEON)
            lb.config(bg=CARD2, fg=TEXT)
            c()

        for w in (f, ico, lbl):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", click)

        return (f, lbl, ico)

    def _set_active_nav(self, name):
        for n, (f, lb, ic) in self._nav_btns.items():
            if n == name:
                f.config(bg=CARD2); ic.config(bg=CARD2, fg=NEON); lb.config(bg=CARD2, fg=TEXT)
            else:
                f.config(bg=SURFACE); ic.config(bg=SURFACE, fg=SUBTEXT); lb.config(bg=SURFACE, fg=SUBTEXT)

    def _switch(self, frame_fn):
        if self._active_frame:
            self._active_frame.destroy()
        self._active_frame = tk.Frame(self.content, bg=BG)
        self._active_frame.pack(fill="both", expand=True)
        frame_fn(self._active_frame)

    # ── Scrollable wrapper ───────────────────────────────────────────────────
    def _scrollable(self, parent):
        canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        return inner

    # ══════════════════════════ HOME ════════════════════════════════════════
    def show_home(self):
        self._set_active_nav("Home")
        self._switch(self._build_home)

    def _build_home(self, parent):
        inner = self._scrollable(parent)

        
        hero = tk.Frame(inner, bg=CARD, padx=40, pady=36)
        hero.pack(fill="x", padx=24, pady=(24, 0))
        tk.Label(hero, text=f"Welcome back,",
                 font=F_SECTION, bg=CARD, fg=SUBTEXT).pack(anchor="w")
        tk.Label(hero, text=self.data["username"],
                 font=F_HERO, bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Label(hero, text="Ready to challenge your mind?",
                 font=F_BODY, bg=CARD, fg=SUBTEXT).pack(anchor="w", pady=(4, 16))
        tk.Button(hero, text="  START PLAYING  ", font=F_BTN,
                  bg=NEON, fg=BG, relief="flat", cursor="hand2",
                  padx=20, pady=10,
                  command=self.show_quiz_list).pack(anchor="w")

        
        stats_row = tk.Frame(inner, bg=BG)
        stats_row.pack(fill="x", padx=24, pady=12)
        scores = self.data.get("scores", [])
        total   = len(scores)
        avg_pct = int(sum(s["pct"] for s in scores) / total) if total else 0
        best    = max((s["pct"] for s in scores), default=0)
        for val, lbl, col in [
            (str(total),      "Quizzes Taken", NEON),
            (f"{avg_pct}%",   "Average Score", GOLD),
            (f"{best}%",      "Best Score",    GREEN),
            (str(len(all_quizzes(self.data))), "Available Quizzes", NEON2),
        ]:
            card = tk.Frame(stats_row, bg=CARD, padx=20, pady=16)
            card.pack(side="left", fill="x", expand=True, padx=5)
            tk.Label(card, text=val, font=F_SCORE, bg=CARD, fg=col).pack()
            tk.Label(card, text=lbl, font=F_SMALL, bg=CARD, fg=SUBTEXT).pack()

        
        tk.Label(inner, text="Recent Activity", font=F_SECTION,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(12, 4))
        recent = scores[-5:][::-1]
        if not recent:
            tk.Label(inner, text="No quizzes completed yet. Go play one!",
                     font=F_BODY, bg=BG, fg=SUBTEXT).pack(padx=28, pady=4)
        else:
            for s in recent:
                row = tk.Frame(inner, bg=CARD, padx=16, pady=10)
                row.pack(fill="x", padx=24, pady=3)
                col = GREEN if s["pct"] >= 70 else (GOLD if s["pct"] >= 40 else RED)
                tk.Label(row, text=s["quiz"], font=F_BODY, bg=CARD, fg=TEXT).pack(side="left")
                tk.Label(row, text=f"{s['score']}/{s['total']}  ({s['pct']}%)",
                         font=F_MONO, bg=CARD, fg=col).pack(side="right")
                tk.Label(row, text=s.get("date", ""), font=F_SMALL,
                         bg=CARD, fg=SUBTEXT).pack(side="right", padx=16)

        
        tk.Label(inner, text="Featured Quizzes", font=F_SECTION,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(16, 4))
        featured_row = tk.Frame(inner, bg=BG)
        featured_row.pack(fill="x", padx=20, pady=(0, 24))
        for q in all_quizzes(self.data)[:4]:
            self._quiz_card(featured_row, q, compact=True).pack(
                side="left", fill="x", expand=True, padx=6)

    # ══════════════════════════ QUIZ LIST ════════════════════════════════════
    def show_quiz_list(self):
        self._set_active_nav("Quizzes")
        self._switch(self._build_quiz_list)

    def _build_quiz_list(self, parent):
        
        hdr = tk.Frame(parent, bg=SURFACE, padx=24, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="All Quizzes", font=F_TITLE, bg=SURFACE, fg=TEXT).pack(side="left")

        self._filter_var = tk.StringVar(master=self, value="All")
        cats = ["All"] + list(dict.fromkeys(
            q.get("category", "Custom") for q in all_quizzes(self.data)))
        for c in cats:
            col = cat_color(c) if c != "All" else SUBTEXT
            btn = tk.Button(hdr, text=c, font=F_SMALL, bg=CARD, fg=col,
                            relief="flat", padx=8, pady=4, cursor="hand2",
                            command=lambda cv=c: self._filter_quizzes(cv))
            btn.pack(side="right", padx=3)

        inner = self._scrollable(parent)
        self._qlist_inner = inner
        self._render_quiz_list(inner, "All")

    def _filter_quizzes(self, cat):
        for w in self._qlist_inner.winfo_children():
            w.destroy()
        self._render_quiz_list(self._qlist_inner, cat)

    def _render_quiz_list(self, parent, cat_filter):
        quizzes = all_quizzes(self.data)
        if cat_filter != "All":
            quizzes = [q for q in quizzes if q.get("category", "Custom") == cat_filter]
        grid = tk.Frame(parent, bg=BG)
        grid.pack(fill="both", padx=20, pady=16)
        for i, q in enumerate(quizzes):
            card = self._quiz_card(grid, q, compact=False)
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    def _quiz_card(self, parent, quiz, compact=False):
        cat   = quiz.get("category", "Custom")
        color = cat_color(cat)
        card  = tk.Frame(parent, bg=CARD, cursor="hand2",
                         highlightbackground=BORDER, highlightthickness=1)

        top = tk.Frame(card, bg=CARD, padx=16 if not compact else 12,
                       pady=12 if not compact else 8)
        top.pack(fill="x")

        
        badge = tk.Label(top, text=f" {cat} ", font=F_SMALL,
                         bg=color, fg=BG, padx=4)
        badge.pack(anchor="w")

        tk.Label(top, text=quiz["title"],
                 font=F_SECTION if not compact else F_BODY,
                 bg=CARD, fg=TEXT, wraplength=200).pack(anchor="w", pady=(4,2))
        if not compact:
            tk.Label(top, text=quiz.get("description", ""),
                     font=F_SMALL, bg=CARD, fg=SUBTEXT,
                     wraplength=260, justify="left").pack(anchor="w")

        info_row = tk.Frame(card, bg=CARD, padx=16 if not compact else 12, pady=6)
        info_row.pack(fill="x")
        nq = len(quiz.get("questions", []))
        tpq = quiz.get("time_per_q", 30)
        tk.Label(info_row, text=f"❓ {nq} questions",
                 font=F_SMALL, bg=CARD, fg=SUBTEXT).pack(side="left")
        tk.Label(info_row, text=f"⏱ {tpq}s each",
                 font=F_SMALL, bg=CARD, fg=SUBTEXT).pack(side="left", padx=10)

        if not compact:
            tk.Button(card, text="PLAY →", font=F_BTN,
                      bg=color, fg=BG, relief="flat", cursor="hand2",
                      padx=16, pady=6,
                      command=lambda q=quiz: self.start_quiz(q)
                      ).pack(anchor="e", padx=16, pady=(0,12))

        def on_enter(e):  card.config(bg=CARD2); _recolor(CARD2)
        def on_leave(e):  card.config(bg=CARD);  _recolor(CARD)
        def _recolor(c):
            for w in card.winfo_children():
                try: w.config(bg=c)
                except: pass
                for ww in w.winfo_children():
                    try: ww.config(bg=c)
                    except: pass

        card.bind("<Button-1>", lambda e, q=quiz: self.start_quiz(q))
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        return card

    # ══════════════════════════ QUIZ ENGINE ══════════════════════════════════
    def start_quiz(self, quiz):
        self._quiz_state = {
            "quiz":      quiz,
            "questions": list(quiz["questions"]),
            "index":     0,
            "score":     0,
            "answers":   [],
            "start_time": time.time(),
        }
        random.shuffle(self._quiz_state["questions"])
        self._set_active_nav("Quizzes")
        self._switch(self._build_quiz_intro)

    def _build_quiz_intro(self, parent):
        quiz = self._quiz_state["quiz"]
        cat  = quiz.get("category", "Custom")
        color = cat_color(cat)

        center = tk.Frame(parent, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text=f" {cat} ", font=F_SMALL,
                 bg=color, fg=BG, padx=6).pack()
        tk.Label(center, text=quiz["title"], font=F_HERO,
                 bg=BG, fg=TEXT).pack(pady=(8,4))
        tk.Label(center, text=quiz.get("description",""),
                 font=F_BODY, bg=BG, fg=SUBTEXT, wraplength=420,
                 justify="center").pack()

        stats = tk.Frame(center, bg=BG)
        stats.pack(pady=20)
        nq = len(self._quiz_state["questions"])
        tpq = quiz.get("time_per_q", 30)
        for val, lbl in [(str(nq), "Questions"),
                         (f"{tpq}s", "Per Question"),
                         (f"{nq*tpq}s", "Total Time")]:
            box = tk.Frame(stats, bg=CARD, padx=20, pady=12)
            box.pack(side="left", padx=8)
            tk.Label(box, text=val, font=F_SCORE, bg=CARD, fg=color).pack()
            tk.Label(box, text=lbl, font=F_SMALL, bg=CARD, fg=SUBTEXT).pack()

        tk.Button(center, text="  BEGIN QUIZ  ", font=F_BTN,
                  bg=color, fg=BG, relief="flat", cursor="hand2",
                  padx=24, pady=12,
                  command=self._next_question).pack(pady=(12,0))
        tk.Button(center, text="← Back", font=F_SMALL,
                  bg=BG, fg=SUBTEXT, relief="flat", cursor="hand2",
                  command=self.show_quiz_list).pack(pady=4)

    def _next_question(self):
        st = self._quiz_state
        if st["index"] >= len(st["questions"]):
            self._switch(self._build_results)
            return
        self._switch(self._build_question)

    def _build_question(self, parent):
        st    = self._quiz_state
        quiz  = st["quiz"]
        qdata = st["questions"][st["index"]]
        total = len(st["questions"])
        idx   = st["index"]
        tpq   = quiz.get("time_per_q", 30)
        color = cat_color(quiz.get("category", "Custom"))

        
        prog_frame = tk.Frame(parent, bg=SURFACE, height=6)
        prog_frame.pack(fill="x")
        prog_canvas = tk.Canvas(prog_frame, bg=SURFACE, height=6,
                                highlightthickness=0)
        prog_canvas.pack(fill="x")
        def draw_progress(pct):
            prog_canvas.delete("all")
            w = prog_canvas.winfo_width() or 800
            prog_canvas.create_rectangle(0,0, int(w*pct),6, fill=color, outline="")
        parent.after(50, lambda: draw_progress((idx+1)/total))

        
        topbar = tk.Frame(parent, bg=SURFACE, padx=24, pady=10)
        topbar.pack(fill="x")
        tk.Label(topbar,
                 text=f"Question {idx+1} of {total}",
                 font=F_SECTION, bg=SURFACE, fg=TEXT).pack(side="left")

        
        self._timer_var = tk.StringVar(master=self, value=str(tpq))
        timer_lbl = tk.Label(topbar, textvariable=self._timer_var,
                             font=F_SCORE, bg=SURFACE, fg=GOLD)
        timer_lbl.pack(side="right")
        tk.Label(topbar, text="⏱", font=F_BODY,
                 bg=SURFACE, fg=SUBTEXT).pack(side="right", padx=4)

        
        tk.Label(topbar,
                 text=f"Score: {st['score']}/{idx}",
                 font=F_BODY, bg=SURFACE, fg=SUBTEXT).pack(side="right", padx=20)

        
        q_frame = tk.Frame(parent, bg=BG, padx=48, pady=24)
        q_frame.pack(fill="both", expand=True)

        tk.Label(q_frame, text=qdata["q"],
                 font=("Trebuchet MS", 17, "bold"),
                 bg=BG, fg=TEXT, wraplength=700,
                 justify="center").pack(pady=(20, 32))

        
        opts_frame = tk.Frame(q_frame, bg=BG)
        opts_frame.pack(fill="x")
        self._answered = False
        opt_btns = []
        letters  = ["A", "B", "C", "D"]

        def select(chosen_idx, btns=opt_btns):
            if self._answered:
                return
            self._answered = True
            self._timer_running = False
            correct = qdata["answer"]
            is_correct = chosen_idx == correct

            if is_correct:
                st["score"] += 1
            st["answers"].append({
                "q":        qdata["q"],
                "chosen":   chosen_idx,
                "correct":  correct,
                "correct_b": is_correct,
            })

            for i, btn in enumerate(btns):
                if i == correct:
                    btn.config(bg=GREEN, fg=BG,
                               highlightbackground=GREEN)
                elif i == chosen_idx and not is_correct:
                    btn.config(bg=RED, fg=TEXT,
                               highlightbackground=RED)
                else:
                    btn.config(fg=MUTED)

            
            if qdata.get("explanation"):
                tk.Label(q_frame,
                         text=f"💡 {qdata['explanation']}",
                         font=F_SMALL, bg=CARD, fg=SUBTEXT,
                         wraplength=620, justify="left",
                         padx=12, pady=8).pack(fill="x", pady=(16,0))

            
            result_text = "✓  Correct!" if is_correct else "✗  Incorrect"
            result_col  = GREEN if is_correct else RED
            tk.Label(q_frame, text=result_text,
                     font=("Trebuchet MS", 14, "bold"),
                     bg=BG, fg=result_col).pack(pady=8)

            
            parent.after(1800, self._advance_question)

        for i, opt in enumerate(qdata["options"]):
            row = tk.Frame(opts_frame, bg=BG)
            row.pack(fill="x", pady=4)
            btn = tk.Button(row,
                text=f"  {letters[i]}   {opt}",
                font=F_OPTION, bg=CARD, fg=TEXT,
                relief="flat", anchor="w", cursor="hand2",
                padx=16, pady=12,
                highlightbackground=BORDER, highlightthickness=1,
                activebackground=CARD2, activeforeground=TEXT,
                command=lambda ci=i: select(ci))
            btn.pack(fill="x")
            opt_btns.append(btn)

            def hover_in(e, b=btn):
                if not self._answered:
                    b.config(bg=CARD2, highlightbackground=color)
            def hover_out(e, b=btn):
                if not self._answered:
                    b.config(bg=CARD, highlightbackground=BORDER)
            btn.bind("<Enter>", hover_in)
            btn.bind("<Leave>", hover_out)

        
        self._timer_running = True
        self._time_left = tpq

        def tick():
            if not self._timer_running:
                return
            if self._time_left <= 0:
                self._timer_var.set("0")
                timer_lbl.config(fg=RED)
                if not self._answered:
                    # Time up — mark as wrong
                    st["answers"].append({
                        "q": qdata["q"], "chosen": -1,
                        "correct": qdata["answer"], "correct_b": False,
                    })
                    self._answered = True
                    for i, btn in enumerate(opt_btns):
                        if i == qdata["answer"]:
                            btn.config(bg=GREEN, fg=BG)
                        else:
                            btn.config(fg=MUTED)
                    tk.Label(q_frame, text="⏰  Time's up!",
                             font=("Trebuchet MS", 14, "bold"),
                             bg=BG, fg=RED).pack(pady=8)
                    parent.after(1800, self._advance_question)
                return
            self._time_left -= 1
            self._timer_var.set(str(self._time_left))
            if self._time_left <= 5:
                timer_lbl.config(fg=RED)
            elif self._time_left <= 10:
                timer_lbl.config(fg=NEON2)
            parent.after(1000, tick)

        parent.after(1000, tick)

    def _advance_question(self):
        self._timer_running = False
        self._quiz_state["index"] += 1
        self._next_question()

    # ══════════════════════════ RESULTS ══════════════════════════════════════
    def _build_results(self, parent):
        st    = self._quiz_state
        quiz  = st["quiz"]
        score = st["score"]
        total = len(st["questions"])
        pct   = int(score / total * 100) if total else 0
        elapsed = int(time.time() - st["start_time"])

        if pct >= 80:   grade, grade_col, msg = "A", GREEN,  "Outstanding! 🏆"
        elif pct >= 60: grade, grade_col, msg = "B", NEON,   "Well done! 🎉"
        elif pct >= 40: grade, grade_col, msg = "C", GOLD,   "Not bad! Keep practising 📚"
        else:           grade, grade_col, msg = "D", RED,    "Keep at it — you'll improve! 💪"

        
        self.data["scores"].append({
            "quiz":  quiz["title"],
            "score": score,
            "total": total,
            "pct":   pct,
            "date":  datetime.datetime.now().strftime("%d %b %Y"),
        })
        save_data(self.data)

        inner = self._scrollable(parent)

        
        hero = tk.Frame(inner, bg=CARD, padx=40, pady=30)
        hero.pack(fill="x", padx=28, pady=(28, 12))
        tk.Label(hero, text=msg, font=F_TITLE, bg=CARD, fg=TEXT).pack()
        tk.Label(hero, text=f"{score} / {total}", font=F_HERO,
                 bg=CARD, fg=grade_col).pack()
        tk.Label(hero, text=f"{pct}%  ·  Grade {grade}  ·  {elapsed}s",
                 font=F_BODY, bg=CARD, fg=SUBTEXT).pack(pady=4)

        
        btn_row = tk.Frame(inner, bg=BG)
        btn_row.pack(pady=8)
        tk.Button(btn_row, text="🔁 Play Again", font=F_BTN,
                  bg=NEON, fg=BG, relief="flat", padx=16, pady=8,
                  cursor="hand2",
                  command=lambda: self.start_quiz(quiz)).pack(side="left", padx=8)
        tk.Button(btn_row, text="📚 All Quizzes", font=F_BTN,
                  bg=CARD, fg=TEXT, relief="flat", padx=16, pady=8,
                  cursor="hand2",
                  command=self.show_quiz_list).pack(side="left", padx=8)
        tk.Button(btn_row, text="🏠 Home", font=F_BTN,
                  bg=CARD, fg=TEXT, relief="flat", padx=16, pady=8,
                  cursor="hand2",
                  command=self.show_home).pack(side="left", padx=8)

        
        tk.Label(inner, text="Answer Review", font=F_SECTION,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(16, 4))
        for i, a in enumerate(st["answers"]):
            row = tk.Frame(inner, bg=CARD, padx=16, pady=10)
            row.pack(fill="x", padx=24, pady=3)
            col = GREEN if a["correct_b"] else RED
            icon = "✓" if a["correct_b"] else "✗"
            tk.Label(row, text=f"{icon}  Q{i+1}: {a['q']}",
                     font=F_BODY, bg=CARD, fg=col,
                     wraplength=560, justify="left").pack(anchor="w")
            q_opts = st["questions"][i]["options"] if i < len(st["questions"]) else []
            if not a["correct_b"] and q_opts:
                correct_text = q_opts[a["correct"]] if a["correct"] < len(q_opts) else ""
                tk.Label(row, text=f"   Correct: {correct_text}",
                         font=F_SMALL, bg=CARD, fg=SUBTEXT).pack(anchor="w")

    # ══════════════════════════ CREATE QUIZ ══════════════════════════════════
    def show_create(self):
        self._set_active_nav("Create")
        self._switch(self._build_create)

    def _build_create(self, parent):
        self._new_questions = []

        inner = self._scrollable(parent)

        tk.Label(inner, text="Create a Quiz", font=F_TITLE,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(24, 4))
        tk.Label(inner, text="Build your own custom quiz to share and play.",
                 font=F_BODY, bg=BG, fg=SUBTEXT).pack(anchor="w", padx=28)
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)

        form = tk.Frame(inner, bg=BG, padx=28)
        form.pack(fill="x")

        def field(label, default=""):
            tk.Label(form, text=label, font=F_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
            e = tk.Entry(form, font=F_BODY, bg=CARD, fg=TEXT,
                         relief="flat", insertbackground=TEXT, highlightthickness=1,
                         highlightbackground=BORDER)
            e.pack(fill="x", ipady=5)
            e.insert(0, default)
            return e

        self._c_title = field("Quiz Title", "My Awesome Quiz")
        self._c_desc  = field("Description", "A fun quiz I created!")

        tk.Label(form, text="Category", font=F_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
        self._c_cat_var = tk.StringVar(master=self, value="Custom")
        self._c_cat = ttk.Combobox(form, textvariable=self._c_cat_var,
                                   values=list(CAT_COLORS.keys()),
                                   state="readonly", font=F_BODY)
        self._c_cat.pack(fill="x")

        tk.Label(form, text="Time per question (seconds)", font=F_SMALL,
                 bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
        self._c_time = tk.Spinbox(form, from_=10, to=120, font=F_BODY,
                                  bg=CARD, fg=TEXT, buttonbackground=CARD,
                                  relief="flat", insertbackground=TEXT)
        self._c_time.delete(0,"end"); self._c_time.insert(0,"30")
        self._c_time.pack(anchor="w")

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=14)
        tk.Label(inner, text="Questions", font=F_SECTION,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28)

        self._q_list_frame = tk.Frame(inner, bg=BG)
        self._q_list_frame.pack(fill="x", padx=24)

        self._no_q_lbl = tk.Label(self._q_list_frame,
            text="No questions yet. Add one below!",
            font=F_BODY, bg=BG, fg=SUBTEXT)
        self._no_q_lbl.pack(pady=8)

        tk.Button(inner, text="+ Add Question", font=F_BTN,
                  bg=PURPLE, fg=TEXT, relief="flat", cursor="hand2",
                  padx=16, pady=8,
                  command=self._open_add_question_dialog
                  ).pack(anchor="w", padx=24, pady=8)

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=8)
        tk.Button(inner, text="💾  SAVE QUIZ", font=F_BTN,
                  bg=NEON, fg=BG, relief="flat", cursor="hand2",
                  padx=24, pady=10,
                  command=self._save_quiz).pack(anchor="w", padx=24, pady=(0,28))

        
        custom = self.data.get("custom_quizzes", [])
        if custom:
            tk.Label(inner, text="Your Custom Quizzes", font=F_SECTION,
                     bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(8,4))
            for cq in custom:
                row = tk.Frame(inner, bg=CARD, padx=16, pady=10)
                row.pack(fill="x", padx=24, pady=3)
                tk.Label(row, text=cq["title"], font=F_BODY, bg=CARD, fg=TEXT).pack(side="left")
                tk.Label(row, text=f"{len(cq['questions'])} questions",
                         font=F_SMALL, bg=CARD, fg=SUBTEXT).pack(side="left", padx=12)
                tk.Button(row, text="▶ Play", font=F_SMALL, bg=NEON, fg=BG,
                          relief="flat", cursor="hand2", padx=8,
                          command=lambda q=cq: self.start_quiz(q)).pack(side="right")
                tk.Button(row, text="✕ Delete", font=F_SMALL, bg=CARD, fg=RED,
                          relief="flat", cursor="hand2", padx=8,
                          command=lambda q=cq: self._delete_custom_quiz(q)
                          ).pack(side="right", padx=4)

    def _refresh_q_list(self):
        for w in self._q_list_frame.winfo_children():
            w.destroy()
        if not self._new_questions:
            tk.Label(self._q_list_frame,
                     text="No questions yet. Add one below!",
                     font=F_BODY, bg=BG, fg=SUBTEXT).pack(pady=8)
            return
        for i, q in enumerate(self._new_questions):
            row = tk.Frame(self._q_list_frame, bg=CARD, padx=12, pady=8)
            row.pack(fill="x", pady=3)
            correct_opt = q["options"][q["answer"]]
            tk.Label(row, text=f"Q{i+1}: {q['q'][:60]}{'…' if len(q['q'])>60 else ''}",
                     font=F_BODY, bg=CARD, fg=TEXT).pack(anchor="w")
            tk.Label(row, text=f"✓ {correct_opt}",
                     font=F_SMALL, bg=CARD, fg=GREEN).pack(anchor="w")
            tk.Button(row, text="✕", font=F_SMALL, bg=CARD, fg=RED,
                      relief="flat", cursor="hand2",
                      command=lambda qi=i: self._remove_question(qi)).pack(side="right")

    def _remove_question(self, idx):
        self._new_questions.pop(idx)
        self._refresh_q_list()

    def _open_add_question_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Question")
        dlg.configure(bg=BG)
        dlg.geometry("520x560")
        dlg.resizable(False, False)
        dlg.grab_set()

        tk.Label(dlg, text="Add a Question", font=F_TITLE,
                 bg=BG, fg=NEON).pack(pady=(20,4))
        tk.Frame(dlg, bg=BORDER, height=1).pack(fill="x", padx=20, pady=4)

        form = tk.Frame(dlg, bg=BG, padx=24)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Question text", font=F_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
        q_entry = tk.Text(form, font=F_BODY, bg=CARD, fg=TEXT, height=3,
                          relief="flat", insertbackground=TEXT, wrap="word")
        q_entry.pack(fill="x")

        opt_entries = []
        for i, letter in enumerate(["A","B","C","D"]):
            tk.Label(form, text=f"Option {letter}", font=F_SMALL,
                     bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(6,0))
            e = tk.Entry(form, font=F_BODY, bg=CARD, fg=TEXT,
                         relief="flat", insertbackground=TEXT)
            e.pack(fill="x", ipady=4)
            opt_entries.append(e)

        tk.Label(form, text="Correct answer", font=F_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
        answer_var = tk.StringVar(master=dlg, value="A")
        rb_row = tk.Frame(form, bg=BG); rb_row.pack(anchor="w")
        for i, letter in enumerate(["A","B","C","D"]):
            tk.Radiobutton(rb_row, text=letter, variable=answer_var,
                           value=letter, font=F_BODY,
                           bg=BG, fg=TEXT, selectcolor=CARD,
                           activebackground=BG).pack(side="left", padx=8)

        tk.Label(form, text="Explanation (optional)", font=F_SMALL,
                 bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(8,0))
        exp_entry = tk.Entry(form, font=F_SMALL, bg=CARD, fg=TEXT,
                             relief="flat", insertbackground=TEXT)
        exp_entry.pack(fill="x", ipady=3)

        def save_q():
            qt = q_entry.get("1.0","end").strip()
            opts = [e.get().strip() for e in opt_entries]
            if not qt or any(o == "" for o in opts):
                messagebox.showwarning("Missing info",
                    "Please fill in the question and all 4 options.", parent=dlg)
                return
            ans_idx = {"A":0,"B":1,"C":2,"D":3}[answer_var.get()]
            self._new_questions.append({
                "q": qt, "options": opts,
                "answer": ans_idx,
                "explanation": exp_entry.get().strip()
            })
            self._refresh_q_list()
            dlg.destroy()

        tk.Frame(dlg, bg=BORDER, height=1).pack(fill="x", padx=20, pady=8)
        tk.Button(dlg, text="✓  ADD QUESTION", font=F_BTN,
                  bg=PURPLE, fg=TEXT, relief="flat", pady=10, cursor="hand2",
                  command=save_q).pack(fill="x", padx=24, pady=(0,20))

    def _save_quiz(self):
        title = self._c_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a quiz title.")
            return
        if len(self._new_questions) < 2:
            messagebox.showerror("Error", "Please add at least 2 questions.")
            return
        try: tpq = int(self._c_time.get())
        except ValueError: tpq = 30

        import uuid
        quiz = {
            "id":          f"custom_{int(time.time())}",
            "title":       title,
            "description": self._c_desc.get().strip(),
            "category":    self._c_cat.get(),
            "time_per_q":  tpq,
            "questions":   self._new_questions[:],
        }
        self.data.setdefault("custom_quizzes", []).append(quiz)
        save_data(self.data)
        messagebox.showinfo("Saved!", f"'{title}' saved with {len(quiz['questions'])} questions.")
        self.show_create()

    def _delete_custom_quiz(self, quiz):
        if messagebox.askyesno("Delete", f"Delete '{quiz['title']}'?"):
            self.data["custom_quizzes"] = [
                q for q in self.data["custom_quizzes"] if q["id"] != quiz["id"]]
            save_data(self.data)
            self.show_create()

    # ══════════════════════════ LEADERBOARD ══════════════════════════════════
    def show_leaderboard(self):
        self._set_active_nav("Leaderboard")
        self._switch(self._build_leaderboard)

    def _build_leaderboard(self, parent):
        inner = self._scrollable(parent)

        tk.Label(inner, text="🏆  Leaderboard", font=F_TITLE,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(24,4))
        tk.Label(inner, text="Your personal scores across all quizzes.",
                 font=F_BODY, bg=BG, fg=SUBTEXT).pack(anchor="w", padx=28)
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)

        scores = self.data.get("scores", [])
        if not scores:
            tk.Label(inner, text="No scores yet. Play a quiz to appear here!",
                     font=F_BODY, bg=BG, fg=SUBTEXT).pack(padx=28, pady=20)
            return

        
        by_quiz = {}
        for s in scores:
            q = s["quiz"]
            by_quiz.setdefault(q, []).append(s["pct"])

        summary = sorted(
            [{"quiz": q, "best": max(v), "avg": int(sum(v)/len(v)), "plays": len(v)}
             for q, v in by_quiz.items()],
            key=lambda x: -x["best"]
        )

        
        hdr = tk.Frame(inner, bg=SURFACE, padx=16, pady=8)
        hdr.pack(fill="x", padx=24, pady=(0,4))
        for txt, w in [("#",30),("Quiz",300),("Best",80),("Avg",80),("Plays",60)]:
            tk.Label(hdr, text=txt, font=F_SMALL, bg=SURFACE, fg=SUBTEXT,
                     width=w//10).pack(side="left", padx=4)

        for i, row_data in enumerate(summary):
            row = tk.Frame(inner, bg=CARD if i%2==0 else CARD2, padx=16, pady=10)
            row.pack(fill="x", padx=24, pady=1)
            rank_col = [GOLD, SUBTEXT, SUBTEXT][min(i,2)]
            medals   = ["🥇","🥈","🥉"]
            medal    = medals[i] if i < 3 else str(i+1)
            tk.Label(row, text=medal, font=F_BODY,
                     bg=row.cget("bg"), fg=rank_col).pack(side="left", padx=4)
            tk.Label(row, text=row_data["quiz"], font=F_BODY,
                     bg=row.cget("bg"), fg=TEXT, width=30,
                     anchor="w").pack(side="left", padx=4)
            col = GREEN if row_data["best"]>=70 else (GOLD if row_data["best"]>=40 else RED)
            tk.Label(row, text=f"{row_data['best']}%", font=F_MONO,
                     bg=row.cget("bg"), fg=col, width=6).pack(side="left", padx=4)
            tk.Label(row, text=f"{row_data['avg']}%", font=F_MONO,
                     bg=row.cget("bg"), fg=SUBTEXT, width=6).pack(side="left", padx=4)
            tk.Label(row, text=str(row_data["plays"]), font=F_MONO,
                     bg=row.cget("bg"), fg=SUBTEXT, width=4).pack(side="left", padx=4)

        
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)
        tk.Button(inner, text="🗑  Clear All Scores", font=F_BTN,
                  bg=CARD, fg=RED, relief="flat", padx=14, pady=7,
                  cursor="hand2", command=self._clear_scores).pack(anchor="w", padx=24, pady=(0,24))

    def _clear_scores(self):
        if messagebox.askyesno("Clear Scores", "Delete all score history?"):
            self.data["scores"] = []
            save_data(self.data)
            self.show_leaderboard()

    # ── Username ─────────────────────────────────────────────────────────────
    def _change_username(self, event=None):
        name = simpledialog.askstring("Change Name",
            "Enter your name:", initialvalue=self.data["username"], parent=self)
        if name and name.strip():
            self.data["username"] = name.strip()
            save_data(self.data)
            self._user_lbl.config(text=f"👤  {self.data['username']}")


# ─────────────────────────── RUN ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QuizForge()
    app.mainloop()
