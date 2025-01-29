# ruff: noqa: SLF001
# pylint: disable=protected-access
"""Test the GitHubProjectETL class."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from analytics.datasets.issues import GitHubIssues, IssueType
from analytics.etl.github import (
    GitHubProjectConfig,
    GitHubProjectETL,
    InputFiles,
    RoadmapConfig,
    SprintBoardConfig,
    get_parent_with_type,
    populate_issue_lookup_table,
)
from analytics.integrations import github

from tests.conftest import issue

# ===========================================================
# Fixtures
# ===========================================================


@pytest.fixture(name="config")
def mock_config(tmp_path: Path) -> GitHubProjectConfig:
    """Fixture to create a sample configuration for testing."""
    return GitHubProjectConfig(
        roadmap_project=RoadmapConfig(owner="test_owner", project_number=1),
        sprint_projects=[SprintBoardConfig(owner="test_owner", project_number=2)],
        temp_dir=str(tmp_path),
    )


@pytest.fixture(name="etl")
def mock_etl(config: GitHubProjectConfig):
    """Fixture to initialize the ETL pipeline."""
    return GitHubProjectETL(config)


@pytest.fixture(name="sprint_file")
def mock_sprint_data_file(config: GitHubProjectConfig) -> list[dict]:
    """Create mock sprint data exported from GitHub."""
    # Arrange - create dummy sprint data

    sprint_data = [
        issue(issue=1, kind=IssueType.TASK, parent="Epic3", points=2),
        issue(issue=2, kind=IssueType.TASK, parent="Epic4", points=1),
    ]
    return [i.model_dump() for i in sprint_data]



@pytest.fixture(name="roadmap_file")
def mock_roadmap_data_file(config: GitHubProjectConfig) -> list[dict]:
    """Create mock sprint data exported from GitHub."""
    roadmap_data = [
        issue(issue=3, kind=IssueType.EPIC, parent="Deliverable5"),
        issue(issue=4, kind=IssueType.EPIC, parent="Deliverable6"),
        issue(issue=5, kind=IssueType.DELIVERABLE, quad="quad1"),
    ]
    return [i.model_dump() for i in roadmap_data]



# ===========================================================
# Test ETL class
# ===========================================================


class TestGitHubProjectETL:
    """Tests the GitHubProjectETL class."""

    def test_extract(
        self,
        monkeypatch: pytest.MonkeyPatch,
        etl: GitHubProjectETL,
    ):
        """Test the extract step by mocking export functions."""
        mock_export_roadmap_data = MagicMock()
        mock_export_sprint_data = MagicMock()
        monkeypatch.setattr(etl, "_export_roadmap_data", mock_export_roadmap_data)
        monkeypatch.setattr(etl, "_export_sprint_data", mock_export_sprint_data)

        # Run the extract method
        etl.extract()

        # Assert roadmap export was called with expected arguments
        roadmap = etl.config.roadmap_project
        mock_export_roadmap_data.assert_called_once_with(
            roadmap=roadmap,
        )

        # Assert sprint export was called with expected arguments
        sprint_board = etl.config.sprint_projects[0]
        mock_export_sprint_data.assert_called_once_with(
            sprint_board=sprint_board,
        )

        # Verify transient files were set correctly
        assert etl._transient_files is not None

    def test_transform(
        self,
        etl: GitHubProjectETL,
        sprint_file: list[dict],
        roadmap_file: list[dict],
    ):
        """Test the transform step by mocking GitHubIssues.load_from_json_files."""
        # Arrange
        output_data = [
            issue(
                issue=1,
                points=2,
                parent="Epic3",
                deliverable="Deliverable5",
                quad="quad1",
                epic="Epic3",
            ),
            issue(
                issue=2,
                points=1,
                parent="Epic4",
                deliverable=None,
                quad=None,
                epic="Epic4",
            ),
        ]
        wanted = [i.model_dump() for i in output_data]
        etl._transient_files = [InputFiles(roadmap=roadmap_file, sprint=sprint_file)]
        # Act
        etl.transform()
        # Assert
        assert etl.dataset.to_dict() == wanted

    def test_load(self, etl: GitHubProjectETL):
        """Test the load step by mocking the to_json method."""
        etl.dataset = MagicMock()

        # Run the load method
        outcome: GitHubIssues = etl.load()

        # Check if to_json was called with the correct output file
        assert outcome is not None

    def test_run(
        self,
        monkeypatch: pytest.MonkeyPatch,
        etl: GitHubProjectETL,
        sprint_file: list[dict],
        roadmap_file: list[dict],
    ):
        """Test the entire ETL pipeline by verifying method calls in run."""
        # Arrange - Mock the export functions with sample sprint and roadmap data
        mock_export_roadmap = MagicMock(return_value=roadmap_file)
        mock_export_sprint = MagicMock(return_value=sprint_file)
        monkeypatch.setattr(github, "export_roadmap_data", mock_export_roadmap)
        monkeypatch.setattr(github, "export_sprint_data", mock_export_sprint)

        # Arrange - specify the output wanted
        output_data = [
            issue(
                issue=1,
                points=2,
                parent="Epic3",
                deliverable="Deliverable5",
                quad="quad1",
                epic="Epic3",
            ),
            issue(
                issue=2,
                points=1,
                parent="Epic4",
                deliverable=None,
                quad=None,
                epic="Epic4",
            ),
        ]
        dataset_wanted = [i.model_dump() for i in output_data]
        files_wanted = [InputFiles(roadmap=roadmap_file, sprint=sprint_file)]

        # Act - run the ETL
        etl.run()

        # Assert
        assert etl._transient_files == files_wanted
        assert etl.dataset.to_dict() == dataset_wanted


# ===========================================================
# Test ETL helper functions
# ===========================================================


class TestPopulateLookupTable:
    """Test the populate_lookup_table() function."""

    def test_drop_issues_with_validation_errors(self):
        """Issues with validation errors should be excluded from the lookup table."""
        # Arrange
        test_data = [
            issue(issue=1).model_dump(),
            issue(issue=2).model_dump(),
            {
                "issue_url": "bad_issue",
                "issue_points": "foo",
            },  # missing required field and wrong type for points
        ]
        wanted = 2
        # Act
        got = populate_issue_lookup_table(lookup={}, issues=test_data)
        # Assert
        assert len(got) == wanted
        assert "bad_issue" not in got


class TestGetParentWithType:
    """Test the get_parent_with_type() method."""

    def test_return_epic_that_is_direct_parent_of_issue(self):
        """Return the correct epic for an issue that is one level down."""
        # Arrange
        task = "Task1"
        epic = "Epic1"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK, parent=epic),
            epic: issue(issue=2, kind=IssueType.EPIC, parent=None),
        }
        wanted = lookup[epic]
        # Act
        got = get_parent_with_type(
            child_url=task,
            lookup=lookup,
            type_wanted=IssueType.EPIC,
        )
        # Assert
        assert got == wanted

    def test_return_correct_deliverable_that_is_grandparent_of_issue(self):
        """Return the correct deliverable for an issue that is two levels down."""
        # Arrange
        task = "Task1"
        epic = "Epic2"
        deliverable = "Deliverable3"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK, parent=epic),
            epic: issue(issue=2, kind=IssueType.EPIC, parent=deliverable),
            deliverable: issue(issue=3, kind=IssueType.DELIVERABLE, parent=None),
        }
        wanted = lookup[deliverable]
        # Act
        got = get_parent_with_type(
            child_url=task,
            lookup=lookup,
            type_wanted=IssueType.DELIVERABLE,
        )
        # Assert
        assert got == wanted

    def test_return_none_if_issue_has_no_parent(self):
        """Return None if the input issue has no parent."""
        # Arrange
        task = "task"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK, parent=None),
        }
        wanted = None
        # Act
        got = get_parent_with_type(
            child_url=task,
            lookup=lookup,
            type_wanted=IssueType.DELIVERABLE,
        )
        # Assert
        assert got == wanted

    def test_return_none_if_parents_form_a_cycle(self):
        """Return None if the issue hierarchy forms a cycle."""
        # Arrange
        task = "Task1"
        parent = "Task2"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK, parent="parent"),
            parent: issue(issue=2, kind=IssueType.TASK, parent=task),
        }
        wanted = None
        # Act
        got = get_parent_with_type(
            child_url=task,
            lookup=lookup,
            type_wanted=IssueType.DELIVERABLE,
        )
        # Assert
        assert got == wanted

    def test_return_none_if_deliverable_is_not_found_in_parents(self):
        """Return None if the desired type (e.g. epic) isn't found in the list of parents."""
        # Arrange
        task = "Task1"
        parent = "Task2"
        epic = "Epic3"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK, parent=parent),
            parent: issue(issue=2, kind=IssueType.TASK, parent=epic),
            epic: issue(issue=3, kind=IssueType.EPIC, parent=task),
        }
        wanted = None
        # Act
        got = get_parent_with_type(
            child_url=task,
            lookup=lookup,
            type_wanted=IssueType.DELIVERABLE,
        )
        # Assert
        assert got == wanted

    def test_raise_value_error_if_child_url_not_in_lookup(self):
        """Raise a value error if the child_url isn't found in lookup table."""
        # Arrange
        task = "Task1"
        lookup = {
            task: issue(issue=1, kind=IssueType.TASK),
        }
        # Act
        with pytest.raises(ValueError, match="Lookup doesn't contain"):
            get_parent_with_type(
                child_url="fake",
                lookup=lookup,
                type_wanted=IssueType.DELIVERABLE,
            )
