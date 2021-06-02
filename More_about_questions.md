### Methodology used to clean each question

Most of the questions were not processed by me in any way. I mostly cleaned the freetext ones. Here are the details:

'Q2':'What is your current rank in jiu jitsu?'
- if the person answered that they train in a gi I changed 'no rank' to 'white belt'

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

'Q19':'What is your favorite part about training?'
- created a wordcloud out of the answers
- you can view the raw dataset in the app

'Q20':'What is your least favorite part about training?',
- created a dictionary after cleaning the data

'Q22':'How old were you when you started jiu jitsu?',

'Q23':'Does your instructor encourage students at your gym to compete?',

'Q24':'Have you competed in jiu jitsu before?',

'Q25':'If you have competed, have you won any of the following medals?',

'Q26':'If you have competed, what was the organization (e.g., IBJJF, NAGA, etc.)? Fill in as many as apply!',
- created a dictionary after cleaning the data

'Q27':'Does your gym have a formal curriculum?',

'Q28':'Have you had any serious injuries from doing jiu jitsu (that is, injuries that required weeks or months off or perhaps even surgery?) If so, please list the injuries and very briefly explain how they occurred and how long it took to recover--e.g., ACL tear via heel hook with 9 month recovery.',
- created a dictionary after cleaning the data

'Q30':'Do you cross-train in other martial arts? If so, which one(s)?',

'Q31':'Do you do mobility exercises to prepare your body for jiu jitsu (e.g., ginastica natural)?',

'Q32':'Do you do yoga to prepare your body for jiu jitsu?',

'Q33':'How many gis do you own?',

'Q35':'How many rash guards do you own?',

'Q38':'How many no-gi shorts do you own?',

'Q39':'What are some of your favorite gi manufactures?',
- created a dictionary after cleaning the data

'Q40':'What are some of your favorite rash guard manufacturers?',
- created a dictionary after cleaning the data

'Q41':'What are some of your favorite short manufacturers?',
- created a dictionary after cleaning the data

'Q42':'Do you buy jiu jitsu apparel (e.g., tee shirts, hats, etc.)?',

'Q43':'If you buy apparel, what are some of your favorite brands? If you don't buy apparel, leave blank!',
- created a dictionary after cleaning the data

'Q44':'Have you ever had a problem with a particular manufacturer or brand?  If so, which one(s) and what was the problem?',
- didn't clean the data, there are not that many answers
- you can see the raw answers in the app

'Q47':'How much do you spend per year (on average) on gear and apparel?',

'Q48':'How much do you spend per month for membership dues?',

'Q49':'How much time do you spend per day (on average) reading or watching jiu jitsu-related material?',

'Q50':'If you have some favorite grappling-related websites and blogs, which ones do you like?',

'Q55':'What is your gender?',

'Q56':'What is your education level? Please select the highest degree you've completed.',

'Q57':'What is your age?',
- used that variable to create the 'age_cat' column with age categories (every 5 years, e.g. 20-25, 25-30, ..., 50+)

'Q57.1':'What is your income?',

'Q59':'What is your race/ethnicity?',

'Q60':'Do you watch sport jiu jitsu?',

'Q61':'How would you describe yourself in terms of political ideology?',
- I decided not to visualise that question on purpose

'Q61.1':'If you do watch sport jiu jitsu, what do you watch and where do you watch it? For instance, do you watch PPVs?  If so, which organizations--EBI, Metamoris, Polaris, etc.',
- created a dictionary after cleaning the data

'Q62':'Do you have a favorite jiu jitsu athlete or athletes?',

'Q63':'Who are your favorite athletes (if any)? As always, leave this blank if it doesn't apply to you!',
- created a dictionary after cleaning the data

'Q65':'If you have some favorite grappling-related podcasts, which ones do you like?',
- created a dictionary after cleaning the data

'Q66':'To which academy do you belong? If it is affiliated, what is the affiliation? For instance:  Oceanside BJJ - A Royce Gracie Affiliate',
- created a dictionary after cleaning the data

'Q66.1':'Is your gym "leg lock friendly"?',

'Q67':'Where is your nationality?',
- created a dictionary after cleaning the data
- many people answered listing multiple countried: I kept the original data but used only the first mentioned country in the analysis

'Q67.1':'What is your preferred "style"?',

'Q68':'What is your favorite submission?',
- wrote a dictionary after cleaning the data
- created another variable out of the answers: "Is your favourite technique a choke"
