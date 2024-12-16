import { render, screen, waitFor } from "@testing-library/react";
import { axe } from "jest-axe";
import { identity } from "lodash";
import Research from "src/app/[locale]/research/page";
import { mockMessages, useTranslationsMock } from "src/utils/testing/intlMocks";

jest.mock("next-intl/server", () => ({
  getTranslations: () => identity,
  setRequestLocale: identity,
}));

jest.mock("next-intl", () => ({
  useTranslations: () => useTranslationsMock(),
  useMessages: () => mockMessages,
}));

describe("Research", () => {
  it("renders intro text", () => {
    render(Research({ params: { locale: "en" } }));

    const content = screen.getByText("intro.content");

    expect(content).toBeInTheDocument();
  });

  it("passes accessibility scan", async () => {
    const { container } = render(Research({ params: { locale: "en" } }));
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
