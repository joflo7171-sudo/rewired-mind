"""Fictional sample data for the DEMO workbook. No real people, businesses or addresses.
Phone numbers use the 555-01xx range reserved for fiction; emails use example.com."""
import random
import datetime as dt

AS_OF = dt.date(2026, 9, 30)
D = dt.date
T = dt.time

TYPES = {  # rate, sqft/hr, min/bed, min/bath, setup
    "Standard Clean": (50, 800, 5, 15, 10),
    "Deep Clean": (55, 400, 10, 30, 15),
    "Move-In/Move-Out": (55, 350, 15, 40, 20),
    "Airbnb Turnover": (50, 900, 10, 20, 15),
    "Commercial Clean": (45, 2500, 0, 20, 15),
}
FREQ = {"Weekly": (0.15, 7), "Biweekly": (0.10, 14), "Every 4 weeks": (0.05, 28), "Monthly": (0.05, 30)}
MIN_JOB = 120


def hours(t, sq, bd, ba):
    rate, sph, mb, mba, setup = TYPES[t]
    return sq / sph + bd * mb / 60 + ba * mba / 60 + setup / 60


def base_price(t, sq, bd, ba):
    return max(MIN_JOB, hours(t, sq, bd, ba) * TYPES[t][0])


def r5(x):
    return int(round(x / 5.0)) * 5


FIRST = ["Avery", "Blake", "Casey", "Devon", "Emerson", "Finley", "Harper", "Jamie", "Kendall", "Logan", "Morgan",
         "Parker", "Quinn", "Reese", "Rowan", "Sage", "Skyler", "Taylor", "Toni", "Wren", "Ellis", "Marlow", "Jules",
         "Robin", "Sasha", "Remy", "Drew", "Hollis", "Lane", "Arden", "Micah", "Noel", "Shay", "Tatum", "Rory", "Kai",
         "Lennox", "Oakley", "Peyton", "Riley", "Sloane", "Blair", "Carmen", "Dana", "Elliot", "Frankie"]
LAST = ["Collins", "Bennett", "Hayes", "Monroe", "Sutton", "Porter", "Ellison", "Whitaker", "Calloway", "Delgado",
        "Fairbanks", "Garrison", "Holloway", "Kensington", "Lockhart", "Merriweather", "Northcott", "Oakes", "Pembrook",
        "Quigley", "Ransford", "Sterling", "Thornbury", "Underhill", "Vance", "Winslow", "Yardley", "Ashworth",
        "Brightwater", "Crestfield", "Dunmore", "Everly", "Foxworth", "Glenwood", "Hartwell", "Ivers", "Jessup"]
STREETS = ["Birch Lane", "Maple Avenue", "Cedar Court", "Willow Way", "Juniper Street", "Aspen Drive", "Hawthorn Road",
           "Linden Place", "Sycamore Street", "Magnolia Circle", "Poplar Trail", "Chestnut Row", "Elm Terrace",
           "Laurel Street", "Spruce Hollow", "Alder Lane", "Hazel Court", "Rowan Drive"]
AREAS = ["Sampletown", "North Sampletown", "Lakeview (fictional)", "Riverbend (fictional)", "Old Mill District"]


