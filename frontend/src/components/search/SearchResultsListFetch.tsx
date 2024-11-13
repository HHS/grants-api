import { SearchAPIResponse } from "src/types/search/searchResponseTypes";

import { getTranslations } from "next-intl/server";

import SearchResultsListItem from "src/components/search/SearchResultsListItem";
import ServerErrorAlert from "src/components/ServerErrorAlert";

interface ServerPageProps {
  searchResultsPromise: Promise<SearchAPIResponse>;
}

export default async function SearchResultsListFetch({
  searchResultsPromise,
}: ServerPageProps) {
  const searchResults = await searchResultsPromise;
  const maxPaginationError = null;
  const t = await getTranslations("Search");

  if (searchResults.status_code !== 200) {
    return <ServerErrorAlert callToAction={t("generic_error_cta")} />;
  }

  if (searchResults.data.length === 0) {
    return (
      <div>
        <h2>{t("resultsListFetch.title")}</h2>
        <ul>
          {t.rich("resultsListFetch.body", {
            li: (chunks) => <li>{chunks}</li>,
          })}
        </ul>
      </div>
    );
  }

  return (
    <ul className="usa-list--unstyled">
      {/* TODO #1485: show proper USWDS error  */}
      {maxPaginationError && <h4>{t("resultsListFetch.paginationError")}</h4>}
      {searchResults.data.map((opportunity) => (
        <li key={opportunity?.opportunity_id}>
          <SearchResultsListItem opportunity={opportunity} />
        </li>
      ))}
    </ul>
  );
}
