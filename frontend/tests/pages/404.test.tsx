import { render, screen, waitFor } from "@testing-library/react";
import { axe } from "jest-axe";
import PageNotFound from "src/app/not-found";

describe("PageNotFound", () => {
  it("renders alert with grants.gov link", () => {
    render(<PageNotFound />);

    const alert = screen.queryByTestId("alert");

    expect(alert).toBeInTheDocument();
  });

  it("links back to the home page", () => {
    render(<PageNotFound />);
    const link = screen.getByRole("link", { name: /Return Home/i });

    expect(link).toBeInTheDocument();
  });

  it("passes accessibility scan", async () => {
    const { container } = render(<PageNotFound />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
