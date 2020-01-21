import pandas as pd
import numpy as np
df1=pd.read_excel('SaleData.xlsx')
df2=pd.read_csv('imdb.csv',escapechar='\\')
df3=pd.read_csv('diamonds.csv')
df4=df3=pd.read_csv('movie_metadata.csv')

# Q1 Find least sales amount for each item
def least_sales(df1):
    ls=least_sale=df1.groupby('Item').Sale_amt.min().reset_index()
    return ls

# Q2 compute total sales at each year X region
def sales_year_region(df1):
    def year(x):
        return x.year
    df1['year']=df1['OrderDate'].apply(year)
    order_by_year=df1.groupby(['year','Region']).Sale_amt.sum().reset_index()
    return order_by_year
# Q3 append column with no of days difference from present date to each order date
def days_diff(df1):
    def datediff(x):
        from datetime import date 
        return date.today()-x.date()
    df1['days_diff']=df1['OrderDate'].apply(datediff)
    df1.drop(['year'],inplace=True,axis=1)
    return df
# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df1):
    def team(x):
         return df1[df1['Manager']==x]['SalesMan'].unique()
    new_dataframe=pd.DataFrame({'Manager':df1['Manager'].unique()})
    team_dataframe=pd.DataFrame({'Manager':df1['Manager'].unique(),'List of Salesman':list(map(team,df1['Manager'].unique().tolist()))})
    return team_dataframe

# Q5 For all regions find number of salesman and number of units
def slsmn_units(df1):
    def sales_count(x):
         return len(df1[df1['Region']==x]['SalesMan'].unique().tolist())
    def sales_amount(x):
         return df1[df1['Region']==x]['Sale_amt'].sum()
    slsmn_unit=pd.DataFrame({'Region':df1['Region'].unique(),'Number of SalesMan':list(map(sales_count,df1['Region'].unique().tolist())) ,'totalsales':
                        list(map(sales_amount,df1['Region'].unique().tolist()))})
    return slsmn_unit
# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    # write code to return pandas dataframe
    def sales_percentage(x):
        return (df1[df1['Manager']==x]['Sale_amt'].sum()/df1['Sale_amt'].sum())*100
    q10=pd.DataFrame({'Manager':df1['Manager'].unique(),'PercentageSales':list(map(sales_percentage,df1['Manager'].unique().tolist()))})
    return q10

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
    return df2.iloc[4:5].imdbRating 
# Q8 return titles of movies with shortest and longest run time
def movies(df):
    a=df2[df2['duration']==df2['duration'].max()]['title']
    b=df2[df2['duration']==df2['duration'].min()]['title']
    return list([a,b])

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
    df2.sort_values(['year','imdbRating'],inplace=True,ascending=[True,False])
    return df2
# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
    dff=df4[(((df4['duration'] >=30) & (df4['duration']<=180)) & (df4['gross'] > 2000000) & (df4['budget']<1000000))]
    #dff=df4[((df2['duration'] >=30) & (df4['duration']<=180))]
    return dff
# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
    duplicate_rows=df3.shape[0]-df3.drop_duplicates().shape[0] 
    return duplicate_rows
# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
    df3.dropna(subset=['cut','color'],inplace=True)
    return df3
# Q13 subset only numeric columns
def sub_numeric(df):
    df3['z'] = pd.to_numeric(df3['z'],errors='coerce')
    df3._get_numeric_data()
    return df3
# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
    def vol(depth,x,y,z):
        if depth <8:
            return 8
        else :
            return x*y*z
    df3['volume']=sub_numeric(df3).apply(lambda x:vol(x.depth,x.x,x.y,x.z),axis=1)
    return df3
# Q15 impute missing price values with mean
def impute(df):
        df3['price']=df3['price'].fillna(value=df3['price'].mean(),inplace=True)
        return df3

#Optional Question 1 Generating the Genre Combinations

def Genere_Combination_report(df):
    ff=df2.groupby(['type','year'])# group by type and year
    m=df2.columns.get_loc("Action")# finding  the location from where the indexing begins
    gg=ff[df2.columns[m:]].sum() # summing


    def genre_maker(x):
        a=gg.columns.tolist() # getting the group by columns to a list 
        temp_combo=[]
        x.shape[0]
        for j in range(x.shape[0]):
            if x[j]!=0:
                temp_combo.append(a[j])
        return temp_combo

    genre_combo=[]
    for i in range(gg.shape[0]):
        x=gg.iloc[i].apply(np.array).values # the row vales
        y=genre_maker(x)
        genre_combo.append(y)

    
#f=pd.DataFrame({'series':genre_combo})

# Getting the Index of group by object
    x=pd.DataFrame(gg.index)
    dfObj=pd.DataFrame({'type':[i[0] for i in x[0]],'Genre_Combo':genre_combo,'year':[i[1] for i in x[0]]})
    dfObj['avg_rating']=ff.imdbRating.mean().tolist()
    dfObj['min_rating']=ff.imdbRating.min().tolist()
    dfObj['max_rating']=ff.imdbRating.max().tolist()
    dfObj['total_run_time_mins']=ff.duration.sum().tolist()
    
    return dfObj

