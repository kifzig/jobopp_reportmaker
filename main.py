from fpdf import FPDF
import pandas as pd
from datetime import date

#This program takes an exported CSV from Salesforce with information about
#current job positions and creates a PDF report to provide to job seekers.
#The report in SF can be tailored to region, subspecialty, or other criteria
#based on the candidate's preferences

# CSV has the following columns:
# Company Name, Job Opportunity Name, City, State, Clinical Subspecialty Client Wants, Complete Job Description

#Recruiter information to print in the footer of the PDF
recruiters = {
    "sample": ("Sample Recruiter", "sample@samplerecruiting.com", "216-216-2162"),
    "kif": ("Kif Francis", "kif@kifzig.com", "216-255-6688"),
    "aaron": ("Aaron Smith", "aaron@kifzig.com", "216-222-8888")
}

#Enter the short key: sample / kif / aaron or add your own

recruiter = input("What is the recruiter's name? ")
recruiter_full_name = recruiters[recruiter][0]
email = recruiters[recruiter][1]
mobile = recruiters[recruiter][2]
today = date.today().strftime("%B %d, %Y")

#Title that will appear at top of document
title="Job Opportunities in the South"

#Reads in csv with the columns: Company Name, Job Opportunity Name, City, State, Clinical Subspecialty Client Wants, Complete Job Description
df = pd.read_csv('import/southern_jobs_from_sf.csv')

class PDF(FPDF):
    def header(self):
        #prints the header image
        self.image('images/summit_recruiting_logo.jpg', 90, 8, 33, link="http://www.google.com")
        self.set_font('Arial', '', 12)
        self.cell(80)
        self.ln(10)
        self.set_text_color(0, 0, 139)
        #prints the title of the report in the header along with today's date
        self.cell(0, 10, title + " - " + today, 1, 0, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        #prints the page number at the bottom of the page
        self.cell(0, 9, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        self.ln(5)
        #prints the footer text with recruiter contact information
        self.cell(0, 10, f'Recruiter: {recruiter_full_name} - Email: {email} - Cell: {mobile}', 0, 0, 'C')

#Creates the instance of the PDF
pdf = PDF()
pdf.alias_nb_pages()

#Creates the Table of Contents page
pdf.add_page()
pdf.set_font('Arial', '', 14)
pdf.ln(5)
pdf.cell(0, 10, "Table of Contents", 0, 1, 'C')
pdf.set_font('Times', '', 12)


#Creates the list for the Table of Contents page(s)
for i, row in df.iterrows():
    pdf.set_x(2)
    city = df.at[i, 'City']
    state = df.at[i, 'State'][0:2]
    pdf.cell(0, 10, "                                                          " + state + " : " + df.at[i, 'Company Name'] + " (" + city + ", " + state + ")", 0, 1)
pdf.add_page(orientation="")


# Prints all the job opportunities that were included in the imported cv
for i, row in df.iterrows():
    pdf.set_font('Times', 'b', 12)
    pdf.cell(0, 10, df.at[i, 'Company Name'], 0, 1, 'C')
    #pdf.set_fill_color(211, 211, 211)
    #pdf.cell(0, 10, df.at[i, 'Job Opportunity Name'], 0, 1, 'C')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, df.at[i, 'City'] + ", " + df.at[i, 'State'][0:3], 0, 1, 'C')
    pdf.multi_cell(0, 5, df.at[i, 'Clinical Subspecialty Client Wants'])
    pdf.ln(5)
    text = df.at[i, 'Complete Job Description']
    text = text.replace("?", "--")
    pdf.multi_cell(0, 5, txt=text)
    pdf.add_page(orientation="")

pdf.output('output/south.pdf', 'F')