import { render, screen, waitFor } from "@testing-library/react";
import { axe } from "jest-axe";
import Index from "src/pages/index";

describe("Index", () => {
  // Demonstration of rendering translated text, and asserting the presence of a dynamic value.
  // You can delete this test for your own project.
  it("renders link to Next.js docs", () => {
    render(<Index />);

    const link = screen.getByRole("link", { name: /next\.js/i });

    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute("href", "https://nextjs.org/docs");
  });

  it("renders alert with grants.gov link", () => {
    render(<Index />);

    const alert = screen.getByTestId("alert");
    const link = screen.getByRole("link", { name: /grants\.gov/i });

    expect(alert).toBeInTheDocument();
    expect(link).toHaveAttribute("href", "https://www.grants.gov");
  });

  it("renders the goals section", () => {
    render(<Index />);

    const goalH2 = screen.getByRole("heading", {
      level: 2,
      name: /What's the goal?/i,
    });

    expect(goalH2).toBeInTheDocument();
  });

  it("passes accessibility scan", async () => {
    const { container } = render(<Index />);
    const results = await waitFor(() => axe(container));

    expect(results).toHaveNoViolations();
  });
});
