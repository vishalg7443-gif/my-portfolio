from flask import Flask, render_template_string, request

app = Flask(__name__)


def future_value(monthly_contribution: float, annual_return: float, years: int) -> float:
    monthly_rate = annual_return / 12
    months = years * 12
    if monthly_rate == 0:
        return monthly_contribution * months
    return monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)


PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Financial Future Dashboard</title>
<style>
body{font-family:Inter,system-ui,sans-serif;background:#07111f;color:#eaf2ff;margin:0}main{max-width:900px;margin:48px auto;padding:24px}.card{background:#0d1b2d;border:1px solid #20344f;border-radius:18px;padding:20px;margin-top:16px}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}label{display:grid;gap:6px}input{padding:11px;border-radius:10px;border:1px solid #38506f;background:#081521;color:white}button{padding:12px 16px;border:0;border-radius:10px;background:#6ee7c7;font-weight:700;cursor:pointer}.bar{height:18px;background:#17314d;border-radius:999px;overflow:hidden}.bar span{display:block;height:100%;background:#6ee7c7}.stat{font-size:1.6rem;font-weight:800}@media(max-width:640px){.grid{grid-template-columns:1fr}}</style>
</head>
<body><main><h1>Financial Future Dashboard</h1><p>Compare how starting earlier changes long-term compound growth.</p>
<form class="card" method="post"><div class="grid"><label>Monthly contribution<input name="monthly" type="number" min="1" step="1" value="{{ monthly }}"></label><label>Annual return (%)<input name="rate" type="number" min="0" max="20" step="0.1" value="{{ rate_pct }}"></label></div><p><button>Calculate</button></p></form>
<div class="grid"><section class="card"><h2>Start at 18</h2><div class="stat">${{ '{:,.0f}'.format(start18) }}</div><p>47 years invested</p><div class="bar"><span style="width:100%"></span></div></section><section class="card"><h2>Start at 28</h2><div class="stat">${{ '{:,.0f}'.format(start28) }}</div><p>37 years invested</p><div class="bar"><span style="width:{{ ratio }}%"></span></div></section></div>
</main></body></html>
"""


@app.route("/", methods=["GET", "POST"])
def dashboard():
    monthly = float(request.form.get("monthly", 100) or 100)
    rate_pct = float(request.form.get("rate", 8) or 8)
    annual_return = rate_pct / 100
    start18 = future_value(monthly, annual_return, 47)
    start28 = future_value(monthly, annual_return, 37)
    ratio = round((start28 / start18) * 100, 1) if start18 else 0
    return render_template_string(
        PAGE,
        monthly=monthly,
        rate_pct=rate_pct,
        start18=start18,
        start28=start28,
        ratio=ratio,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
