from flask import Flask, render_template, request

app = Flask(__name__)

# Probabilities based on given statistics
P_relapase = 1 - (73 / 100)
P_not_relapse = 73 / 100

# Feature probabilities
P_less_than_12_weeks_given_relapse = 0.50
P_less_than_12_weeks_given_not_relapse = 0.50

P_medication_given_relapse = 0.50
P_medication_given_not_relapse = 0.50

P_support_given_relapse = 0.50
P_support_given_not_relapse = 0.50

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        less_than_12_weeks = request.form['less_than_12_weeks'] == 'yes'
        medication = request.form['medication'] == 'yes'
        support = request.form['support'] == 'yes'

        # Calculate probabilities using Naive Bayes
        P_X_given_relapse = (
            (P_less_than_12_weeks_given_relapse if less_than_12_weeks else 1 - P_less_than_12_weeks_given_relapse) *
            (P_medication_given_relapse if medication else 1 - P_medication_given_relapse) *
            (P_support_given_relapse if support else 1 - P_support_given_relapse)
        )

        P_X_given_not_relapse = (
            (P_less_than_12_weeks_given_not_relapse if less_than_12_weeks else 1 - P_less_than_12_weeks_given_not_relapse) *
            (P_medication_given_not_relapse if medication else 1 - P_medication_given_not_relapse) *
            (P_support_given_not_relapse if support else 1 - P_support_given_not_relapse)
        )

        P_relapse_given_X = P_X_given_relapse * P_relapase
        P_not_relapse_given_X = P_X_given_not_relapse * P_not_relapse

        P_total = P_relapse_given_X + P_not_relapse_given_X

        P_relapse_given_X /= P_total
        P_not_relapse_given_X /= P_total

        # Determine risk and asset
        risk_factors = []
        assets = []

        if less_than_12_weeks:
            risk_factors.append("Being sober for less than 12 weeks")
        else:
            assets.append("Being sober for more than 12 weeks")

        if medication:
            assets.append("Being on a medication with an aggressive outreach program")
        else:
            risk_factors.append("Not being on a medication with an aggressive outreach program")

        if support:
            assets.append("Regularly supporting other people in sober networks")
        else:
            risk_factors.append("Not supporting other people in sober networks")

        return render_template(
            'result.html',
            relapse_prob=P_relapse_given_X,
            not_relapse_prob=P_not_relapse_given_X,
            risk_factors=risk_factors,
            assets=assets
        )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
