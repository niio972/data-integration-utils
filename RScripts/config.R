
#' Automatic loading package
#'
#' @param packages.list list of packages
#'
#' @return
#' @export
#'
#' @examples  loadPackages(c("tidyr","ggplot"))
loadPackages <- function(packages.list){
  new.packages <- packages.list[!(packages.list %in% installed.packages()[,"Package"])]
  if(length(new.packages)) install.packages(new.packages)
  lapply(new.packages, require, character.only=T)
}