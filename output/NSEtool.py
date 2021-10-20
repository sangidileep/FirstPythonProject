# importing nse from nse tools
import pandas as pd
from nsetools import Nse

# creating a Nse object
nse = Nse()

# printing Nse object
print(nse)
print(nse.__doc__)

# getting quote of the sbin
quote = nse.get_quote('sbin')
print(quote)


# printing company name
print(quote['companyName'])

# printing buy price
print("Buy Price : " + str(quote['buyPrice1']))

# datasbi= pd.DataFrame(quote,index='pricebandupper')
# print(datasbi)
