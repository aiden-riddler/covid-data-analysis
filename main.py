from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, validators
from wtforms.validators import DataRequired
import re
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'
Bootstrap(app)


class UploadFileForm(FlaskForm):
    excel_file = FileField("Choose Excel File", validators=[DataRequired()])
    submit = SubmitField("Analysis Mode")


@app.route('/', methods=['post', 'get'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        excel_file = request.files['excel_file']
        if re.search(".xlsx$", excel_file.filename):
            print(type(excel_file))
            covid_df = pd.read_excel(excel_file, sheet_name='Form responses 1')
            astra = {
                "First Dose Astraceneca": covid_df['1st Dose Total (Astraceneca)'].sum(),
                "Second Dose Astraceneca": covid_df['2nd Dose Total (Astraceneca)'].sum(),
                "Third Dose Astraceneca": covid_df['Booster Total (Astraceneca)'].sum(),
                "Opened Vials Astraceneca": covid_df['Opened Vials (Astraceneca)'].sum(),
                "Remaining Vials Astraceneca": covid_df['Remaining Vials (Astraceneca)'].sum(),
            }

            moderna = {
                "First Dose Moderna": covid_df['1st Dose Total Moderna'].sum(),
                "Second Dose Moderna": covid_df['2nd Dose Total Moderna'].sum(),
                "Third Dose Moderna": covid_df['Booster Total (Moderna)'].sum(),
                "Opened Vials Moderna": covid_df['Opened Vials  (Moderna)'].sum(),
                "Remaining Vials Moderna": covid_df['Remaining Vials  (Moderna)'].sum(),
            }

            pfizer = {
                "First Dose Pfizer": covid_df['1st Dose Total Pfizer'].sum(),
                "Second Dose Pfizer": covid_df['2nd Dose Total Pfizer'].sum(),
                "Third Dose Pfizer": covid_df['Booster Total Pfizer'].sum(),
                "Opened Vials pfizer": covid_df['Opened Vials (Pfizer)'].sum(),
                "Remaining Vials pfizer": covid_df['Remaining Vials (Pfizer)'].sum(),
            }

            jj = {
                "First Dose JJ": covid_df['Total Vaccinated J&J'].sum(),
                "Second Dose JJ": covid_df['Booster Total (J&J)'].sum(),
                "Opened Vials JJ": covid_df['Opened Vials (J&J)'].sum(),
                "Remaining Vials JJ": covid_df['Remaining Vials (J&J)'].sum(),
            }
            hcw = covid_df['HCW (1st Dose Astraceneca)'].sum() + covid_df['HCW (1st Dose Moderna)'].sum() + covid_df[
                'HCW (1st Dose Pfizer)'].sum() + covid_df['HCW (J&J)'].sum()
            teachers = covid_df['Teachers (1st Dose Astraceneca)'].sum() + covid_df['Teachers (1st Dose Moderna)'].sum() + covid_df[
                'Teachers (1st Dose Pfizer)'].sum() + covid_df['Teachers (J&J)'].sum()
            security = covid_df['Security (1st Dose Astraceneca)'].sum() + covid_df['Security (1st Dose Moderna)'].sum() + covid_df[
                'Security (1st Dose Pfizer)'].sum() + covid_df['Security (J&J)'].sum()
            others = covid_df['Others (1st Dose Astraceneca)'].sum() + covid_df['Others (1st Dose Moderna)'].sum() + covid_df[
                'Others (1st Dose Pfizer)'].sum() + covid_df['Others (J&J)'].sum()

            hcw_2 = covid_df['HCW (2nd Dose Astraceneca)'].sum() + covid_df[' HCW (2nd Dose Moderna)'].sum() + covid_df[
                'HCW (2nd Dose Pfizer)'].sum()
            teachers_2 = covid_df['Teachers (2nd Dose Astraceneca)'].sum() + covid_df['Teachers (2nd Dose Moderna)'].sum() + covid_df[
                'Teachers (2nd Dose Pfizer)'].sum()
            security_2 = covid_df['Security (2nd Dose Astraceneca)'].sum() + covid_df['Security (2nd Dose Moderna)'].sum() + covid_df[
                'Security (2nd Dose Pfizer)'].sum()
            others_2 = covid_df['Others (2nd Dose Astraceneca)'].sum() + covid_df['Others  (2nd Dose Moderna)'].sum() + covid_df[
                'Others (2nd Dose Pfizer)'].sum()

            hcw3 = covid_df['HCW (Booster  Astraceneca)'].sum() + covid_df['HCW (Booster Moderna)'].sum() + covid_df['HCW (Booster Pfizer)'].sum() + covid_df['HCW (Booster J&J)'].sum()
            teachers3 = covid_df['Teachers (Booster  Astraceneca)'].sum() + covid_df['Teachers (Booster Moderna)'].sum() + covid_df['Teachers (Booster Pfizer)'].sum() + covid_df['Teachers (Booster J&J)'].sum()
            security3 = covid_df['Security (Booster  Astraceneca)'].sum() + covid_df['Security (Booster Moderna)'].sum() + covid_df['Security (Booster Pfizer)'].sum() + covid_df['Security (Booster J&J)'].sum()
            others3 = covid_df['Others (Booster  Astraceneca)'].sum() + covid_df['Others (Booster Moderna)'].sum() + covid_df['Others (Booster Pfizer)'].sum() + covid_df['Others (Booster J&J)'].sum()

            occupations = {
                "HCW 1st Dose": hcw,
                "Teachers 1st Dose": teachers,
                "Security 1st Dose": security,
                "Others 1st Dose": others,
                "HCW 2nd Dose": hcw_2,
                "Teachers 2nd Dose": teachers_2,
                "Security 2nd Dose": security_2,
                "Others 2nd Dose": others_2,
                "HCW 3rd Dose": hcw3,
                "Teachers 3rd Dose": teachers3,
                "Security 3rd Dose": security3,
                "Others 3rd Dose": others3
            }

            data = {
                "Astraceneca": astra,
                "Moderna": moderna,
                "Pfizer": pfizer,
                "JJ": jj,
                "Occupations": occupations
            }

            return render_template("index.html", form=form, data=data)

    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
