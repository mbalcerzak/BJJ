# Brasilian Jiu Jitsu Survey 2017

I am passionate about BJJ and Natural Language Processing and I found a perfect project to combine both. Data contains 63 columns and 887 unique answers. I cleaned it and visualised it. It's available in an interactive dashboard so that everyone can focus on parts they're th emost interested in



### Challenges I had / still have to overcome:
- misspellings (or loose question interpretation: I am afraid neither Texas or 'Murika are a country :P)
- some missing data
- different names for the same BJJ techniques
- grabbing both academy name and its affiliation and not mixing them up
- lots lots lots of data cleaning

### Smart solutions:
- Levenshtein distance for misspellings
- finding a list of famous athletes / well-known gyms / brands first and then running a check on the column
- using an NLP model (this time it was TextBlob) to find a noun in a sentence 
  e.g. "Elbow tendinitis that I am currently working through." --> "ELBOW" or "ELBOW TENDINITIS"

My favourite quesiton ('Q19':'What is your favorite part about training?') is visualised in a wordcloud (in BJJ belt colours ^^)


### Directiories and files
**Dctionaries** - contains .py files with dictionaries (feel free to message me if you think the list is incomplete or there is a mistake)
**Functions** - functions I used to process the data with

## Packages used

```python


```
