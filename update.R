city <- read.csv('lastest/city_history.csv',stringsAsFactors = F,encoding="UTF-8")
province <- read.csv('lastest/province_history.csv',stringsAsFactors = F,encoding="UTF-8") 
worldwide <- read.csv('lastest/worldwide_history.csv',stringsAsFactors = F,encoding="UTF-8") 

city = city[,c('date','province','city','confirmed','cured','dead')]
colnames(city) = c('time','province','city','cum_confirm','cum_heal','cum_dead')
city$time = as.Date(city$time,format='%Y-%m-%d')
province = province[,c('date','province','confirmed','cured','dead','suspected')]
colnames(province) = c('time','province','cum_confirm','cum_heal','cum_dead','suspected')
province$time = as.Date(province$time,format='%Y-%m-%d')
worldwide = worldwide[,c('date','country','confirmed','cured','dead')]
colnames(worldwide) = c('time','country','cum_confirm','cum_heal','cum_dead')
worldwide$time = as.Date(worldwide$time,format='%Y-%m-%d')

f_p <- function(province) {
  province = sub("省", "", province)
  province = sub("自治区", "", province)
  province = sub("市", "", province)
  province = sub("特别行政区", "", province)
  province = sub("维吾尔", "", province)
  province = sub("壮族", "", province)
  province = sub("回族", "", province)
  return(province)
}

f_c <- function(city) {
  city <- as.character(city)
  city <- sub("市$", "", city)
  city <- sub("地区$","", city)
  city <- sub("省$","", city)
  city <- sub("特别行政区$","", city)
  city <- sub("土家族","", city)
  city <- sub("蒙古族","", city)
  city <- sub("哈尼族","", city)
  city <- sub("布依族","", city)
  city <- gsub(".族","", city)
  city <- sub("自治","", city)
  city[city == '神农架林区'] = '神农架'
  city[city == '甘孜州'] = '甘孜'
  city[city == '凉山州'] = '凉山'
  return(city)
}

trans <- function(city,f) {
  res <- f(city)
  return(res)
}

f1 <- function(city) {
  city <- as.character(city)
  city[city == '未公布来源'] = '地区待确认'
  city[city == '所属地待确认'] = '地区待确认'
  city[city == '未公布来源'] = '地区待确认'
  city[city == '武汉来京'] = '外地来京'
  city[city == '锡林郭勒盟'] = '锡林郭勒'
  city[city == '伊犁哈萨克州'] = '伊犁'
  city[city == '延边朝州'] = '延边'
  return(city)
}
f2 <- function(city) {
  city <- as.character(city)
  city <- sub("区$", "", city)
  return(city)
}
city$city = trans(city$city,f1)
nn = city$province %in% c('北京市','上海市') #只处理北京上海
city[nn,]$city = trans(city[nn,]$city,f2)

province$province = trans(province$province,f_p)
city$province = trans(city$province,f_p)
city$city = trans(city$city,f_c)

Dataframe_2_S3 <- function(data){
  S3 <- list(
    data = city,
    province = province,
    global = worldwide,
    time = max(data$time) 
  )
  class(S3) <- 'nCov2019History'
  return(S3)
}
b = Dataframe_2_S3(worldwide)
saveRDS(b,'dxy_historical_data.rds') # actually, it is github source data
