df <- read.csv('lastest/city.csv',stringsAsFactors = F,encoding="UTF-8")

colnames(df) <-  c('time','province','city','city_confirmed','city_cured','city_dead','city_suspected',
                  'confirmed','suspected','cured','dead','comment')
df$time = as.Date(df$time,format='%Y-%m-%d') 
city <- df[,1:7]
colnames(city) <- c('time','province','city','cum_confirm','cum_heal','cum_dead','suspected')
province <- df[,c(1,2,8:11)]
colnames(province) <- c('time','province','cum_confirm','cum_heal','cum_dead','suspected')

Dataframe_2_S3 <- function(data){
  S3 <- list(
    data = city,
    province = unique(province),
    time = max(data$time) 
  )
  class(S3) <- 'nCov2019History'
  return(S3)
}

b <- Dataframe_2_S3(df)
saveRDS(b,'dxy_historical_data.rds')
