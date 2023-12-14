import type { GetStaticProps, NextPage } from "next";
import { PROCESS_CRUMBS } from "src/constants/breadcrumbs";

import { useTranslation } from "next-i18next";
import { serverSideTranslations } from "next-i18next/serverSideTranslations";

import Breadcrumbs from "src/components/Breadcrumbs";
import PageSEO from "src/components/PageSEO";
import BetaAlert from "../components/BetaAlert";
import ProcessContent from "./content/ProcessIntro";
import ProcessInvolved from "./content/ProcessInvolved";
import ProcessMilestones from "./content/ProcessMilestones";

const Process: NextPage = () => {
  const { t } = useTranslation("common", { keyPrefix: "Process" });

  return (
    <>
      <PageSEO title={t("page_title")} description={t("meta_description")} />
      <BetaAlert />
      <Breadcrumbs breadcrumbList={PROCESS_CRUMBS} />
      <ProcessContent />
      <div className="padding-top-4 bg-gray-5">
        <ProcessMilestones />
      </div>
      <ProcessInvolved />
    </>
  );
};

// Change this to GetServerSideProps if you're using server-side rendering
export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale ?? "en");
  return { props: { ...translations } };
};

export default Process;
