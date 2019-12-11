# Brasilian Jiu Jitsu Survey 2017

I am passionate about BJJ and Natural Language Processing - I found a perfect project to combine both. Data was provided to me in a .csv file. I cleaned it and visualised it. It's available in an interactive dashboard so that everyone can focus on parts they're th emost interested in

Data contains 63 columns and 887 rows.

### Challenges I had / still have to overcome:
- misspellings (and wrong question interpretation: neither Texas or 'Murika are a country :P)
- some missing data
- different names for the same BJJ techniques
- grabbing both academy name and its affiliation and not mixing them up
- lots lots lots of data cleaning

### Smart solutions:
- Levenshtein distance for misspellings
- finding a list of famous athletes / well-known gyms / brands first and then running a check on the column
- using an NLP model (this time it was TextBlob) to find a noun in a sentence 
  e.g. "Elbow tendinitis that I am currently working through." --> "ELBOW" or "ELBOW TENDINITIS"

My favourite quesiton ('Q19':'What is your favorite part about training?') is visualised in a wordcloud (in all belt coulours ^^)
