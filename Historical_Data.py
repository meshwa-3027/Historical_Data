from datetime import datetime
from alice_credentials import login 
import pandas as pd


alice = login() 

instrument = alice.get_instrument_by_symbol("NSE", "NIFTY 50")
from_datetime = datetime(2024,5,1,9,15,0)    # From last & days (yyyy,m,d,H,M,S) (date and timestamp)
to_datetime = datetime(2024,5,31,15,30,0)    # To now
interval = "1"       # ["1", "D"] 
indices = True      # For Getting index data
his_data = alice.get_historical(instrument, from_datetime, to_datetime, interval, indices)
df = pd.DataFrame(his_data) 
print(df)

############################## STORE DATA INTO EXCEL ################################


df.to_excel("historical_data.xlsx",index=False)
print("Data Stored")


############################# RESAMPLE USING EXCHANGE TIME ##########################

# Set the 'exchange_time_stamp' column as the index of the DataFrame
df['exchange_time_stamp'] = pd.to_datetime(df['datetime'])

df.set_index('exchange_time_stamp', inplace=True)

# Resample the DataFrame for a 5-minute interval
resampled_data = df.resample('15T').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
})

# Reset the index to make 'exchange_time_stamp' a regular column
resampled_data.reset_index(inplace=True)

print(resampled_data)

resampled_data.to_excel("resampled_data.xlsx",index = False)
print(" Resample Data stored")
