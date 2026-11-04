"""
app/rag/knowledge_base.py
──────────────────────────
Curated financial literacy knowledge base.

This module provides seed documents covering:
  - UPI & digital payments
  - Online scam avoidance
  - Interest rates
  - Budgeting
  - Personal finance management

Sources mirrored from RBI, NPCI, MeitY, and public banking education portals.
"""

FINANCIAL_DOCUMENTS = [
    # ── UPI & Digital Payments ──────────────────────────────────────
    {
        "id": "upi_001",
        "title": "How to Send Money via UPI",
        "category": "upi",
        "language": "en",
        "source": "NPCI / bhimupi.org.in",
        "content": """
UPI (Unified Payments Interface) is a real-time payment system developed by NPCI (National
Payments Corporation of India) that allows instant money transfers between bank accounts using
a smartphone.

HOW TO SEND MONEY VIA UPI:
1. Download a UPI-enabled app: BHIM, PhonePe, Google Pay, Paytm, or your bank's app.
2. Register by linking your bank account and setting a 4–6 digit UPI PIN.
3. To send money, choose 'Send Money' or 'Pay'.
4. Enter the recipient's UPI ID (e.g., name@bankname), mobile number, or scan their QR code.
5. Enter the amount and a remarks (optional).
6. Confirm with your UPI PIN.
7. You will receive a transaction success/failure notification instantly.

UPI TRANSACTION LIMITS:
- Standard limit: ₹1,00,000 per transaction.
- Some banks allow up to ₹5,00,000 for specific categories.
- No charges for transactions up to ₹2,000 (as per RBI guidelines).

SAFETY TIPS:
- Never share your UPI PIN with anyone, including bank employees.
- Verify the recipient's UPI ID before confirming payment.
- Do NOT enter your UPI PIN to RECEIVE money — you only need PIN to SEND.
- Use only official apps from trusted sources (Play Store / App Store).
        """.strip(),
    },
    {
        "id": "upi_002",
        "title": "UPI ID Formats and How to Find Yours",
        "category": "upi",
        "language": "en",
        "source": "NPCI",
        "content": """
A UPI ID (also called Virtual Payment Address or VPA) uniquely identifies your bank account
on the UPI network.

COMMON UPI ID FORMATS:
- mobilenumber@bankname  (e.g., 9876543210@sbi)
- username@upi           (e.g., rahul.sharma@upi — BHIM default)
- username@bankshortcode (e.g., priya@icici, ajay@hdfcbank)
- username@paytm         (Paytm wallet IDs)

HOW TO FIND YOUR UPI ID:
1. Open your UPI app (BHIM / PhonePe / Google Pay).
2. Go to Profile or My Account.
3. Your UPI ID / VPA is displayed there.
4. You can also create a custom UPI ID in most apps.

RECEIVING MONEY:
- Share your UPI ID or QR code with the sender.
- You do NOT need to share your bank account number or IFSC code.
- Money is credited directly to your linked bank account.
        """.strip(),
    },
    # ── Online Scam Avoidance ────────────────────────────────────────
    {
        "id": "scam_001",
        "title": "Common UPI and Online Payment Scams to Avoid",
        "category": "scam_prevention",
        "language": "en",
        "source": "RBI / Cyber Dost (MHA)",
        "content": """
COMMON ONLINE PAYMENT SCAMS IN INDIA:

1. SCREEN SHARING SCAM:
   Fraudsters ask you to install AnyDesk or TeamViewer, gain access to your screen,
   and steal your UPI PIN or banking credentials.
   PROTECTION: Never install screen-sharing apps at a stranger's request.

2. COLLECT REQUEST FRAUD:
   Scammers send a UPI "Collect Request" (payment request) disguised as a refund.
   Accepting and entering your PIN sends THEM money.
   PROTECTION: You enter PIN to SEND money, not to receive it. Reject unknown collect requests.

3. QR CODE SCAM:
   A fake QR code is shared saying "scan to receive your prize money."
   Scanning and entering PIN debits your account.
   PROTECTION: Scanning a QR code to RECEIVE money is impossible — always a scam.

4. KYC UPDATE SCAM:
   Calls/SMS claiming your UPI/wallet will be suspended unless you complete KYC.
   They redirect to fake sites to steal credentials.
   PROTECTION: Complete KYC only through official app or bank branch. Ignore such calls.

5. OTP FRAUD:
   Caller poses as bank/NPCI employee, asks for OTP "to verify your account."
   PROTECTION: Never share OTP, CVV, or UPI PIN with anyone over call/SMS/chat.

6. FAKE CUSTOMER CARE:
   Fraudulent customer care numbers appear on Google search results.
   PROTECTION: Always call numbers from the official bank website or app only.

REPORT FRAUD:
- National Cyber Crime Helpline: 1930
- Online: cybercrime.gov.in
- RBI Complaint Portal: cms.rbi.org.in
        """.strip(),
    },
    {
        "id": "scam_002",
        "title": "Phishing and Social Engineering Scams",
        "category": "scam_prevention",
        "language": "en",
        "source": "CERT-In / RBI",
        "content": """
PHISHING SCAMS:
Phishing is when fraudsters create fake websites or emails that look like real banks or
payment platforms to steal your login credentials.

HOW TO IDENTIFY PHISHING:
- Check the URL carefully: real SBI site is onlinesbi.com, not onlinesbi.co or sbionline.com
- Look for HTTPS padlock in the browser address bar.
- Be suspicious of urgent language: "Your account will be blocked in 24 hours!"
- Verify sender email address — banks use official domain emails only.

SOCIAL ENGINEERING:
Fraudsters manipulate you emotionally:
- "You've won a lottery" — requires advance fee payment.
- "Job offer" — asks for registration fee via UPI.
- "Your relative is in trouble" — asks for urgent money transfer.

SAFE PRACTICES:
1. Do not click links in SMS or email — type the website address directly.
2. Enable two-factor authentication on all banking apps.
3. Regularly check your bank statement for unknown transactions.
4. Use strong, unique passwords for banking apps.
5. Never save banking passwords in browsers on shared computers.
        """.strip(),
    },
    # ── Interest Rates ──────────────────────────────────────────────
    {
        "id": "interest_001",
        "title": "Understanding Loan Interest Rates in India",
        "category": "interest_rates",
        "language": "en",
        "source": "RBI / NHB",
        "content": """
TYPES OF INTEREST RATES:

1. FIXED INTEREST RATE:
   The rate remains constant throughout the loan tenure.
   Pros: Predictable EMI, good for budgeting.
   Cons: Usually slightly higher than floating rate. No benefit if market rates fall.

2. FLOATING (VARIABLE) INTEREST RATE:
   Rate changes with the RBI Repo Rate or MCLR (Marginal Cost of Funds Based Lending Rate).
   Pros: Benefit when rates fall.
   Cons: EMI uncertainty when rates rise.

TYPICAL SAFE INTEREST RATE RANGES (2024):
- Home Loan:        8.5% – 10.5% per annum (PA)
- Personal Loan:    10% – 24% PA
- Car Loan:         8.5% – 14% PA
- Education Loan:   8% – 15% PA
- Gold Loan:        7.5% – 17% PA
- Credit Card:      36% – 42% PA (very high — avoid carrying balance)
- Microfinance:     up to 26% PA (regulated cap by RBI)

RED FLAGS — PREDATORY LENDING:
- Any lender offering loans at 2–3% per MONTH = 24–36% per YEAR or more — often illegal.
- Advance fee loans: "Pay ₹500 processing fee to get your ₹50,000 loan" — scam.
- Apps not registered with RBI operating lending services — illegal digital lending.
- Check if lender is RBI-registered at: rbi.org.in > Consumer Education > Financial Entities

HOW TO CALCULATE EMI:
EMI = P × r × (1+r)^n / ((1+r)^n - 1)
Where: P = Principal, r = monthly rate, n = number of months

RULE OF THUMB: A safe loan EMI should not exceed 40% of your monthly take-home salary.
        """.strip(),
    },
    {
        "id": "interest_002",
        "title": "Savings Account and Fixed Deposit Interest Rates",
        "category": "interest_rates",
        "language": "en",
        "source": "RBI / SEBI",
        "content": """
SAVINGS ACCOUNT INTEREST RATES (approximate, 2024):
- Public sector banks (SBI, PNB, Bank of Baroda): 2.7% – 3.5% PA
- Private banks (HDFC, ICICI, Axis): 3% – 4% PA
- Small Finance Banks (AU, Equitas, Jana): 4% – 7% PA
- Payments Banks (Airtel, India Post): up to 2.5% PA

FIXED DEPOSIT (FD) RATES (approximate, 2024):
- 1-year FD (public banks): 6.5% – 7.25% PA
- 1-year FD (private banks): 7% – 7.75% PA
- 1-year FD (small finance banks): 8% – 9.5% PA
- Senior citizen FDs: additional 0.25% – 0.75% over standard rates

RECURRING DEPOSIT (RD):
- Similar to FD rates, for monthly deposits.
- Good for building a savings habit.

INSURANCE ON DEPOSITS:
- DICGC (Deposit Insurance and Credit Guarantee Corporation) insures deposits up to
  ₹5,00,000 per depositor per bank. Your money is safe even if the bank fails.

POST OFFICE SCHEMES (guaranteed by Government of India):
- Public Provident Fund (PPF): ~7.1% PA, 15-year lock-in, tax-free returns.
- National Savings Certificate (NSC): ~7.7% PA.
- Sukanya Samriddhi Yojana (for girl child): ~8.2% PA.
        """.strip(),
    },
    # ── Budgeting ───────────────────────────────────────────────────
    {
        "id": "budget_001",
        "title": "How to Create a Personal Budget",
        "category": "budgeting",
        "language": "en",
        "source": "RBI Financial Education",
        "content": """
BUDGETING is the process of planning how to spend and save your income so that you meet
your financial goals without running into debt.

THE 50/30/20 RULE (popular framework):
- 50% of income → Needs (rent, food, utilities, transport, EMIs)
- 30% of income → Wants (dining out, entertainment, shopping)
- 20% of income → Savings and investments (FD, PPF, mutual funds)

STEP-BY-STEP BUDGET CREATION:
1. CALCULATE YOUR MONTHLY INCOME: Include salary, freelance, rent income, etc.
2. LIST ALL EXPENSES:
   - Fixed: Rent, EMI, school fees, insurance premium
   - Variable: Groceries, electricity, phone bill
   - Discretionary: Eating out, movies, clothes
3. SUBTRACT EXPENSES FROM INCOME to find surplus or deficit.
4. SET SAVINGS GOALS: Emergency fund, retirement, education, home purchase.
5. TRACK SPENDING: Use a notebook, spreadsheet, or apps (ET Money, Walnut, Money Manager).
6. REVIEW MONTHLY: Adjust the budget based on actual spending.

EMERGENCY FUND:
- Build a fund equal to 3–6 months of expenses.
- Keep it in a liquid savings account or short-term FD.
- Use only for genuine emergencies (job loss, medical, urgent repair).

TIPS FOR CUTTING EXPENSES:
- Cook at home more often.
- Compare prices before purchases (use BankBazaar, Paisabazaar for financial products).
- Cancel unused subscriptions.
- Use public transport when possible.
        """.strip(),
    },
    {
        "id": "budget_002",
        "title": "Zero-Based Budgeting and Envelope Method",
        "category": "budgeting",
        "language": "en",
        "source": "RBI Financial Education",
        "content": """
ZERO-BASED BUDGETING (ZBB):
Every rupee of income is assigned a job: spending, saving, or investing.
Income - All allocations = Zero (not zero in your account — zero unassigned money)

HOW TO DO ZBB:
1. Start with your monthly take-home income.
2. List every expense category and assign exact amounts.
3. Include savings and investments as budget "expenses."
4. If income > total allocations: assign the surplus to savings/debt repayment.
5. If allocations > income: reduce discretionary spending until balanced.

ENVELOPE METHOD (Cash-Based):
1. Create labeled envelopes for each spending category (Groceries, Transport, Entertainment).
2. Put the budgeted cash into each envelope at the start of the month.
3. Spend only from the relevant envelope.
4. When the envelope is empty, stop spending in that category.
5. Digital version: use separate bank accounts or wallet categories.

DEBT REPAYMENT STRATEGIES:
- AVALANCHE METHOD: Pay minimums on all debts; put extra money on highest-interest debt first.
  (Mathematically optimal — saves most interest)
- SNOWBALL METHOD: Pay minimums on all; put extra on smallest debt first.
  (Psychologically motivating — quick wins)

FINANCIAL GOALS FRAMEWORK (SMART Goals):
- Specific: "Save ₹1,00,000 for a laptop."
- Measurable: "Save ₹8,333/month for 12 months."
- Achievable: Based on current income and expenses.
- Relevant: Aligned with life priorities.
- Time-bound: "Within 12 months."
        """.strip(),
    },
    # ── Personal Finance Management ─────────────────────────────────
    {
        "id": "pf_001",
        "title": "Investment Options for Beginners in India",
        "category": "personal_finance",
        "language": "en",
        "source": "SEBI Investor Education",
        "content": """
INVESTMENT OPTIONS FOR BEGINNERS (low-to-high risk):

LOW RISK:
1. Public Provident Fund (PPF): ~7.1% PA, tax-free, government-backed. 15-year tenure.
2. Fixed Deposits (FD): 6.5–9.5% PA, capital guaranteed, insured up to ₹5 lakh.
3. Sukanya Samriddhi Yojana: ~8.2% PA, for girl child's education/marriage.
4. National Pension System (NPS): Market-linked, tax benefits under Section 80C and 80CCD.

MEDIUM RISK:
5. Debt Mutual Funds: Invest in bonds/government securities. Returns 6–9% PA typically.
6. Balanced/Hybrid Mutual Funds: Mix of equity and debt. Returns 8–12% PA historically.

HIGHER RISK (higher potential returns):
7. Equity Mutual Funds (SIP): Invest in stock markets via systematic investment plan.
   Historical long-term return: 12–15% PA over 10+ years. NOT guaranteed.
8. Direct Stock Investment: Requires knowledge and research. High risk/reward.

BEGINNER TIPS:
- Start with SIP (Systematic Investment Plan) in a mutual fund: as low as ₹100/month.
- Use SEBI-registered platforms: Zerodha, Groww, ET Money, Paytm Money.
- Diversify across asset classes — don't put all savings in one place.
- Invest for the long term (5–10+ years) for wealth creation.
- Understand that past performance does not guarantee future returns.

NEVER INVEST IN:
- Ponzi schemes promising guaranteed 2%/day or 30%/month returns.
- Unregistered investment advisors or apps not regulated by SEBI/RBI.
        """.strip(),
    },
    {
        "id": "pf_002",
        "title": "Credit Score — What It Is and How to Improve It",
        "category": "personal_finance",
        "language": "en",
        "source": "CIBIL / TransUnion",
        "content": """
WHAT IS A CREDIT SCORE?
A credit score is a 3-digit number (300–900) that represents your creditworthiness.
In India, CIBIL Score (by TransUnion CIBIL) is the most widely used.

SCORE RANGES:
- 750–900: Excellent — easiest loan approval, best interest rates.
- 700–749: Good — loan approval likely with reasonable rates.
- 650–699: Fair — may get loans but at higher interest rates.
- 600–649: Poor — difficult to get credit.
- 300–599: Very Poor — most applications rejected.

WHAT AFFECTS YOUR SCORE:
1. Payment History (35%): Pay EMIs and credit card bills on time.
2. Credit Utilization (30%): Use less than 30% of your credit card limit.
3. Credit Age (15%): Older accounts improve score — don't close old cards.
4. Credit Mix (10%): Having both secured (home loan) and unsecured (personal loan) credit helps.
5. New Credit Inquiries (10%): Too many loan applications in a short time hurt your score.

HOW TO IMPROVE YOUR CREDIT SCORE:
1. Pay all EMIs and credit card dues on or before the due date.
2. Keep credit card utilization below 30% of the limit.
3. Do not apply for multiple loans simultaneously.
4. Check your CIBIL report annually for errors at: cibil.com (1 free check/year).
5. Maintain long-standing credit accounts in good standing.

FREE CREDIT SCORE CHECK:
- CIBIL: cibil.com
- BankBazaar, PaisaBazaar, Bajaj Finserv apps — free monthly checks.
        """.strip(),
    },
    {
        "id": "pf_003",
        "title": "Income Tax Basics for Salaried Individuals",
        "category": "personal_finance",
        "language": "en",
        "source": "Income Tax Department of India",
        "content": """
INCOME TAX IN INDIA — BASICS:

TAX REGIMES (FY 2024–25):
1. OLD REGIME: Higher tax rates but allows deductions (80C, HRA, LTA, etc.)
2. NEW REGIME (default): Lower tax slabs but most deductions not allowed.

NEW REGIME TAX SLABS (FY 2024–25):
- Up to ₹3,00,000:    Nil
- ₹3,00,001–7,00,000: 5%
- ₹7,00,001–10,00,000: 10%
- ₹10,00,001–12,00,000: 15%
- ₹12,00,001–15,00,000: 20%
- Above ₹15,00,000:   30%
- Rebate u/s 87A: No tax if total income ≤ ₹7,00,000 in new regime.

KEY DEDUCTIONS (OLD REGIME):
- Section 80C: Up to ₹1,50,000 (PPF, ELSS, LIC, EPF, home loan principal)
- Section 80D: Health insurance premium (₹25,000 self, ₹25,000 parents)
- HRA: House Rent Allowance exemption
- Standard Deduction: ₹50,000 for salaried employees

HOW TO FILE ITR:
1. Visit: incometax.gov.in
2. Login with PAN and Aadhaar.
3. Choose correct ITR form (ITR-1 for most salaried employees).
4. Pre-filled data from Form 16 / AIS — verify and submit.
5. Deadline: July 31 each year for salaried individuals.

IMPORTANT: Filing ITR on time avoids penalties and helps build credit history.
        """.strip(),
    },
    {
        "id": "pf_004",
        "title": "Insurance — Types and Why You Need It",
        "category": "personal_finance",
        "language": "en",
        "source": "IRDAI",
        "content": """
INSURANCE PROTECTS you and your family from financial shocks due to death,
illness, accidents, or property damage.

TYPES OF INSURANCE:

1. TERM LIFE INSURANCE (Most Important):
   - Pays a lump sum to your family if you die during the policy term.
   - Pure protection — no maturity benefit.
   - Cheapest form: ₹1 crore cover for ~₹6,000–10,000/year for a 30-year-old.
   - Recommended: Cover = 10–15× your annual income.

2. HEALTH INSURANCE:
   - Covers hospitalization, surgery, and medical expenses.
   - Minimum recommended: ₹5–10 lakh family floater.
   - Cashless treatment at network hospitals.
   - Buy early when healthy — premiums are lower and conditions are not pre-existing.

3. VEHICLE INSURANCE:
   - Third-party: Mandatory by law for all vehicles.
   - Comprehensive: Covers own damage + third party.

4. HOME INSURANCE:
   - Covers structure and/or contents against fire, flood, theft, etc.
   - Often underutilized in India — recommended for homeowners.

RED FLAGS IN INSURANCE:
- ULIPs (Unit Linked Insurance Plans) sold as investment + insurance — usually poor returns.
- Endowment / money-back policies — low returns (4–6% PA), not recommended for investment.
- Always buy insurance from IRDAI-registered companies only.
- Check insurer's claim settlement ratio at irdai.gov.in before buying.

FREE GOVERNMENT SCHEMES:
- Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY): ₹2 lakh life cover @ ₹436/year.
- Pradhan Mantri Suraksha Bima Yojana (PMSBY): ₹2 lakh accident cover @ ₹20/year.
        """.strip(),
    },
    # ── Government Schemes ──────────────────────────────────────────
    {
        "id": "gov_001",
        "title": "Key Government Financial Schemes for Citizens",
        "category": "government_schemes",
        "language": "en",
        "source": "Government of India — india.gov.in",
        "content": """
MAJOR GOVERNMENT FINANCIAL SCHEMES:

1. JAN DHAN YOJANA (PMJDY):
   Zero-balance bank account for all Indians.
   Benefits: ₹2 lakh accident insurance, ₹10,000 overdraft, RuPay debit card.
   Apply: At any public sector bank.

2. ATAL PENSION YOJANA (APY):
   Pension scheme for unorganized sector workers (18–40 years).
   Guaranteed monthly pension of ₹1,000–5,000 from age 60.
   Government contributes 50% of subscription (for eligible enrollees).

3. MUDRA LOAN (PMMY):
   Loans up to ₹10 lakh for micro/small businesses without collateral.
   Three categories: Shishu (up to ₹50,000), Kishore (₹50K–₹5L), Tarun (₹5L–₹10L).
   Apply: Through banks, MFIs, or udyamimitra.in

4. PM SVANidhi:
   Micro-credit for street vendors — ₹10,000 to ₹50,000.
   Collateral-free, digital transactions give subsidy.

5. STAND-UP INDIA:
   Loans ₹10 lakh – ₹1 crore for SC/ST and women entrepreneurs.

6. SUKANYA SAMRIDDHI YOJANA:
   For girl children below 10 years. 8.2% interest PA, tax-free.
   Minimum ₹250/year, maximum ₹1.5 lakh/year. Matures at girl's age 21.

DIGITAL PAYMENT GOVERNMENT INITIATIVES:
- BHIM App: Government's own UPI app, free to use.
- DigiLocker: Store/access official documents digitally.
- Aadhaar-enabled Payment System (AePS): Withdraw cash at business correspondents
  using Aadhaar biometrics — useful in rural areas without ATMs.
        """.strip(),
    },
]
