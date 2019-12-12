# Brasilian Jiu Jitsu Survey 2017

I am passionate about BJJ and Natural Language Processing and I found a perfect project to combine both. Data contains 63 columns and 887 unique answers. I cleaned it and visualised it. It's available in an interactive dashboard so that everyone can focus on parts they're th emost interested in

I visualised my favourite quesiton ('Q19':'What is your favorite part about training?') in a wordcloud (in BJJ belt colours ^^). I think It captures well what we all love about that gentle art

<img  width="1000" height="500" src="https://github.com/mbalcerzak/BJJ/blob/master/BJJ_wordcloud.png">

### Challenges I had to overcome:
- misspellings (or loose question interpretation: I am afraid neither Texas or 'Murika are a country :P)
- some missing data
- different names for the same BJJ techniques
- grabbing both academy name and its affiliation and not mixing them up (it was the same question)
- lots lots lots of data cleaning

### Solutions:
- Levenshtein distance for misspellings
- finding a list of famous athletes / well-known gyms / brands first and creating a base for a dictionary that way
- using an NLP model (this time it was TextBlob) to find a noun in a sentence  
  e.g. "Elbow tendinitis that I am currently working through." --> "ELBOW" or "ELBOW TENDINITIS"

### Directiories and files
- **Dctionaries** - contains .py files with dictionaries (feel free to message me if you think the list is incomplete or there is a mistake)
- **Functions** - functions I used to process the data with

## Packages used

```python


```
### Methodology used to clean each question

'Q2':'What is your current rank in jiu jitsu?',
'Q3':'How long have you been training jiu jitsu?',
'Q6':'How long did it take you to go from white belt to blue belt?',
'Q7':'How long did it take you to go from blue belt to purple belt?',
'Q8':'How long did it take you to go from purple belt to brown belt?',
'Q9':'How long did it take you to go from brown belt to black belt?',
'Q10':'On average, how many times do you train per week?',
'Q11':'Do you train both gi and no-gi?',
'Q12':'Do you prefer training gi or no-gi?',
'Q13':'Does your academy focus on self-defense?',
'Q14':'What is your preferred time to train?',
'Q16':'Do you train at gyms when you travel?',
'Q17':'Did you have a background in another martial art before you started jiu jitsu?  If so, which one(s)?',
'Q18':'Why did you start training jiu jitsu?',
'Q19':'What is your favorite part about training?',
'Q20':'What is your least favorite part about training?',
'Q22':'How old were you when you started jiu jitsu?',
'Q23':'Does your instructor encourage students at your gym to compete?',
'Q24':'Have you competed in jiu jitsu before?',
'Q25':'If you have competed, have you won any of the following medals?',
'Q26':'If you have competed, what was the organization (e.g., IBJJF, NAGA, etc.)? Fill in as many as apply!',
'Q27':'Does your gym have a formal curriculum?',
'Q28':'Have you had any serious injuries from doing jiu jitsu (that is, injuries that required weeks or months off or perhaps even surgery?) If so, please list the injuries and very briefly explain how they occurred and how long it took to recover--e.g., ACL tear via heel hook with 9 month recovery.',
'Q30':'Do you cross-train in other martial arts? If so, which one(s)?',
'Q31':'Do you do mobility exercises to prepare your body for jiu jitsu (e.g., ginastica natural)?',
'Q32':'Do you do yoga to prepare your body for jiu jitsu?',
'Q33':'How many gis do you own?',
'Q35':'How many rash guards do you own?',
'Q38':'How many no-gi shorts do you own?',
'Q39':'What are some of your favorite gi manufactures?',
'Q40':'What are some of your favorite rash guard manufacturers?',
'Q41':'What are some of your favorite short manufacturers?',
'Q42':'Do you buy jiu jitsu apparel (e.g., tee shirts, hats, etc.)?',
'Q43':'If you buy apparel, what are some of your favorite brands? If you don't buy apparel, leave blank!',
'Q44':'Have you ever had a problem with a particular manufacturer or brand?  If so, which one(s) and what was the problem?',
'Q47':'How much do you spend per year (on average) on gear and apparel?',
'Q48':'How much do you spend per month for membership dues?',
'Q49':'How much time do you spend per day (on average) reading or watching jiu jitsu-related material?',
'Q50':'If you have some favorite grappling-related websites and blogs, which ones do you like?',
'Q55':'What is your gender?',
'Q56':'What is your education level? Please select the highest degree you've completed.',
'Q57':'What is your age?',
'Q57.1':'What is your income?',
'Q59':'What is your race/ethnicity?',
'Q60':'Do you watch sport jiu jitsu?',
'Q61':'How would you describe yourself in terms of political ideology?',
'Q61.1':'If you do watch sport jiu jitsu, what do you watch and where do you watch it? For instance, do you watch PPVs?  If so, which organizations--EBI, Metamoris, Polaris, etc.',
'Q62':'Do you have a favorite jiu jitsu athlete or athletes?',
'Q63':'Who are your favorite athletes (if any)? As always, leave this blank if it doesn't apply to you!',
'Q65':'If you have some favorite grappling-related podcasts, which ones do you like?',
'Q66':'To which academy do you belong? If it is affiliated, what is the affiliation? For instance:  Oceanside BJJ - A Royce Gracie Affiliate',
'Q66.1':'Is your gym "leg lock friendly"?',
'Q67':'Where is your nationality?',
'Q67.1':'What is your preferred "style"?',
'Q68':'What is your favorite submission?',
