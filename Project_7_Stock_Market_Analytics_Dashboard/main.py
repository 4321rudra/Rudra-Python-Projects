import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt
# ============================
# Data Collection : Collecting Data for the provided stocks from yahoo finance
# ============================
def download_data(scrip_list):
    all_scrip_data={}
    for scrip in scrip_list:
        df=yf.download(scrip,period='1y')
        if df.empty:
            print(f"Could Not find Data for {scrip}")
            continue
        all_scrip_data[scrip]=df
    return all_scrip_data
# ============================
# Data Transformation : calculate various technical indicators for each stocks
# ============================
def transform_data(all_scrip_data):
    for scrip,df in all_scrip_data.items():
        df.columns=df.columns.get_level_values(0)
        df['Previous Close']=df['Close'].shift(1)
        df['Price Change']=df['Close']-df['Previous Close']
        df['Daily Return']=df["Close"].pct_change()
        df["SMA 7"]=df["Close"].rolling(7).mean()
        df["SMA 20"]=df["Close"].rolling(20).mean()
        df['SMA 30']=df['Close'].rolling(30).mean()
        df['20D Volatility']=(df['Daily Return'].rolling(20).std())
        df['Normalized Close']=(df['Close']/df['Close'].iloc[0])*100
    return all_scrip_data
# ============================
# Analysis : doing various analysis for all stocks
# ============================

def data_analysis(all_scrip_data):
    for scrip,df in all_scrip_data.items():
        
        print(scrip)
        print(df[['Close','Previous Close','Price Change','Daily Return']].head(10))
        print(f"Days with positive returns : {len(df[df['Daily Return']>0])}" )
        print(f"Days with negative returns : {len(df[df['Daily Return']<0])}" )
        idx=df['Daily Return'].idxmax()
        print(f"Date : {idx.date()}")
        print(f"Price Change : {df.loc[idx]['Price Change']:.2f}")
        print(f"Return : {df.loc[idx]['Daily Return']:.2%}")
        print(df[["Close", "SMA 7"]].head(10))
        idx=df['20D Volatility'].idxmax()
        print(f'Highest Volatility \nDate:{idx} \nVolatility:{df.loc[idx]['20D Volatility']:.2%}')
        idx=df['20D Volatility'].idxmin()
        print(f'Lowest Volatility \nDate:{idx} \nVolatility:{df.loc[idx]['20D Volatility']:.2%}')
        print(f'Average Volatility : {df['20D Volatility'].mean():.2%}')
        print(f'Monthly Average Closing Price : \n{df["Close"].resample("ME").mean().round(2)}')
        print(f'Monthly Highest Closing Price : \n{df["Close"].resample("ME").max().round(2)}')
        print(f'Monthly Trading Volume in Lakh: \n{df["Volume"].resample("ME").mean().div(100000).round(2)}')
        print(f'Weeky Average Closing Price :\n{df['Close'].resample("W").mean().round(2)}')
def build_comparison_df(all_scrip_data):
    comparison_df=pd.DataFrame()
    for scrip,df in all_scrip_data.items():
        comparison_df[scrip]=all_scrip_data[scrip]['Close']
    return comparison_df
def watchlist_analysis(all_scrip_data):
    comparison_df=build_comparison_df(all_scrip_data)
    print("\n=========================\n\tWatchlist Summary\n=========================\n")
    
    summary=[]
    for scrip, df in all_scrip_data.items():
        summary.append({'Stock':scrip,
                       'Average Daily Return':df['Daily Return'].mean(),
                       'Average Volatility':df['20D Volatility'].mean(),
                       'Highest Close':df['Close'].max(),
                       'Lowest Close':df['Close'].min(),
                       'Current Close':df['Close'].iloc[-1],
                       'Total Return':(df['Close'].iloc[-1]/df['Close'].iloc[0]-1),
                       'Highest Volume in Lakh':df['Volume'].max()/100000,
                       'Average Volume in Lakh':df['Volume'].mean()/100000,
                       'Positive Days':(df['Daily Return']>0).sum(),
                       'Negative Days':(df['Daily Return']<0).sum()})
        
    summary_df=pd.DataFrame(summary)
    summary_df=summary_df.sort_values("Total Return",ascending=False,ignore_index=True)
    print(summary_df[['Stock','Total Return','Average Daily Return','Positive Days','Negative Days']])
    print(f"Best performing stock : {summary_df.iloc[0]['Stock'] }\tPerformance :{summary_df.iloc[0]['Total Return']:.2%}")
    print(f"Worst performing stock : {summary_df.iloc[-1]['Stock'] }\tPerformance :{summary_df.iloc[-1]['Total Return']:.2%}")
    idx=summary_df['Average Volatility'].idxmax()
    
    print(f"Most Volatile Stock : {summary_df.iloc[idx]['Stock']}")
    idx=summary_df['Average Volatility'].idxmin()
    print(f"Least Volatile Stock : {summary_df.iloc[idx]['Stock']}")
    corr_matrix=comparison_df.corr()
    print(f"Correlation Matrix :\n{corr_matrix}")
    
    max_corr=-2
    for i in range(len(corr_matrix)):
        for j in range(i+1,len(corr_matrix)):
            if i==j:
                continue
            value=corr_matrix.iloc[i,j]
            if value>max_corr:
                max_corr=value
                pair=(corr_matrix.index[i],corr_matrix.columns[j])
    print(f"Most Correlated Pair : {pair}\tCorrelation : {round(max_corr,3)}")
    min_corr=2
    for i in range(len(corr_matrix)):
        for j in range(i+1,len(corr_matrix)):
            if i==j:
                continue
            value=corr_matrix.iloc[i,j]
            if value<min_corr:
                min_corr=value
                pair=(corr_matrix.index[i],corr_matrix.columns[j])
    print(f"Least Correlated Pair : {pair}\tCorrelation : {round(min_corr,3)}")
    return summary_df
