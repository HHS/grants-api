const {
  NODE_ENV,
  NEXT_PUBLIC_BASE_PATH,
  USE_SEARCH_MOCK_DATA = "",
  SENDY_API_URL,
  SENDY_API_KEY,
  SENDY_LIST_ID,
  API_URL,
  API_AUTH_TOKEN = "",
  NEXT_PUBLIC_BASE_URL,
  NEXT_PUBLIC_GOOGLE_ANALYTICS_ID = "",
} = process.env;

// home for all interpreted server side environment variables
export const environment: { [key: string]: string } = {
  LEGACY_HOST:
    NODE_ENV === "production"
      ? "https://grants.gov"
      : "https://test.grants.gov",
  NEXT_PUBLIC_BASE_PATH: NEXT_PUBLIC_BASE_PATH ?? "",
  USE_SEARCH_MOCK_DATA,
  SENDY_API_URL: SENDY_API_URL || "",
  SENDY_API_KEY: SENDY_API_KEY || "",
  SENDY_LIST_ID: SENDY_LIST_ID || "",
  API_URL: API_URL || "",
  API_AUTH_TOKEN,
  NEXT_PUBLIC_BASE_URL: NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  NEXT_PUBLIC_GOOGLE_ANALYTICS_ID,
};
