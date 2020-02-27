city <- read.csv('lastest/city_history.csv',stringsAsFactors = F,encoding="UTF-8")
# date	country	countryCode	province	provinceCode	city	cityCode	confirmed	suspected	cured	dead
province <- read.csv('lastest/province_history.csv',stringsAsFactors = F,encoding="UTF-8") 
# date	country	countryCode	province	provinceCode	city	cityCode	confirmed	suspected	cured	dead
worldwide <- read.csv('lastest/worldwide_history.csv',stringsAsFactors = F,encoding="UTF-8") 
# date	country	countryCode	province	provinceCode	city	cityCode	confirmed	suspected	cured	dead

city = city[,c('date','province','city','confirmed','cured','dead')]
colnames(city) = c('time','province','city','cum_confirm','cum_heal','cum_dead')
city$time = as.Date(city$time,format='%Y-%m-%d')
province = province[,c('date','province','confirmed','cured','dead','suspected')]
colnames(province) = c('time','province','cum_confirm','cum_heal','cum_dead','suspected')
province$time = as.Date(province$time,format='%Y-%m-%d')
worldwide = worldwide[,c('date','country','confirmed','cured','dead')]
colnames(worldwide) = c('time','country','cum_confirm','cum_heal','cum_dead')
worldwide$time = as.Date(worldwide$time,format='%Y-%m-%d')

#spec_city = c('北京市','上海市','重庆市','香港特别行政区','澳门特别行政区','台湾省')

#for (i in spec_city) {
#  city[which(city$province == i ),]$city = i
#}
trans_city <- function(city,f) {
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
city$city = trans_city(city$city,f1)
nn = city$province %in% c('北京市','上海市') #只处理北京上海
city[nn,]$city = trans_city(city[nn,]$city,f2)

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
saveRDS(b,'dxy_historical_data.rds')