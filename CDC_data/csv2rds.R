cn <- read.csv('lastest/cdc_cn.csv',stringsAsFactors = F,encoding="UTF-8")
cb <- unique(cn)
cn <- cn[c("date","省份","累计确诊","累计疑似","累计死亡","新增确诊","新增疑似","新增死亡")]
colnames(cn) <- c('time','province','cum_confirm','cum_suspected','cum_dead','add_confirm','add_suspected','add_dead')
cn$time = as.Date(cn$time,format='%Y-%m-%d')

gb <- read.csv('lastest/cdc_gb.csv',stringsAsFactors = F,encoding="UTF-8")
gb <- unique(gb)
gb <- gb[c("date","name_cn","累计确诊","新增确诊")]
colnames(gb) <- c('time','country','cum_confirm','add_confirm')
gb$time = as.Date(gb$time,format='%Y-%m-%d')



Dataframe_2_S3 <- function(data){
  S3 <- list(
    data = cn,
	province = cn,
    global = gb,
    time = max(data$time) 
  )
  class(S3) <- 'nCov2019History'
  return(S3)
}
b = Dataframe_2_S3(cn)
saveRDS(b,'nhc_data.rds')
