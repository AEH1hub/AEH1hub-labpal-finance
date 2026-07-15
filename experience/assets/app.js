const scenarioSelect = document.querySelector(
  "#scenario-select"
);
const statusElement = document.querySelector(
  "#experience-status"
);
const experienceElement = document.querySelector(
  "#reasoning-experience"
);

function setText(selector, value) {
  const element = document.querySelector(selector);
  element.textContent = value ?? "Not recorded";
}

function renderList(selector, values, emptyMessage) {
  const list = document.querySelector(selector);
  list.replaceChildren();

  if (!Array.isArray(values) || values.length === 0) {
    const item = document.createElement("li");
    item.className = "empty-state";
    item.textContent = emptyMessage;
    list.append(item);
    return;
  }

  for (const value of values) {
    const item = document.createElement("li");
    item.textContent = value;
    list.append(item);
  }
}

function renderExperience(payload) {
  const result = payload.result;
  const question = result.preserved_question;
  const understanding = result.current_understanding;

  setText("#question-text", question.original_question);
  setText("#question-type", question.question_type);
  setText("#evidence-mode", question.evidence_mode);
  setText(
    "#action-boundary",
    question.action_boundary_state
  );
  setText("#execution-id", result.execution_id);

  setText(
    "#understanding-statement",
    understanding.current_statement
  );
  setText(
    "#verification-notice",
    understanding.verification_notice
  );

  setText("#decision-state", result.decision_state);
  setText("#review-state", result.review_state);
  setText("#reasoning-summary", result.reasoning_summary);

  renderList(
    "#evidence-list",
    result.evidence_considered,
    "No evidence was considered within this scope."
  );

  renderList(
    "#unknown-list",
    result.unknowns,
    "No material unknown was recorded within this scope."
  );

  renderList(
    "#contradiction-list",
    result.contradictions,
    "No contradiction was recorded within this scope."
  );

  renderList(
    "#next-evidence-list",
    result.next_evidence_needed,
    "No next evidence requirement was recorded."
  );

  document.querySelector("#raw-json").textContent =
    JSON.stringify(payload, null, 2);

  statusElement.textContent =
    "Reasoning experience loaded.";
  experienceElement.hidden = false;
}

async function loadScenario(scenarioId) {
  statusElement.textContent =
    "Loading reasoning experience…";
  experienceElement.hidden = true;

  try {
    const response = await fetch(
      `./data/${scenarioId}.json`
    );

    if (!response.ok) {
      throw new Error(
        `Scenario request failed with ${response.status}.`
      );
    }

    const payload = await response.json();
    renderExperience(payload);
  } catch (error) {
    statusElement.textContent =
      "The reasoning experience could not be loaded.";
    console.error(error);
  }
}

scenarioSelect.addEventListener("change", () => {
  loadScenario(scenarioSelect.value);
});

loadScenario(scenarioSelect.value);
