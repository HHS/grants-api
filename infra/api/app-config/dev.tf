module "dev_config" {
  source                          = "./env-config"
  app_name                        = local.app_name
  default_region                  = module.project_config.default_region
  environment                     = "dev"
  has_database                    = local.has_database
  database_instance_count         = 2
  database_enable_http_endpoint   = true
  has_incident_management_service = local.has_incident_management_service
  database_max_capacity           = 16
  database_min_capacity           = 2

  has_opensearch                           = true
  opensearch_multi_az_with_standby_enabled = false
  opensearch_zone_awareness_enabled        = false
  opensearch_dedicated_master_enabled      = false
  opensearch_dedicated_master_count        = 1
  opensearch_dedicated_master_type         = "m6g.large.search"
  opensearch_instance_count                = 1
  opensearch_instance_type                 = "or1.medium.search"
  opensearch_availability_zone_count       = 3

  # Runs, but with everything disabled.
  # See api/src/data_migration/command/load_transform.py for argument specifications.
  load_transform_args = [
    "poetry",
    "run",
    "flask",
    "data-migration",
    "load-transform",
    "--no-load",
    "--no-transform",
    "--no-set-current",
  ]

  service_override_extra_environment_variables = {
  }
}
