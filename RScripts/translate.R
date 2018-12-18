source("RScripts/config.R")
loadPackages(c("readr","dplyr","jsonlite","stringr","yaml"))
library("readr")
library("dplyr")
library("jsonlite")
library("stringr")
library("yaml")


scriptDirectory <- "/home/charlero/PROJETS/BigDataGrappes/Git/data-integration-utils/RScripts"
vocabularyDirectory <- paste0(scriptDirectory , "/vocabulary.yml")
# csvFilesDirectory <- paste0(scriptDirectory , "/example")
csvFilesDirectory <- "/home/charlero/PROJETS/BigDataGrappes/Git/CSVtoTurtle/toParse/csv"
outputPath <- "/home/charlero/PROJETS/BigDataGrappes/Git/data-integration-utils/RScripts/output"
outpuPrefixFile =""

print(getwd())
if(!dir.exists(outputPath)){
  dir.create(outputPath, showWarnings = TRUE, recursive = FALSE, mode = "0777")
}

files <- list.files(path=csvFilesDirectory, pattern="*.csv", full.names=TRUE, recursive=FALSE)
lapply(files, function(file) {
  data <- read_csv(file)
  vocab <- yaml.load_file(vocabularyDirectory)
  for(x in names(vocab)){
    data = data %>%  mutate_all(funs(str_replace(., x,vocab[[x]])))
  }
  filename = basename(file)
  write_csv(data, paste0(outputPath,"/",outpuPrefixFile,filename))
})


# translate <-  function(x){
#   if(x %in% names(vocab)){
#     str_replace(x, x, vocab[[x]])
#   }
# }


