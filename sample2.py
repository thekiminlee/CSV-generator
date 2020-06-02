import pyDataGenerator as dg
import pandas as pd
import random
import math
import datetime
import xml.etree.ElementTree as ET

# reading from xml
tree = ET.parse('processors2.xml')
root = tree.getroot()

processor_map = {
    1:"A", 2:"B", 3:"C"
}

class Processor:
    def __init__(self, c, n):
        self.country = c
        self.name = n
        self.profit = 0
        self.average_rating = 0
        self.satisfactory_score = 0
        self.profit_score = 0
        self.final_score = 0
        self.fx_margin = 0
        self.revenue_share = 0
        self.percent_rate = 0
        self.flat_rate = 0
    def calc_finalscore(self, pw, sw):
        self.final_score = self.profit_score * pw + self.satisfactory_score * sw
    def calc_revenue(self, amount:float, isFx:bool):
        return self.fx_margin * amount * self.revenue_share if isFx else 0.0
    def calc_cost(self, amount):
        return amount * self.percent_rate + self.flat_rate
    def calc_profit(self, amount, isFx):
        self.profit = self.calc_revenue(amount, isFx) - self.calc_cost(amount)
        return self.profit


def elementToProcessor(processor, country, pname):
    p = Processor(country, pname)
    p.flat_rate = float(processor.find("flat_rate").text)
    p.percent_rate = float(processor.find("percent_rate").text.strip("%"))/100
    p.revenue_share = float(processor.find("revenue_share").text.strip("%"))/100
    p.fx_margin = float(processor.find("fx_margin").text.strip("%"))/100
    p.average_rating = float(processor.find("average_rating").text)
    return p

def setup():
    countries = root.getchildren()
    info = {}
    for country in countries:
        processors = country.getchildren()[0]
        for processor in processors:
            #to get rid of the placeholder a in front of each country code
            tag = int(country.tag[1:])
            if(tag not in info):
                info[tag] = {}
            info[tag][processor.tag] = elementToProcessor(processor, tag, processor.tag)
    return info

info = setup()
#---------------------------------------------------------

def encode(x):
    y = x.encode('utf-8')
    num = int.from_bytes(y, byteorder='big')
    return num

def generateID(rng):
    alp = ['A', 'B', 'C']
    id = ''
    result = []

    for j in range(rng):
        for i in range(5):
            id += alp[random.randint(0, len(alp)-1)]
        result.append(encode(id))
        id = ''

    return result

def generateEndDate():
    date = '2019-0{month}-{day}T12:00:00Z'.format(month=[3,3,3,4][random.randint(0,3)], day=random.randint(10,15))
    return date

def endDates(rng):
    result = []
    for i in range(rng):
        result.append(generateEndDate())
    return result

# Configuration
dg.ATTR_NAME = [
    # Processor
    'processor',
    # Transaction info
    'amount',
    'original_currency',
    'target_currency',
    'fx',
    'transaction_status',
    'transaction_start_date',
    'transaction_end_date',
    'duration',
    'transaction_profit',
    # User Info
    'pyr_id',
    'pye_id',
    'ppid',
    'country',
    'payee_satisfaction',
    'payor_satisfaction',
    'overall_satisfaction'
]
dg.ATTR_RANGE = [
    # Processor
    [1, 2, 3],

    # Transaction info
    (100.00, 5000.00),  # amount
    [410, 156, 840, 978, 986, 484, 356],  # original_currency
    [410, 156, 840, 978, 986, 484, 356],  # target_currency
    [0],  # fx (placeholder value. Will reflect currency status in preprocessing)
    [1, 1, 1, 1, 0],  # txn status
    ['2019-03-06T01:00:00Z', '2019-03-07T15:00:00Z', '2019-03-02T19:00:00Z', '2019-03-03T00:00:00Z', '2019-03-03T12:00:00Z'],  # txn start date
    endDates(50), # txn end date
    [0],
    [0],  # txn profit

    # Payor info
    generateID(100),  # payor id (243 variations)
    generateID(100), # payee id
    generateID(50), # ppid
    [410, 156, 840, 250, 76, 276, 484, 356],  # country
    # payee_rating (placeholder value. Will reflect overall data in preprocessing)
    [0],
    [0],
    [0]
    # overall_rating (placeholder value. Will reflect overall data in preprocessing)
    # ,[0]
]
dg.FILE = "test.csv"
dg.DECIMAL = 2

