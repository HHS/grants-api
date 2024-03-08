export interface AssistanceListing {
  assistance_listing_number: string;
  program_title: string;
}

export interface Summary {
  additional_info_url: string | null;
  additional_info_url_description: string | null;
  agency_code: string | null;
  agency_contact_description: string | null;
  agency_email_address: string | null;
  agency_email_address_description: string | null;
  agency_name: string | null;
  agency_phone_number: string | null;
  applicant_eligibility_description: string | null;
  applicant_types: string[] | null;
  archive_date: string | null;
  award_ceiling: number | null;
  award_floor: number | null;
  close_date: string | null;
  close_date_description: string | null;
  estimated_total_program_funding: number | null;
  expected_number_of_awards: number | null;
  fiscal_year: number | null;
  forecasted_award_date: string | null;
  forecasted_close_date: string | null;
  forecasted_close_date_description: string | null;
  forecasted_post_date: string | null;
  forecasted_project_start_date: string | null;
  funding_categories: string[] | null;
  funding_category_description: string | null;
  funding_instruments: string[] | null;
  is_cost_sharing: boolean | null;
  is_forecast: boolean;
  post_date: string | null;
  summary_description: string | null;
}

export interface Opportunity {
  agency: string | null;
  category: string | null;
  category_explanation: string | null;
  created_at: string;
  opportunity_assistance_listings: AssistanceListing[];
  opportunity_id: number;
  opportunity_number: string;
  opportunity_status: string;
  opportunity_title: string;
  summary: Summary;
  updated_at: string;
}

export interface PaginationInfo {
  order_by: string;
  page_offset: number;
  page_size: number;
  sort_direction: string;
  total_pages: number;
  total_records: number;
}

export interface ApiResponse {
  data: Opportunity[];
  message: string;
  pagination_info: PaginationInfo;
  status_code: number;
  warnings?: [];
}
