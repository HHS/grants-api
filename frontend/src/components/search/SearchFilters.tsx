"use client";

import clsx from "clsx";

import { useState } from "react";

import ContentDisplayToggle from "src/components/ContentDisplayToggle";
import SearchFilterAccordion, {
  SearchFilterConfiguration,
} from "src/components/search/SearchFilterAccordion/SearchFilterAccordion";
import SearchOpportunityStatus from "src/components/search/SearchOpportunityStatus";

export default function SearchFilters({
  opportunityStatus,
  filterConfigurations,
}: {
  opportunityStatus: Set<string>;
  filterConfigurations: SearchFilterConfiguration[];
}) {
  // all filter options will be displayed on > mobile viewports
  // on mobile, filter options will be hidden by default and can be toggled here
  const [showFilterOptions, setShowFilterOptions] = useState(false);
  const FilterAccordions = filterConfigurations.map(
    ({
      filterOptions,
      query,
      queryParamKey,
      title,
    }: SearchFilterConfiguration) => {
      return (
        <SearchFilterAccordion
          filterOptions={filterOptions}
          query={query}
          queryParamKey={queryParamKey}
          title={title}
          key={title}
        />
      );
    },
  );
  return (
    <>
      <div className="display-flex flex-column flex-align-center tablet:display-none">
        <ContentDisplayToggle
          setToggledContentVisible={setShowFilterOptions}
          toggledContentVisible={showFilterOptions}
          toggleText={showFilterOptions ? "Hide Filters" : "Show Filters"}
        />
      </div>
      <div
        data-testid="search-filters"
        className={clsx({
          "display-none": !showFilterOptions,
          "tablet:display-block": true,
        })}
      >
        <SearchOpportunityStatus query={opportunityStatus} />
        {FilterAccordions}
      </div>
    </>
  );
}