# Generation
dg.generate(5000)

def convertTime(start, end):
    starttime = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    endtime = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    diff = endtime.date() - starttime.date()
    return diff.days

# Data preprocessing
print("Processing data...")

data = pd.read_csv(dg.FILE)

rate_conversion = {1: 4, 2: 3, 3: 2, 4: 1}
max_profit = {}
mean_rating = {}

for i in range(0, len(data)):
    # Getting transaction profit and initialize mean_rating dict
    country = data.loc[i, 'country']
    processor = processor_map[data.loc[i, 'processor']]
    amount = data.loc[i, 'amount']
    if data.loc[i, 'original_currency'] != data.loc[i, 'target_currency']:
        data.loc[i, 'fx'] = 1
    data.loc[i, 'transaction_profit'] = info[country][processor].calc_profit(amount, data.loc[i, 'fx'])
    if(country not in max_profit):
        max_profit[country] = {}
        mean_rating[country] = {}
    if(processor not in max_profit[country]):
        max_profit[country][processor] = data.loc[i, 'transaction_profit']
        mean_rating[country][processor] = []

    max_profit[country][processor] = max(max_profit[country][processor], data.loc[i, 'transaction_profit'])

for i in range(0, len(data)):
    # calculating payee rating value
    country = data.loc[i, 'country']
    processor = processor_map[data.loc[i, 'processor']]
    random_bias = [0.41, 1, 0.25, -0.3]
    rating = 0
    rating += (data.loc[:, 'transaction_profit'][i] * 4.00) / max_profit[country][processor] * 0.8
    rating += random_bias[random.randint(0, 3)]
    duration = convertTime(data.loc[:, 'transaction_start_date'][i], data.loc[:, 'transaction_end_date'][i]) * 0.6
    data.loc[:, 'duration'][i] = duration
    rating += (duration * 4.00)/90.00
    rating += random_bias[random.randint(0, 3)]
    rating /= 2.00

    #appends the rating for this transactions to list; 5 should be the maximum rating possible.
    mean_rating[country][processor].append(5-rating)

    if(rating <= 3.00) and (data.loc[:, 'transaction_status'][i] == 0):
        rating += 1.00
    if(rating > 4.00):
        rating = 3.99
    elif(rating < 0):
        rating = 0.1

    rating = rate_conversion[math.ceil(rating)]
    if(rating in (3, 4)):
        data.loc[:, 'payee_satisfaction'][i] = 1
        data.loc[:, 'overall_satisfaction'][i] = [1,1,1,1,1,0][random.randint(0,5)]
    else:
        data.loc[:, 'payee_satisfaction'][i] = 0
        data.loc[:, 'overall_satisfaction'][i] = [1,1,0][random.randint(0,2)]

    payor_option = [1,0]
    if data.loc[:, 'payee_satisfaction'][i] == 1:
        payor_option += [1,1]
    if duration < 40:
        payor_option += [1]
    else:
        payor_option += [0]
    data.loc[:, 'payor_satisfaction'][i] = payor_option[random.randint(0,len(payor_option)-1)]

    overall_option = [1,0]
    if data.loc[:, 'payor_satisfaction'][i] + data.loc[:, 'payee_satisfaction'][i] == 2:
        overall_option += [1,1,1]
    elif data.loc[:, 'payor_satisfaction'][i] + data.loc[:, 'payee_satisfaction'][i] == 1:
        overall_option += [1]
    else:
        overall_option += [0, 0]

    if data.loc[i, 'fx'] == 1 and data.loc[i, 'transaction_profit'] > 0:
        overall_option += [1]
    else:
        overall_option += [0]
    data.loc[:, 'overall_satisfaction'][i] = overall_option[random.randint(0, len(overall_option)-1)]


#prints out the mean rating for populating the xml for later use in the non-ml program
def update_average_rating(file):
    for c in mean_rating.keys():
        for p in mean_rating[c].keys():
            l = mean_rating[c][p]
            mean = sum(l)/len(l)
            #print(c, p, mean)
            root.find("a"+str(c)).getchildren()[0].find(p).find("average_rating").text = str(round(mean,3))
    tree.write(file)

update_average_rating("updated.xml")
data.to_csv(dg.FILE)


print("Process complete")

