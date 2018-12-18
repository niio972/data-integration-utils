print(getwd())
source("RScripts/config.R")
loadPackages(c("drake","dplyr","readxl"))

document = "/home/charlero/PROJETS/BigDataGrappes/Données vinif/"

plan <- drake_plan(
  raw_data = readxl::read_excel( file_in(document + 'Base de données vin blanc 20162017 Information.xlsx'))
  data =raw_data %>%
        mutate(if (a == 2 | a == 5 | a == 7 | (a == 1 & b == 4)){g = 2})
)

plan
config <- drake_config(plan)

make(plan)
readd(raw_data)
