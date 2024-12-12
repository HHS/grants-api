import { render, screen, waitFor } from "@testing-library/react";
import { axe } from "jest-axe";
import { identity } from "lodash";
import Subscribe from "src/app/[locale]/subscribe/page";
import { useTranslationsMock } from "src/utils/testing/intlMocks";

jest.mock("react-dom", () => {
  const originalModule =
    jest.requireActual<typeof import("react-dom")>("react-dom");

  return {
    ...originalModule,
    useFormStatus: jest.fn(() => ({ pending: false })),
    useFormState: () => [
      [
        {
          // Return a mock state object
          errorMessage: "errors.server",
          validationErrors: {
            name: ["errors.missing_name"],
            email: ["errors.missing_email", "errors.invalid_email"],
          },
        },
        // Mock setState function
        () => {
          ("");
        },
      ],
    ],
  };
});

jest.mock("next-intl", () => ({
  useTranslations: () => useTranslationsMock(),
}));

jest.mock("next-intl/server", () => ({
  getTranslations: () => identity,
  setRequestLocale: identity,
}));

describe("Subscribe", () => {
  it("renders intro text", () => {
    render(Subscribe({ params: { locale: "en" } }));

    const content = screen.getByText("intro");

    expect(content).toBeInTheDocument();
  });

  it("passes accessibility scan", async () => {
    const { container } = render(Subscribe({ params: { locale: "en" } }));
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
