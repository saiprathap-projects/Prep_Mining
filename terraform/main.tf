provider "aws" {
  region = var.region
}
resource "aws_ecr_repository" "prep_mining_app" {
  name = var.repository_name
}
resource "aws_ecr_repository" "prep_mining_nginx" {
  name = var.repository_name_1
}
resource "aws_ecr_repository" "mysql" {
  name = var.repository_name_2
}