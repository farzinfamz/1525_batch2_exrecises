library(readxl)
df1 <- read_excel('SaleData.xlsx')
df2 <- read.csv('imdb.csv')
df3 <- read.csv('diamonds.csv')
df4 <- read.csv('movie_metadata.csv')


# Q1 Find least sales amount for each item
least_sales <- function(df1){
  
  least_sale <- df1%>% group_by(Item)
  ls <- least_sale %>% filter(Sale_amt==min(Sale_amt)) 
  return (ls[c('Item','Sale_amt')])
}

# Q2 compute total sales at each year X region

sales_year_region <-function(df1){
  
  year <- function (x){
    return(lubridate::year(x))
  }
  df1['year'] <- lapply(df1['OrderDate'], year)
  
  
  total_sales <- df1 %>% group_by(year,Region)
  
  return (total_sales %>% summarize(Total_sale=sum(Sale_amt)))
  
}

# Q3 append column with no of days difference from present date to each order date
days_diff <- function (df1){
  
  today <- Sys.Date()
  
  date_diff <- function(x){
    return (today - as.Date(x))
  }
  
  df1['days_diff'] <- lapply(df1['OrderDate'], date_diff)
  return (df1)
  
}

days_diff(df1)

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
mgr_slsmn <- function(df1){
  
  v1 <- df1 %>% select(Manager) %>% distinct() 
  new_df=data.frame(manager=v1)
  
  list_managers <- new_df$Manager
  list_salesman <- list()
  
  team <- function(x){
    
    dfls <- df1 %>% filter( df1['Manager']==x)
    return(unique(dfls$SalesMan))
  } 
  
  for (i in 1:length(list_managers)){
    list_salesman[[i]] <- team(list_managers[i])
  }
  
  
  
  
  df <- data.frame(manager = v1)
  df$salesman <- list_salesman
  
  return (df)
}

# Q5 For all regions find number of salesman and number of units
slsmn_units <- function (df1){
  v1 <- unique(df1['Region'])
  slsm_unit <- data.frame(Region=v1)
  
  sls_no <- function(x){
    dfls <- df1 %>% filter( df1['Region']==x)
    return(length(unique(dfls$SalesMan)))
  }
  
  v2 <- vector()
  
  region <- slsm_unit$Region
  
  for(i in 1:length(region)){
    v2[i]=sls_no(region[i])
  }
  
  slsm_unit$Number_of_Salesman=v2
  
  
  sls_totalsale <- function(x){
    dfls <- df1 %>% filter( df1['Region']==x)
    return(sum(dfls$Sale_amt))
  }
  
  v3 <- vector()
  
  region <- slsm_unit$Region
  
  for(i in 1:length(region)){
    v2[i]=sls_totalsale(region[i])
  }
  
  
  slsm_unit['TotalSale'] <- v2
  
  return (slsm_unit)
  
  
}
slsmn_units(df1)

# Q6 Find total sales as percentage for each manager
sales_pct <- function (df1){
  v1 <- df1 %>% select(Manager) %>% distinct() 
  new_df=data.frame(manager=v1)
  
  Percentage_sale <- function(x){
    dfls <- df1 %>% filter( df1['Manager']==x)
    return(sum(dfls$Sale_amt)/sum(df1$Sale_amt))
  }
  
  
  
  v2 <- vector()
  
  
  
  for(i in 1:length(region)){
    v2[i]=Percentage_sale(region[i])
  }
  
  new_df$PercentageSale <- v2 
  return (new_df)
}

#Q7 get imdb rating for fifth movie of dataframe
fifth_movie <- function(df2){
  df2 <- read.csv('imdb.csv')
  return (df2$imdbRating[5])
  
}
# Q8 return titles of movies with shortest and longest run time
movies <- function(df2){
  df2 <- df2[!is.na(df2$duration),]
  df2_max_duration <- df2 %>% filter(duration==max(df2$duration))
  a <-df2_min_duration['title']
  
  df2_min_duration <- df2 %>% filter(duration==min(df2$duration))
  b <- df2_min_duration['title']
  return (a)
}

#Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
sort_df <- function(df2){
  df2_new <- order(df2['year'],-df2['imdbRating'])
  return (df2_new)
}
subset_df <- function(df4){
  df4_duartion <- df4 %>% filter((duration >= 30 && duration <= 180) && (gross >2000000) && (budget <1000000))
  return (df4_duartion)
}

subset_df(df4)

# Q11 count the duplicate rows of diamonds DataFrame.
dupl_rows <- function(df3){
  return (sum(duplicated(df3)))
  
}
# Q12 droping those rows where any value in a row is missing in carat and cut columns
drop_row <- function (df3){
  df3 %>% na.omit(carat,cut)
  return (df3)
}

# Q13 subset only numeric columns
sub_numeric <- function (df3){
  df3['z'] <- lapply(df3['z'],as.numeric)
  df3 <- df3[,sapply(df3,is.numeric)]
  return (df3)
}

# Q14 compute volume as (x*y*z) when depth > 60 else 8
volume <- function(df){
  vol <- function(x,y,z,d){
    if(d<8){
      return(8)
    }else{
      return(x*y*z)
    }
  }
  #df3['Volume'] <- lapply(c(df3['x'],df3['y'],df3['z'],df3['depth']),vol())
  #df3['Volume'] <- lapply(c(df3[,1],df3),vol)
  
  v2 <- vector()
  for(i in 1:nrow(df3)){
    v2[i] <- vol(df3$x[i],df3$y[i],df3$z[i],df3$depth[i])
  }
  
  df3$Volume <- v2
  
  return(df3)
  
}

# Q15 impute missing price values with mean
impute <- function(df3){
  df3$price[is.na(df3$price)] <- mean(df3$price)
  return(df3)
}

