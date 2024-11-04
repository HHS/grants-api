import { Meta } from "@storybook/react";
import OpportunityDocuments from "src/components/opportunity/OpportunityDocuments";

const meta: Meta<typeof OpportunityDocuments> = {
  title: "Components/OpportunityDocuments",
  component: OpportunityDocuments,
};
export default meta;

export const Default = {
  args: {
    documents: [
        {
            opportunity_attachment_type: "notice_of_funding_opportunity",
            file_name: "FundingInformation.pdf",
            download_path: "https://example.com",
            updated_at: "2021-10-01T00:00:00Z",
        },
        {
            opportunity_attachment_type: "other",
            file_name: "File2_ExhibitB.pdf",
            download_path: "https://example.com",
            updated_at: "2021-10-01T00:00:00Z",
        },
    ],
  },
};