#Optional Question 2
def movie_length(df):
    df2=pd.read_csv('imdb.csv',escapechar='\\')
    dff= pd.DataFrame({'Year' :df2['year'],'TitleLength':df2['title'].str.len()})
    gg=dff.groupby('Year')
    mat=gg.TitleLength.apply(np.array).values

    arr_25=[0] * mat.shape[0]
    arr_50=[0] * mat.shape[0]
    arr_75=[0] * mat.shape[0]
    arr_min=[0] * mat.shape[0]
    arr_max=[0] * mat.shape[0]
#mat.shape[0]
    for i in range(mat.shape[0]):
        arr_25[i]=np.percentile(mat[i],25)
        arr_75[i]=np.percentile(mat[i],75)
        arr_50[i]=np.percentile(mat[i],50)
        arr_min[i]=mat[i].min()
        arr_max[i]=mat[i].max()

    def fun(x,arr_25,arr_50,arr_75):
            num_75=0
            num_25=0
            num50_75=0
            num25_50=0
            for i in range(x.shape[0]):
        
                if x[i] <= arr_25:
                    num_25=num_25+1
                elif x[i]>arr_25 and x[i]<=arr_50:
                    num25_50 = num25_50+1
                elif x[i]>arr_50 and x[i]<=arr_75:
                    num50_75 = num50_75+1
                else :
                    num_75=num_75+1
    
            return(num_25,num25_50,num50_75,num_75)
    
    count_25=[0] * mat.shape[0]
    count25_50=[0] * mat.shape[0]
    count50_75=[0] * mat.shape[0]
    count_75=[0] * mat.shape[0]
    for i in range(mat.shape[0]):
                   count_25[i],count25_50[i],count50_75[i],count_75[i]=fun(mat[i],arr_25[i],arr_50[i],arr_75[i])
        


    df_fy=pd.DataFrame({'MinimumLength':gg.TitleLength.min(),'Maximum_Length':gg.TitleLength.max()})
    df_fy['num_videos_less_than_25_percentile']=count_25
    df_fy['num_vdieos_25_50percentile']=count25_50
    df_fy['num_videos_50_75percentile']=count50_75
    df_fy['num_videos_greaterthan_75_percentile']=count_75
    return df_fy

#Optional Question 3
def cut_volume(df3):
    dff3=volume(df3)
    t=pd.qcut(dff3['volume'],q=10).tolist()
    dff3['VolumeRange']=t
    gg=dff3.groupby(['VolumeRange','cut']).volume.count()
    percentage = gg.groupby(level=0).apply(lambda x:100 * (x / float(x.sum())))
    ff=percentage.reset_index()

#ff.rename(index = {"Volume": "Volume Percentage"},inplace = True) 
#ff.rename(columns = {'Volume':'TEST'}, inplace = True)
    a=ff.pivot_table(values='volume',index=['VolumeRange'],columns=['cut'])
    return(a)

#Q4 Optional
def quarter_on_quarter(df):
    ff=df4.sort_values(['title_year','gross'],ascending=[False,False])
    cv=ff['title_year'].tolist()
    ind=cv.index(cv[0]-11)
    g=ff[:ind-1]
    a=0.1

    dff = (g.groupby('title_year',group_keys=False,sort=False).apply(lambda x: x.head(int(len(x) * a))).reset_index(drop=True))

        
    gg=dff.groupby('title_year',sort=False)
    gg.imdb_score.mean()
    fk=gg.gross.count()
    fk.index.tolist()

    df_final=pd.DataFrame({'Year':fk.index.tolist(),'Average_imdb_rating':gg.imdb_score.mean().apply(np.array).values,'count':fk.apply(np.array).values})
    return df_final

#Q5 Optional
def decile_duration(df2):
    
    gg=df2.groupby(pd.qcut(df2.duration,10))[df2.columns[16:]].sum() # grouping over decile
    b=gg.iloc[0].apply(np.array).values

    def gen_3_maker(x):
        a=gg.columns.tolist()
        d=[]
        c=c=np.argsort(-x)   
        d.append(a[c[0]])
        d.append(a[c[1]])
        d.append(a[c[2]])

        return d

    b3_genre=[]

    for i in range(gg.shape[0]):
        x=gg.iloc[i].apply(np.array).values # the row vales
        y=gen_3_maker(x)
        b3_genre.append(y)
    

    df_result=pd.DataFrame({'Duration':gg.index.tolist(),'nominations':df2.groupby(pd.qcut(df2.duration,10))['nrOfNominations'].sum().tolist()})
    df_result['wins']=df2.groupby(pd.qcut(df2.duration,10))['nrOfWins'].sum().tolist()
    df_result['count']=df2.groupby(pd.qcut(df2.duration,10))['duration'].count().tolist() 
    df_result['top_3_genres']=b3_genre
    return df_result

