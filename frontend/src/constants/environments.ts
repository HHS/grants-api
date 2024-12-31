import { stringToBoolean } from "src/utils/generalUtils";

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
  FEATURE_SEARCH_OFF = "false",
  FEATURE_OPPORTUNITY_OFF = "false",
  FEATURE_AUTH_OFF = "true",
  NEXT_BUILD = "false",
  SESSION_SECRET = "",
} = process.env;

// eslint-disable-next-line
console.log("!!! from env", FEATURE_AUTH_OFF);
// console.log("!!! from public env", process.env.NEXT_PUBLIC_FEATURE_AUTH_OFF);÷

export const featureFlags = {
  opportunityOff: stringToBoolean(FEATURE_OPPORTUNITY_OFF),
  searchOff: stringToBoolean(FEATURE_SEARCH_OFF),
  authOff: stringToBoolean(FEATURE_AUTH_OFF),
};

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
  GOOGLE_TAG_MANAGER_ID: "GTM-MV57HMHS",
  FEATURE_OPPORTUNITY_OFF,
  FEATURE_SEARCH_OFF,
  FEATURE_AUTH_OFF,
  NEXT_BUILD,
  SESSION_SECRET,
};
