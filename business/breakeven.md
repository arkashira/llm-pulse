# breakeven.md  

## 1. Cost per Active User (monthly)

| Cost Component | Assumptions | Monthly Cost / User (USD) |
|----------------|-------------|---------------------------|
| **Compute** – 1‑minute of inference monitoring per 1 k API calls (AWS t3.medium) | 0.5 vCPU hr ≈ $0.009 | **$0.05** |
| **Storage** – 10 KB of time‑series metrics + 5 KB of alert history per user | 15 KB ≈ 0.00002 GB → $0.0005/GB‑mo | **$0.01** |
| **Bandwidth** – 50 KB outbound per user for webhook/email alerts | 0.05 MB ≈ $0.02/GB → $0.001 | **$0.02** |
| **Total Variable Cost** |  | **$0.08 / user / month** |

> Variable cost excludes shared SaaS licences (e.g., monitoring dashboard) that are amortised in the fixed‑cost pool below.

---

## 2. Pricing Tiers  

| Tier | Monthly Price (USD) | Core Features | Included Alerts* |
|------|--------------------|----------------|------------------|
| **Basic** | **$9** | • Real‑time latency & error‑rate charts  <br>• Email webhook for critical degradation  <br>• 5 custom alert rules | Up to 5 |
| **Pro** | **$29** | • Everything in Basic  <br>• Slack & PagerDuty integrations  <br>• 30 custom alert rules  <br>• Model‑drift detection (embedding similarity)  <br>• Historical export (30 days) | Up to 30 |
| **Enterprise** | **$99** | • Everything in Pro  <br>• Unlimited alerts & rules  <br>• Dedicated SLA (99.9 % uptime)  <br>• On‑premise data‑sink option  <br>• Custom ML‑drift models  <br>• Account‑level analytics dashboard | Unlimited |

\*Alert count = distinct rule‑triggered notifications per month.  

Assume average revenue per user (ARPU) weighted by a realistic mix: 40 % Basic, 45 % Pro, 15 % Enterprise  

\[
\text{ARPU}=0.4·9 + 0.45·29 + 0.15·99 = 3.6 + 13.05 + 14.85 ≈ **$31.5**
\]

---

## 3. Customer‑Acquisition Cost (CAC)

| Source | Cost Range (USD) |
|--------|------------------|
| Paid ads (LinkedIn, dev‑forums) | $80 – $120 |
| Content & SEO (white‑paper, webinars) | $40 – $80 |
| Direct sales / outbound (enterprise) | $150 – $250 |

**Adopted CAC for modelling:** **$150** (conservative, enterprise‑heavy mix).

---

## 4. Lifetime Value (LTV)

*Assumptions*  

* Monthly churn = 5 % (average across SaaS B2B tools).  
* Average customer lifespan = 1 / churn ≈ 20 months.  
* Discount factor ignored for short horizon.

\[
\text{LTV} = \text{ARPU} × \text{Lifespan} = 31.5 × 20 ≈ **$630**
\]

---

## 5. Break‑Even Users (Variable‑Cost Model)

Fixed monthly overhead (cloud infra, core team, monitoring SaaS licences, support) = **$5,000**.

Contribution margin per user = Price – Variable Cost  

Weighted contribution = ARPU – $0.08 ≈ **$31.42**  

\[
\text{Break‑even users} = \frac{\text{Fixed Cost}}{\text{Contribution per user}} = \frac{5{,}000}{31.42} ≈ **159 users**
\]

Rounded up → **160 active users** needed to cover all monthly expenses.

---

## 6. Path to $10 K MRR  

Target MRR = $10,000  

Using the same mix (40 % Basic, 45 % Pro, 15 % Enterprise):

| Tier | Users Needed | Monthly Revenue |
|------|--------------|-----------------|
| Basic ($9) | **200** | $1,800 |
| Pro ($29) | **150** | $4,350 |
| Enterprise ($99) | **30** | $2,970 |
| **Total** | **380** | **$9,120** |

Add a small buffer of **30 Basic** users (30 × $9 = $270) → **410 users** → **$9,390**.  

Add **10 Pro** users (10 × $29 = $290) → **$9,680**.  

Add **5 Enterprise** users (5 × $99 = $495) → **$10,175**.

**Resulting composition to surpass $10 K MRR**

| Tier | Users |
|------|-------|
| Basic | 200 |
| Pro   | 160 |
| Enterprise | 35 |
| **Total Users** | **395** |
| **MRR** | **≈ $10,200** |

*Alternative single‑tier routes*  

* All‑Pro: 10,000 / 29 ≈ **345** Pro users.  
* All‑Enterprise: 10,000 / 99 ≈ **102** Enterprise users.

---

### Quick Reference Summary

| Metric | Value |
|--------|-------|
| Variable cost / user | $0.08/mo |
| ARPU (weighted) | $31.5/mo |
| CAC (average) | $150 |
| LTV | $630 |
| Fixed monthly cost | $5,000 |
| Break‑even users | **≈ 160** |
| Users for $10 K MRR (mixed) | **≈ 395** (200 Basic, 160 Pro, 35 Enterprise) |

---  

*All numbers are based on current cloud pricing (AWS US‑East) and market‑average SaaS churn. Adjust as real usage data arrives.*