def generate(seed=11):
    rnd = random.Random(seed)
    used = set()

    def person():
        while True:
            n = f"{rnd.choice(FIRST)} {rnd.choice(LAST)}"
            if n not in used:
                used.add(n)
                return n

    phone_i = [100]

    def phone():
        phone_i[0] += 1
        return f"(555) 01{phone_i[0] % 100:02d}-{rnd.randint(1000, 9999)}"[:15].replace("01", "01", 1)

    ph = [3]

    def phone2():
        ph[0] += 1
        return f"555-01{ph[0] % 100:02d}"

    def email(n):
        return n.lower().replace(" ", ".") + "@example.com"

    addr_used = set()

    def address():
        while True:
            a = f"{rnd.randint(10, 980)} {rnd.choice(STREETS)}"
            if a not in addr_used:
                addr_used.add(a)
                return a

    staff = [
        dict(name="Jordan Rivera", role="Owner", rate=28, phone="555-0100", email="jordan@example.com", status="Active",
             start=D(2024, 3, 1), notes="Owner-operator; covers inspections"),
        dict(name="Maria Lopez", role="Team Lead", rate=21, phone="555-0101", email="maria@example.com", status="Active",
             start=D(2025, 2, 10), notes="Leads deep cleans and move-outs"),
        dict(name="Dana Whitfield", role="Cleaner", rate=19, phone="555-0102", email="dana@example.com", status="Active",
             start=D(2025, 8, 4), notes=""),
        dict(name="Kevin Osei", role="Cleaner", rate=18.5, phone="555-0103", email="kevin@example.com", status="Active",
             start=D(2026, 1, 12), notes="Short-term rental turnovers"),
    ]
    sources_w = [("Google Business Profile", 6), ("Google Search", 4), ("Referral", 5), ("Facebook", 3),
                 ("Nextdoor", 3), ("Website Form", 3), ("Instagram", 1), ("Flyer / Door Hanger", 2)]

    def source():
        tot = sum(w for _, w in sources_w)
        x = rnd.uniform(0, tot)
        for s, w in sources_w:
            x -= w
            if x <= 0:
                return s
        return sources_w[0][0]

    customers, properties = [], []

    def add_customer(ctype, name=None, added=None):
        n = name or person()
        c = dict(name=n, phone=phone2(), email=email(n) if " " in n else "office@example.com", ctype=ctype,
                 source=source(), contact=rnd.choice(["Text", "Text", "Email", "Call"]), status="Active",
                 added=added, notes="")
        customers.append(c)
        return c

    def add_property(cust, ptype, sq, bd, ba, pets="", special=""):
        a = address() + ", " + rnd.choice(AREAS[:3])
        p = dict(addr=a, customer=cust["name"], area=a.split(", ")[1], ptype=ptype, sq=sq, beds=bd, baths=ba,
                 pets=pets, access=rnd.choice(["Lockbox code on file", "Customer home", "Garage keypad (code in office file)",
                                               "Key under office management", "Smart lock — code sent day before"]),
                 parking=rnd.choice(["Driveway", "Street", "Visitor lot", "Garage apron"]), special=special)
        properties.append(p)
        return p

    # residential customers
    res = []
    for i in range(22):
        c = add_customer("Residential")
        sq = rnd.choice([1100, 1300, 1500, 1700, 1800, 2000, 2200, 2400, 2600, 2900, 3200, 3600])
        bd = 2 if sq < 1400 else 3 if sq < 2100 else 4 if sq < 3000 else 5
        ba = 1.5 if sq < 1400 else 2 if sq < 2100 else 2.5 if sq < 2600 else 3 if sq < 3000 else 3.5
        p = add_property(c, rnd.choice(["House", "House", "Townhome", "Condo"]), sq, bd, ba,
                         pets=rnd.choice(["", "", "1 dog", "2 cats", "1 cat"]),
                         special=rnd.choice(["", "", "Unscented products only", "Skip office room", "Shoes off at entry"]))
        res.append((c, p))
    # commercial
    com = []
    for nm, sq, ba in [("Brightside Dental Studio (sample)", 2400, 2), ("Oakview Office Suites (sample)", 5200, 4),
                       ("Harbor Yoga Loft (sample)", 1800, 2)]:
        c = add_customer("Commercial", nm)
        c["contact"] = "Email"
        p = add_property(c, "Medical/Dental" if "Dental" in nm else "Office", sq, 0, ba, special="After-hours only")
        com.append((c, p))
    # short-term rental hosts
    strs = []
    for i in range(4):
        c = add_customer("Short-Term Rental Host")
        sq = rnd.choice([850, 1000, 1200, 1400])
        p = add_property(c, "Short-Term Rental", sq, 1 if sq < 950 else 2, 1 if sq < 1300 else 2,
                         special="Photo each room after reset")
        strs.append((c, p))
    # property manager with 3 units (move-outs)
    pm = add_customer("Property Manager", "Crescent Property Group (sample)")
    pm["contact"] = "Email"
    pm_units = [add_property(pm, "Apartment", sq, bd, ba) for sq, bd, ba in [(900, 2, 1), (1150, 2, 2), (1400, 3, 2)]]

    jobs, plans = [], []
    workers = ["Maria Lopez", "Dana Whitfield", "Kevin Osei", "Jordan Rivera"]
    times = [T(8, 0), T(8, 30), T(9, 0), T(10, 0), T(11, 30), T(12, 30), T(13, 0), T(14, 0), T(15, 0)]

    def add_job(date, cust, prop, service, price, worker, crew=1, plan=None, est=None, notes=""):
        h = hours(service, prop["sq"], prop["beds"], prop["baths"])
        status = "Completed" if date <= AS_OF else "Scheduled"
        if status == "Completed" and rnd.random() < 0.035:
            status = rnd.choice(["Cancelled", "Rescheduled"])
        act = round(h * rnd.uniform(0.85, 1.22), 2) if status == "Completed" else None
        j = dict(date=date, time=rnd.choice(times), customer=cust["name"], property=prop["addr"], service=service,
                 plan=plan, worker=worker, crew=crew, est=est, act=act, price=price, tax=0, status=status, notes=notes)
        jobs.append(j)
        return j

    # recurring plans
    plan_defs = []
    freq_choices = ["Weekly", "Biweekly", "Biweekly", "Biweekly", "Biweekly", "Every 4 weeks", "Biweekly", "Weekly",
                    "Every 4 weeks", "Monthly"]
    for i, (c, p) in enumerate(res[:10]):
        start = D(2026, 1, 12) + dt.timedelta(days=rnd.randint(0, 170))
        plan_defs.append((c, p, "Standard Clean", freq_choices[i], start))
    plan_defs.append((com[0][0], com[0][1], "Commercial Clean", "Weekly", D(2026, 2, 6)))
    plan_defs.append((com[1][0], com[1][1], "Commercial Clean", "Weekly", D(2026, 4, 3)))
    for idx, (c, p, svc, fq, start) in enumerate(plan_defs):
        pid = f"R-{idx + 1:03d}"
        disc, days = FREQ[fq]
        price = r5(base_price(svc, p["sq"], p["beds"], p["baths"]) * (1 - disc))
        worker = "Dana Whitfield" if svc == "Standard Clean" and idx % 2 else ("Maria Lopez" if svc == "Standard Clean" else "Kevin Osei")
        status = "Active"
        end = AS_OF + dt.timedelta(days=12)
        if idx == 3:
            status, end = "Paused", D(2026, 8, 10)
        if idx == 7:
            status, end = "Ended", D(2026, 6, 20)
        if idx == 0:
            end = AS_OF - dt.timedelta(days=9)  # demo: an active plan whose next visit is overdue
        plans.append(dict(customer=c["name"], property=p["addr"], service=svc, freq=fq, price=price, worker=worker,
                          start=start, pref=start.strftime("%A") + (" AM" if idx % 2 else " PM"), status=status,
                          notes="Started with deep clean" if svc == "Standard Clean" else "After 6 PM"))
        # first deep clean for residential plans
        if svc == "Standard Clean":
            dc = r5(base_price("Deep Clean", p["sq"], p["beds"], p["baths"]))
            add_job(start - dt.timedelta(days=7), c, p, "Deep Clean", dc, "Maria Lopez", 2, notes="Initial deep clean")
        d = start
        while d <= end:
            add_job(d, c, p, svc, price, worker, 1 if svc == "Standard Clean" else 2, plan=pid)
            if fq == "Monthly":
                m = d.month + 1
                d = D(d.year + (m > 12), (m - 1) % 12 + 1, min(d.day, 28))
            else:
                d += dt.timedelta(days=days)
    # one-time residential deep cleans / standard
    for c, p in res[10:]:
        n = rnd.randint(1, 3)
        base = D(2026, 1, 15) + dt.timedelta(days=rnd.randint(0, 250))
        for k in range(n):
            svc = "Deep Clean" if k == 0 else "Standard Clean"
            d = base + dt.timedelta(days=k * rnd.randint(30, 60))
            if d > AS_OF + dt.timedelta(days=10):
                break
            pr = r5(base_price(svc, p["sq"], p["beds"], p["baths"])) + (rnd.choice([0, 35, 70]) if svc == "Deep Clean" else 0)
            add_job(d, c, p, svc, pr, "Maria Lopez" if svc == "Deep Clean" else rnd.choice(workers[:3]),
                    2 if svc == "Deep Clean" else 1, notes="Oven + fridge add-ons" if pr % 70 == 0 and svc == "Deep Clean" else "")
    # short-term rental turnovers
    for c, p in strs:
        d = D(2026, 1, 9) + dt.timedelta(days=rnd.randint(0, 20))
        while d <= AS_OF + dt.timedelta(days=8):
            pr = r5(base_price("Airbnb Turnover", p["sq"], p["beds"], p["baths"]) + 15 * p["beds"])
            add_job(d, c, p, "Airbnb Turnover", pr, "Kevin Osei", 1, notes="Includes laundry")
            d += dt.timedelta(days=rnd.randint(9, 20))
    # yoga loft: every 4 weeks-ish one-time commercial
    c, p = com[2]
    for d in [D(2026, 3, 14), D(2026, 5, 9), D(2026, 7, 11), D(2026, 9, 12)]:
        add_job(d, c, p, "Commercial Clean", r5(base_price("Commercial Clean", p["sq"], 0, p["baths"]) + 40), "Dana Whitfield", 2)
    # move-outs for property manager
    for u, d in zip(pm_units + pm_units[:2], [D(2026, 2, 27), D(2026, 5, 29), D(2026, 7, 31), D(2026, 9, 25), D(2026, 10, 6)]):
        add_job(d, pm, u, "Move-In/Move-Out", r5(base_price("Move-In/Move-Out", u["sq"], u["beds"], u["baths"]) + 75),
                "Maria Lopez", 2, est=round(hours("Move-In/Move-Out", u["sq"], u["beds"], u["baths"]) + 1.25, 2),
                notes="Inside oven, fridge, cabinets")
    # a loss-making example (underpriced job)
    c, p = res[12]
    add_job(D(2026, 9, 18), c, p, "Deep Clean", 180, "Maria Lopez", 2, notes="Discounted too far — see profit")

    jobs.sort(key=lambda j: (j["date"], j["time"]))
    for i, j in enumerate(jobs):
        j["id"] = f"J-{i + 1:04d}"

    # customers added date & first job date
    first_job = {}
    for j in jobs:
        first_job.setdefault(j["customer"], j["date"])
    for c in customers:
        fj = first_job.get(c["name"], AS_OF)
        c["added"] = fj - dt.timedelta(days=rnd.randint(3, 12))
    # tag one inactive customer
    for c in customers:
        if c["name"] == res[20][0]["name"]:
            c["notes"] = "Moved? Try a reactivation message"

    # payments
    payments = []
    methods = [("Card", 45), ("Online Invoice", 20), ("Payment App", 15), ("Cash", 10), ("Check", 10)]

    def method():
        x = rnd.uniform(0, 100)
        for m, w in methods:
            x -= w
            if x <= 0:
                return m
        return "Card"
    for j in jobs:
        if j["status"] != "Completed":
            continue
        days_ago = (AS_OF - j["date"]).days
        roll = rnd.random()
        if days_ago < 20 and roll < 0.18:
            continue  # unpaid
        pay_d = j["date"] + dt.timedelta(days=rnd.choice([0, 0, 0, 1, 2, 5]))
        if pay_d > AS_OF:
            pay_d = AS_OF
        amt = j["price"]
        if 0.18 <= roll < 0.22 and days_ago < 40:
            amt = round(j["price"] / 2, 2)
        m = "Online Invoice" if "sample" in j["customer"] else method()
        payments.append(dict(date=pay_d, job=j["id"], amount=amt, tip=rnd.choice([None] * 8 + [10, 20]),
                             method=m, ref="INV-" + j["id"][2:], notes="Deposit / partial" if amt != j["price"] else ""))
    payments.sort(key=lambda x: x["date"])

    # mileage
    mileage = []
    for j in jobs:
        if j["status"] != "Completed":
            continue
        miles = round(rnd.uniform(6, 24), 1)
        row = dict(date=j["date"], job=j["id"], purpose=f"Job: {j['service']}", frm="Home base", to=j["property"].split(",")[0],
                   driver=j["worker"])
        if rnd.random() < 0.15:
            o = rnd.randint(40000, 60000)
            row.update(odo1=o, odo2=o + int(miles))
        else:
            row["miles"] = miles
        mileage.append(row)
    for m in range(1, 10):
        mileage.append(dict(date=D(2026, m, 20), purpose="Supply run", frm="Home base", to="Supply store", miles=11.5,
                            driver="Jordan Rivera"))
    mileage.sort(key=lambda x: x["date"])
    for row in mileage:
        row["from"] = row.pop("frm")

    # expenses
    expenses = []
    for m in range(1, 10):
        def e(day, cat, vendor, desc, amt, pw="Card", receipt="Yes"):
            expenses.append(dict(date=D(2026, m, day), cat=cat, vendor=vendor, desc=desc, amount=amt, paidwith=pw, receipt=receipt))
        e(1, "Software & Apps", "Scheduling app (sample)", "Monthly subscription", 49)
        e(3, "Phone & Internet", "Mobile carrier (sample)", "Business line", 85)
        e(5, "Insurance", "Insurance agency (sample)", "Monthly premium", 165)
        e(8, "Advertising & Marketing", rnd.choice(["Local print shop", "Social media ads", "Community newsletter"]), "Local marketing", rnd.choice([80, 120, 150, 220, 300]))
        e(10, "Supplies (job use)", "Janitorial supplier (sample)", "Chemicals & microfiber", rnd.randint(120, 260))
        e(24, "Supplies (job use)", "Big-box store", "Liners, paper goods", rnd.randint(60, 140))
        for wk in (6, 13, 20, 27):
            e(wk, "Fuel & Vehicle", "Fuel station", "Fuel", rnd.randint(45, 70))
        e(28, "Bank Fees", "Bank (sample)", "Account fee", 12, "Bank Transfer")
    expenses += [
        dict(date=D(2026, 3, 2), cat="Uniforms", vendor="Uniform shop (sample)", desc="Team shirts x8", amount=184, paidwith="Card", receipt="Yes"),
        dict(date=D(2026, 4, 15), cat="Professional Fees", vendor="Bookkeeper (sample)", desc="Quarterly bookkeeping", amount=250, paidwith="Bank Transfer", receipt="Yes"),
        dict(date=D(2026, 5, 19), cat="Equipment", vendor="Equipment dealer (sample)", desc="Commercial vacuum", amount=389, paidwith="Card", receipt="Yes"),
        dict(date=D(2026, 7, 7), cat="Training", vendor="Online course (sample)", desc="Team training module", amount=99, paidwith="Card", receipt="No"),
        dict(date=D(2026, 9, 16), cat="Equipment", vendor="Equipment dealer (sample)", desc="Extension poles & squeegees", amount=142, paidwith="Card", receipt="Yes"),
    ]
    expenses.sort(key=lambda x: x["date"])

    # leads
    leads = []
    plan_customers = {p["customer"] for p in plans if p["status"] == "Active"}
    for c in customers:
        fj = [j for j in jobs if j["customer"] == c["name"]]
        q = fj[0]["price"] if fj else 150
        leads.append(dict(date=c["added"], name=c["name"], phone=c["phone"], email=c["email"], source=c["source"],
                          service=fj[0]["service"] if fj else "Standard Clean", area=next(p["area"] for p in properties if p["customer"] == c["name"]),
                          quote=q, stage="Recurring Client" if c["name"] in plan_customers else "Booked",
                          last=c["added"] + dt.timedelta(days=1), next=None, notes=""))
    lost_reasons = ["Price", "Chose another company", "No response", "Timing / availability", "Outside service area", "Price", "No response"]
    for i in range(30):
        d = D(2026, 1, 10) + dt.timedelta(days=rnd.randint(0, 225))
        n = person()
        svc = rnd.choice(list(TYPES)[:4])
        leads.append(dict(date=d, name=n, phone=phone2(), email=email(n), source=source(), service=svc,
                          area=rnd.choice(AREAS), quote=rnd.choice([None, 160, 210, 285, 340, 395]), stage="Lost/Declined",
                          last=d + dt.timedelta(days=rnd.randint(2, 9)), next=None, lost=rnd.choice(lost_reasons), notes=""))
    open_defs = [("New Lead", 0, None), ("New Lead", 1, 0), ("New Lead", 2, -1),
                 ("Contacted", 3, 0), ("Contacted", 5, -2), ("Contacted", 4, 2),
                 ("Quote Requested", 2, 1), ("Quote Requested", 6, -1),
                 ("Quote Sent", 5, 1), ("Quote Sent", 8, -3), ("Quote Sent", 14, 2), ("Quote Sent", 20, -4),
                 ("Follow-Up", 28, -1), ("Follow-Up", 35, 3), ("Follow-Up", 40, 5)]
    for stage, ago, nxt in open_defs:
        d = AS_OF - dt.timedelta(days=ago + rnd.randint(0, 4))
        n = person()
        svc = rnd.choice(list(TYPES))
        quote = None if stage in ("New Lead", "Contacted", "Quote Requested") else rnd.choice([165, 190, 240, 310, 365, 420, 520])
        leads.append(dict(date=d, name=n, phone=phone2(), email=email(n), source=source(), service=svc, area=rnd.choice(AREAS),
                          quote=quote, stage=stage, last=None if stage == "New Lead" and nxt is None else min(AS_OF, d + dt.timedelta(days=1)),
                          next=None if nxt is None else AS_OF + dt.timedelta(days=nxt), notes=""))
    # booked lead not yet added to customers
    n = person()
    leads.append(dict(date=AS_OF - dt.timedelta(days=3), name=n, phone=phone2(), email=email(n), source="Referral",
                      service="Deep Clean", area="Sampletown", quote=345, stage="Booked", last=AS_OF - dt.timedelta(days=1),
                      notes="Booked for Oct 8 — add to CUSTOMERS"))
    leads.sort(key=lambda x: x["date"])

    # reviews
    reviews = []
    for c in customers:
        cj = [j for j in jobs if j["customer"] == c["name"] and j["status"] == "Completed"]
        if not cj or rnd.random() < 0.35:
            continue
        j = cj[0] if rnd.random() < 0.6 else cj[-1]
        req = j["date"] + dt.timedelta(days=1)
        if req > AS_OF:
            continue
        roll = rnd.random()
        if (AS_OF - req).days < 12:
            status = "Requested"
        elif roll < 0.68:
            status = "Received"
        elif roll < 0.82:
            status = "Reminder sent"
        else:
            status = "No response"
        rec = req + dt.timedelta(days=rnd.randint(0, 4)) if status == "Received" else None
        rating = rnd.choice([5, 5, 5, 5, 4, 5, 4, 3]) if status == "Received" else None
        reviews.append(dict(customer=c["name"], job=j["id"], req=req, platform=rnd.choice(["Google"] * 5 + ["Facebook", "Nextdoor"]),
                            status=status, rec=rec, rating=rating, replied=("Yes" if rnd.random() < 0.85 else "No") if status == "Received" else None,
                            notes="Mentioned attention to detail" if rating == 5 else ("Wanted baseboards done — follow up" if rating == 3 else "")))
    reviews.sort(key=lambda x: x["req"])

    # referrals
    referrals = []
    booked_refs = [c for c in customers if c["source"] == "Referral"][:4]
    for i, c in enumerate(booked_refs):
        by = rnd.choice([x for x in customers if x["ctype"] == "Residential" and x["name"] != c["name"]])
        referrals.append(dict(date=c["added"], by=by["name"], new=c["name"], contact=c["phone"], status="Booked",
                              reward="$25 service credit (example)", rstatus="Given" if i < 3 else "Owed", notes=""))
    for st in ["Quoted", "Not booked", "Referred"]:
        by = rnd.choice([x for x in customers if x["ctype"] == "Residential"])
        n = person()
        referrals.append(dict(date=AS_OF - dt.timedelta(days=rnd.randint(3, 60)), by=by["name"], new=n, contact=phone2(),
                              status=st, reward="$25 service credit (example)", rstatus="Not due", notes=""))
    referrals.sort(key=lambda x: x["date"])

    # quality control
    qc = []
    cl_map = {"Standard Clean": "Residential Standard", "Deep Clean": "Deep Clean", "Move-In/Move-Out": "Move-In/Move-Out",
              "Airbnb Turnover": "Airbnb Turnover", "Commercial Clean": "Commercial"}
    done = [j for j in jobs if j["status"] == "Completed"]
    for j in sorted(rnd.sample(done, 48), key=lambda x: x["date"]):
        checked = rnd.randint(20, 28)
        miss = rnd.choice([0, 0, 0, 0, 1, 1, 2, 3, 4])
        passed = checked - miss
        fail = passed / checked < 0.9
        qc.append(dict(date=j["date"], job=j["id"], list=cl_map[j["service"]], inspector="Jordan Rivera", checked=checked,
                       passed=passed, found="" if miss == 0 else rnd.choice(["Streaks on mirror", "Baseboards missed in hallway",
                                                                             "Dust on ceiling fan", "Trash not replaced in bath",
                                                                             "Stovetop residue"]),
                       rework="Yes" if fail else "No", rdate=j["date"] + dt.timedelta(days=1) if fail else None,
                       resolved=("Yes" if j["date"] < AS_OF - dt.timedelta(days=5) else "No") if fail else None))
    issues = []
    samp = sorted(rnd.sample(done, 6), key=lambda x: x["date"])
    iss_defs = [("Customer", "Missed area", "Guest bath floor not mopped", "Returned next morning at no charge", "Resolved"),
                ("Customer", "Late / no-show", "Crew arrived 50 minutes late", "Apologized; 10% credit on next visit", "Resolved"),
                ("Staff", "Access problem", "Lockbox code did not work", "Rescheduled; updated access notes", "Resolved"),
                ("Inspection", "Quality complaint", "Kitchen backsplash streaky", "Coaching with cleaner; re-cleaned", "Resolved"),
                ("Customer", "Damage report", "Customer reports chipped vase", "Documented with photos; owner reviewing", "In progress"),
                ("Customer", "Billing question", "Charged for add-on not requested", "Checking job notes", "Open")]
    for j, (by, t, desc, act, st) in zip(samp, iss_defs):
        d = j["date"] + dt.timedelta(days=1)
        if st != "Resolved" and d < AS_OF - dt.timedelta(days=20):
            d = AS_OF - dt.timedelta(days=rnd.randint(2, 8))
        issues.append(dict(date=d, job=j["id"], by=by, type=t, desc=desc, action=act,
                           rework=d + dt.timedelta(days=1) if t in ("Missed area", "Quality complaint") else None,
                           status=st, cost=rnd.choice([0, 25, 40]) if st == "Resolved" else None,
                           closed=d + dt.timedelta(days=rnd.randint(1, 4)) if st == "Resolved" else None))

    # follow-ups (manual)
    unpaid_jobs = [j for j in jobs if j["status"] == "Completed" and not any(p["job"] == j["id"] for p in payments)]
    fu = []
    for j in unpaid_jobs[:2]:
        fu.append(dict(due=AS_OF - dt.timedelta(days=1), contact=j["customer"], type="Invoice", related=j["id"], channel="Text",
                       workflow="03 Quote follow-up", status="Open", notes="Send friendly payment reminder"))
    inactive = res[20][0]["name"]
    fu += [
        dict(due=AS_OF, contact=inactive, type="Reactivation", related="", channel="Email", workflow="10 Reactivation", status="Open", notes=""),
        dict(due=AS_OF + dt.timedelta(days=2), contact=res[5][0]["name"], type="Referral", related="", channel="Text", workflow="09 Referral request", status="Open", notes="Loves the service — ask for a referral"),
        dict(due=AS_OF - dt.timedelta(days=6), contact=res[2][0]["name"], type="Review", related="", channel="Text", workflow="07 Review request", status="Done", notes="Left 5 stars"),
        dict(due=AS_OF + dt.timedelta(days=5), contact="Oakview Office Suites (sample)", type="Other", related="", channel="Email", workflow="15 Commercial proposal", status="Open", notes="Propose adding window service"),
        dict(due=AS_OF - dt.timedelta(days=3), contact=issues[-1]["job"], type="Complaint", related=issues[-1]["job"], channel="Call", workflow="17 Complaint response", status="Open", notes="Billing question — call back"),
        dict(due=AS_OF - dt.timedelta(days=15), contact=res[8][0]["name"], type="Quote", related="", channel="Text", workflow="03 Quote follow-up", status="Skipped", notes="Customer said not this season"),
    ]
    fu[-2]["contact"] = next(j["customer"] for j in jobs if j["id"] == issues[-1]["job"])

    tasks = [
        dict(task="Restock van kits (microfiber, liners, glass cleaner)", to="Dana Whitfield", due=AS_OF + dt.timedelta(days=1), prio="High", status="Not started"),
        dict(task="Wash and dry all microfiber cloths", to="Kevin Osei", due=AS_OF, prio="Medium", status="In progress"),
        dict(task="Update access notes for lockbox customers", to="Jordan Rivera", due=AS_OF - dt.timedelta(days=2), prio="High", status="Not started"),
        dict(task="Photograph before/after for Deep Clean jobs this week (with permission)", to="Maria Lopez", due=AS_OF + dt.timedelta(days=4), prio="Low", status="Not started"),
        dict(task="Inspect vacuum filters and replace if worn", to="Maria Lopez", due=AS_OF - dt.timedelta(days=5), prio="Medium", status="Done"),
        dict(task="Shadow Maria on a move-out clean", to="Kevin Osei", due=AS_OF + dt.timedelta(days=6), prio="Medium", status="Not started"),
        dict(task="Send weekly schedule to team", to="Jordan Rivera", due=AS_OF + dt.timedelta(days=3), prio="High", status="Not started"),
    ]
    supplies = [
        ("All-purpose cleaner concentrate", "Chemicals", "1 gal", 18.50, 3, 2), ("Glass cleaner", "Chemicals", "32 oz", 4.25, 5, 6),
        ("Bathroom cleaner", "Chemicals", "32 oz", 5.10, 8, 6), ("Degreaser", "Chemicals", "32 oz", 6.75, 2, 3),
        ("Neutral floor cleaner", "Chemicals", "1 gal", 16.00, 2, 1), ("Microfiber cloths (24 pk)", "Tools", "pack", 21.00, 4, 2),
        ("Scrub brushes", "Tools", "each", 3.50, 10, 6), ("Mop pads", "Tools", "each", 6.00, 12, 8),
        ("Trash liners 13 gal (200)", "Paper & Liners", "box", 24.00, 1, 2), ("Paper towels (12 rolls)", "Paper & Liners", "case", 19.00, 3, 2),
        ("Laundry detergent", "Laundry", "bottle", 12.50, 2, 2), ("Nitrile gloves (100)", "Protective Gear", "box", 11.00, 5, 3),
        ("Shoe covers (100)", "Protective Gear", "box", 9.50, 2, 2), ("HEPA vacuum bags (5)", "Equipment", "pack", 17.00, 3, 2),
        ("Extension pole", "Equipment", "each", 28.00, 2, 1), ("Spray bottles (labeled)", "Tools", "each", 1.80, 20, 10),
    ]
    supplies = [dict(item=a, cat=b, unit=c, cost=d, onhand=e, reorder=f, supplier="Janitorial supplier (sample)",
                     lastbuy=D(2026, 9, 10), notes="Follow label directions; SDS binder in van" if b == "Chemicals" else "")
                for a, b, c, d, e, f in supplies]

    # map keys to workbook column keys
    jobs_rows = [dict(id=None, date=j["date"], time=j["time"], customer=j["customer"], property=j["property"], service=j["service"],
                      plan=j["plan"], worker=j["worker"], crew=j["crew"], est=j["est"], act=j["act"], price=j["price"],
                      tax=j["tax"], status=j["status"], notes=j["notes"]) for j in jobs]
    for r in jobs_rows:
        r.pop("id")
    return dict(
        leads=leads, customers=customers,
        properties=[dict(addr=p["addr"], customer=p["customer"], area=p["area"], ptype=p["ptype"], sqft=p["sq"], beds=p["beds"],
                         baths=p["baths"], pets=p["pets"], access=p["access"], parking=p["parking"], special=p["special"]) for p in properties],
        jobs=jobs_rows, recurring=plans, staff=staff, tasks=tasks, payments=payments, expenses=expenses, mileage=mileage,
        supplies=supplies, followups=fu, reviews=reviews, referrals=referrals, qc=qc, issues=issues,
        _jobs_full=jobs,
    )


if __name__ == "__main__":
    d = generate()
    for k, v in d.items():
        print(k, len(v))
    rev = sum(j["price"] for j in d["_jobs_full"] if j["status"] == "Completed")
    print("revenue", rev)
