import pick from "lodash/pick";
import { featureFlags } from "src/constants/environments";
import FeatureFlagProvider from "src/services/featureFlags/FeatureFlagProvider";

import {
  NextIntlClientProvider,
  useMessages,
  useTranslations,
} from "next-intl";
import { setRequestLocale } from "next-intl/server";

import Footer from "src/components/Footer";
import GrantsIdentifier from "src/components/GrantsIdentifier";
import Header from "src/components/Header";

type Props = {
  children: React.ReactNode;
  locale: string;
};

export default function Layout({ children, locale }: Props) {
  setRequestLocale(locale);

  const t = useTranslations();
  const messages = useMessages();

  return (
    // Stick the footer to the bottom of the page
    <div className="display-flex flex-column minh-viewport">
      <a className="usa-skipnav" href="#main-content">
        {t("Layout.skip_to_main")}
      </a>
      <NextIntlClientProvider
        locale={locale}
        messages={pick(messages, "Header")}
      >
        <FeatureFlagProvider serverSideFlags={featureFlags}>
          <Header locale={locale} />
        </FeatureFlagProvider>
      </NextIntlClientProvider>
      <main id="main-content">{children}</main>
      <Footer />
      <GrantsIdentifier />
    </div>
  );
}
