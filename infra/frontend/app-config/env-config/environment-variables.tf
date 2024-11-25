locals {
  # Map from environment variable name to environment variable value
  # This is a map rather than a list so that variables can be easily
  # overridden per environment using terraform's `merge` function
  default_extra_environment_variables = {
    # Example environment variables
    # WORKER_THREADS_COUNT    = 4
    # LOG_LEVEL               = "info"
    # DB_CONNECTION_POOL_SIZE = 5
    NEW_RELIC_ENABLED = null
    NODE_OPTIONS = null
  }

  # Configuration for secrets
  # List of configurations for defining environment variables that pull from SSM parameter
  # store. Configurations are of the format
  # {
  #   ENV_VAR_NAME = {
  #     manage_method     = "generated" # or "manual" for a secret that was created and stored in SSM manually
  #     secret_store_name = "/ssm/param/name"
  #   }
  # }
  secrets = {
    # Sendy API key to pass with requests for sendy subscriber endpoints.
    SENDY_API_KEY = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/sendy-api-key"
    },
    # Sendy API base url for requests to manage subscribers.
    SENDY_API_URL = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/sendy-api-url"
    },
    # Sendy list ID to for requests to manage subscribers to the Simpler Grants distribution list.
    SENDY_LIST_ID = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/sendy-list-id"
    },
    # URL that the frontend uses to make fetch requests to the Grants API.
    API_URL = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/api-url"
    },
    # Token that the frontend uses to authenticate when making Grants API fetch requests.
    API_AUTH_TOKEN = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/api-auth-token"
    },
    NEXT_PUBLIC_GOOGLE_ANALYTICS_ID = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/google-analytics-id"
    },
    NEW_RELIC_APP_NAME = {
      manage_method     = "manual"
      secret_store_name = "/${var.app_name}/${var.environment}/new-relic-app-name"
    },
    NEW_RELIC_LICENSE_KEY = {
      manage_method     = "manual"
      secret_store_name = "new-relic-license-key"
    }
  }
}
