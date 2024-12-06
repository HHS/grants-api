import { FeatureFlags } from "src/services/FeatureFlagManager";

// Feature flags should default to false
export const featureFlags: FeatureFlags = {
  // This is for showing the search page as it is being developed and user tested
  // This should be removed when the search page goes live, before May 2024
  hideSearchV0: false,
  searchOff: false,
  opportunityOff: false,
};

// http://localhost:3000/es/opportunity/33?_ff=opportunityOff%3Afalse
