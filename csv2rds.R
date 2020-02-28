df <- read.csv('dxylastest/city.csv',stringsAsFactors = F,encoding="UTF-8")
#df <- unique(df)
colnames(df) <-  c('time','province','city','city_confirmed','city_cured','city_dead','city_suspected',
                   'confirmed','suspected','cured','dead','comment')
df$time = as.Date(df$time,format='%Y-%m-%d') 
city <- df[,1:7]
colnames(city) <- c('time','province','city','cum_confirm','cum_heal','cum_dead','suspected')
province <- df[,c(1,2,8:11)]
colnames(province) <- c('time','province','cum_confirm','suspected','cum_heal','cum_dead')

a = readRDS('old_city.rds')
b = readRDS('old_prov.rds')
new_city = rbind(a,city)
new_prov = rbind(b,province)

Dataframe_2_S3 <- function(data){
  S3 <- list(
    data = new_city,
    province = new_prov,
    time = max(data$time) 
  )
  class(S3) <- 'nCov2019History'
  return(S3)
}
b = Dataframe_2_S3(df)
saveRDS(b,'dxy_origin_historical_data.rds')
