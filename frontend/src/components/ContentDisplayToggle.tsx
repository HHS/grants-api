import { Dispatch, SetStateAction } from "react";

import { USWDSIcon } from "src/components/USWDSIcon";

// this could either be simpler and more generic
// or we could opt to build the entire show / hide functionality into this component and pass the content controlled by the toggle as children
export default function ContentDisplayToggle({
  setToggledContentVisible,
  toggledContentVisible,
  toggleText,
}: {
  setToggledContentVisible: Dispatch<SetStateAction<boolean>>;
  toggledContentVisible: boolean;
  toggleText: string;
}) {
  const iconName = toggledContentVisible ? "arrow_drop_up" : "arrow_drop_down";
  return (
    <div
      data-testid="content-display-toggle"
      className="grants-toggle grid-col-4"
    >
      <a
        onClick={(_event) => setToggledContentVisible(!toggledContentVisible)}
        aria-pressed={toggledContentVisible}
        className="usa-link text-bold grants-toggle-button"
      >
        <USWDSIcon name={iconName} className="usa-icon usa-icon--size-4" />
        <span>{toggleText}</span>
      </a>
    </div>
  );
}
