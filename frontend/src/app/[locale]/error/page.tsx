import { Metadata } from "next";

import { useTranslations } from "next-intl";
import { getTranslations } from "next-intl/server";
import { GridContainer } from "@trussworks/react-uswds";

import ServerErrorAlert from "src/components/ServerErrorAlert";

export async function generateMetadata() {
  const t = await getTranslations();
  const meta: Metadata = {
    title: t("ErrorPages.generic_error.page_title"),
    description: t("Index.meta_description"),
  };
  return meta;
}

// not a NextJS error page - this is here to be redirected to manually in cases
// where Next's error handling situation doesn't quite do what we need.
const TopLevelError = () => {
  const t = useTranslations("Errors");
  return (
    <GridContainer>
      <ServerErrorAlert callToAction={t("try_again")} />
    </GridContainer>
  );
};

export default TopLevelError;
