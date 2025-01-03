import ProcessIntro from "src/app/[locale]/process/ProcessIntro";
import { render, screen } from "tests/react-utils";

describe("Process Content", () => {
  it("Renders without errors", () => {
    render(<ProcessIntro />);
    const ProcessH1 = screen.getByRole("heading", {
      level: 1,
      name: /Our open process/i,
    });

    expect(ProcessH1).toBeInTheDocument();
  });
});
