c <- read.csv('lastest/city.csv',stringsAsFactors = F)

colnames(c) <-  c('time','province','city','city_confirmed','city_cured','city_dead','city_suspected',
           'confirmed','suspected','cured','dead','comment')
c$time = as.Date(c$time,format='%Y-%m-%d') 
Dataframe_2_S3 <- function(data){
  S3 <- list(
    data = data,
    time = max(data$time) 
  )
  class(S3) <- 'nCov2019History'
  return(S3)
}

b <- Dataframe_2_S3(c)
saveRDS(b,'historical_data.rds')