# ============================
# Visualizations 
# ============================
def price_comparison_plot(all_scrip_data):
    """Stock price comparison of stocks"""
    plt.figure(figsize=(12,6))
    for scrip, df in all_scrip_data.items():
        plt.plot(df.index,df['Close'],label=scrip,linewidth=2)
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Closing Price (₹)')
    plt.grid(True)
    plt.title('Stock Price Comparison')
    plt.tight_layout()
    plt.show()
def normalized_visualization(all_scrip_data):
    """Normalized stock comparison of stocks , in this we visualize how the all the stocks if theire start price is 100 , its better for comparison"""
    plt.figure(figsize=(12,6))
    for scrip,df in all_scrip_data.items():
        # normalized=(df['Close']/df['Close'].iloc[0])*100
        plt.plot(df.index,df['Normalized Close'],label=scrip,linewidth=2)
    plt.title('Normalized Stock Performance (Base=100)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.tight_layout()
    plt.legend()
    plt.show()
def sma_visualization(all_scrip_data,stock):
    """Price vs SMA 20 chart visualization"""
    if stock not in all_scrip_data.keys():
        print('Stock data not found!')
        return
    df=all_scrip_data[stock]
    plt.figure(figsize=(12,6))
    plt.plot(df.index,df['Close'],label='Close',color='red',linewidth=2)
    plt.plot(df.index,df['SMA 20'],label='SMA 20',color='blue',linewidth=2)
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price(₹)')
    plt.title('SMA 20 vs Closing Price ')
    plt.tight_layout()
    plt.show()
def total_return_bar(summary_df):
    """Here we visualize , what did the each stock returns after 1 year"""
    plt.figure(figsize=(12,6))
    bars=plt.bar(summary_df['Stock'],summary_df['Total Return']*100)
    for bar in bars:
        x=bar.get_x() +bar.get_width()/2
        if bar.get_height()>=0:
            y=1.02*bar.get_height()
        else:
            y=bar.get_height()-5
        plt.text(x,y,f"{bar.get_height():.2f}%",ha='center',va='bottom')
    plt.xlabel('Stocks')
    plt.ylabel('Total Return (%)')
    plt.title('Total Return Bar Chart ')
    plt.tight_layout()
    plt.grid(True,which='major',axis='y',color='gray',alpha=0.3)
    plt.show()
def return_distribution(all_scrip_data,scrip):
    df=all_scrip_data[scrip]
    plt.hist(df['Daily Return']*100,bins=20,label=scrip,rwidth=0.9)
    plt.legend()
    plt.xlabel('Daily Return (%)')
    plt.grid(axis='y',alpha=0.3)
    plt.title(f'Daily Return Distribution {scrip}')
    plt.ylabel('Number Of Days')
    plt.tight_layout()
    plt.show()
    
def return_vs_volume(all_scrip_data,scrip):
    df=all_scrip_data[scrip]
    plt.scatter(df['Daily Return']*100,df['Volume'],alpha=0.6,marker='*')
    plt.xlabel('Daily Return(%)')
    plt.ylabel('Volume')
    plt.tight_layout()
    plt.grid(axis='y',alpha=0.3)
    plt.title(f'Daily Return vs Volume for {scrip}')
    plt.show()

def heatmap(all_scrip_data):
    comparison_df=build_comparison_df(all_scrip_data)
    plt.figure(figsize=(9,6))
    
    corr_matrix=comparison_df.corr()
    print(corr_matrix)
    
    plt.imshow(corr_matrix,cmap='RdYlGn',filternorm=True)
    
    arr=list(range(len(corr_matrix)))
    plt.xticks(ticks=arr,labels=corr_matrix.columns,rotation=45)
    plt.yticks(ticks=arr,labels=corr_matrix.index)
    plt.title('Correlation Heatmap')
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            plt.text(j,i,corr_matrix.iloc[i,j].round(2),ha='center',va='center',color='white')
    
    plt.colorbar()
    plt.tight_layout()
    plt.show()
# ============================
# Main Program
# ============================
def main():
    scrip_list=['OLAELEC.NS','COHANCE.NS','BSOFT.NS','APOLLO.NS','IDEA.NS','HFCL.NS']
    all_scrip_data=download_data(scrip_list)
    all_scrip_data=transform_data(all_scrip_data)
    data_analysis(all_scrip_data)
    summary_df=watchlist_analysis(all_scrip_data)
    price_comparison_plot(all_scrip_data)
    normalized_visualization(all_scrip_data)
    sma_visualization(all_scrip_data,scrip_list[0])
    total_return_bar(summary_df)

    return_distribution(all_scrip_data,scrip_list[5])
    return_vs_volume(all_scrip_data,scrip_list[5])
    heatmap(all_scrip_data)
if __name__=="__main__":
    main()