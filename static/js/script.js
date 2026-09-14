const medicalText = document.getElementById("medicalText");

const analyzeButton = document.getElementById("analyzeButton");

const buttonText = document.getElementById("buttonText");

const loader = document.getElementById("loader");

const clearButton = document.getElementById("clearButton");

const sampleButton = document.getElementById("sampleButton");

const characterCount = document.getElementById("characterCount");

const resultsSection = document.getElementById("resultsSection");

const entityCount = document.getElementById("entityCount");

const entityCards = document.getElementById("entityCards");

const highlightedText = document.getElementById("highlightedText");

const errorMessage = document.getElementById("errorMessage");


const SAMPLE_TEXT = `
The patient has been experiencing high fever, severe headache,
cough and fatigue for three days. The patient also reports
shortness of breath.

The doctor diagnosed the patient with influenza and prescribed
Paracetamol 500 mg twice daily for five days.

The patient was advised to monitor blood pressure and heart rate.
`.trim();


/* =========================
   CHARACTER COUNT
========================= */

medicalText.addEventListener("input", () => {

    const count = medicalText.value.length;

    characterCount.textContent =
        `${count.toLocaleString()} characters`;

});


/* =========================
   LOAD SAMPLE
========================= */

sampleButton.addEventListener("click", () => {

    medicalText.value = SAMPLE_TEXT;

    updateCharacterCount();

    hideError();

    medicalText.focus();

});


/* =========================
   CLEAR
========================= */

clearButton.addEventListener("click", () => {

    medicalText.value = "";

    updateCharacterCount();

    resultsSection.classList.add("hidden");

    entityCards.innerHTML = "";

    highlightedText.innerHTML = "";

    hideError();

    medicalText.focus();

});


/* =========================
   ANALYZE
========================= */

analyzeButton.addEventListener("click", analyzeText);


async function analyzeText() {

    const text = medicalText.value.trim();


    if (!text) {

        showError(
            "Please enter medical text before analyzing."
        );

        return;
    }


    setLoading(true);

    hideError();


    try {

        const response = await fetch(
            "/api/extract",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Unable to process the medical text."
            );

        }


        displayResults(data);

    }

    catch (error) {

        showError(
            error.message ||
            "Something went wrong while processing the text."
        );

    }

    finally {

        setLoading(false);

    }

}


/* =========================
   DISPLAY RESULTS
========================= */

function displayResults(data) {

    resultsSection.classList.remove("hidden");


    entityCount.textContent =
        `${data.entity_count} ${
            data.entity_count === 1
                ? "entity"
                : "entities"
        }`;


    renderEntityCards(data.grouped_entities);

    renderHighlightedText(
        data.input_text,
        data.entities
    );


    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =========================
   ENTITY CARDS
========================= */

function renderEntityCards(groupedEntities) {

    entityCards.innerHTML = "";


    const labels = [
        "SYMPTOM",
        "MEDICINE",
        "DISEASE",
        "MEDICAL_TERM",
        "DOSAGE",
        "FREQUENCY",
        "DURATION"
    ];


    labels.forEach(label => {

        const entities =
            groupedEntities[label];


        if (!entities || entities.length === 0) {
            return;
        }


        const card =
            document.createElement("div");

        card.className = "entity-card";


        const header =
            document.createElement("div");

        header.className =
            "entity-card-header";


        const labelElement =
            document.createElement("span");

        labelElement.className =
            `entity-label ${getLabelClass(label)}`;

        labelElement.textContent =
            formatLabel(label);


        const number =
            document.createElement("span");

        number.className =
            "entity-number";

        number.textContent =
            `${entities.length} found`;


        header.appendChild(labelElement);

        header.appendChild(number);


        const list =
            document.createElement("div");

        list.className =
            "entity-list";


        entities.forEach(entity => {

            const tag =
                document.createElement("span");

            tag.className =
                "entity-tag";

            tag.textContent =
                `${entity.text} (${entity.source || "NLP"})`;

            list.appendChild(tag);

        });


        card.appendChild(header);

        card.appendChild(list);

        entityCards.appendChild(card);

    });


    if (!entityCards.children.length) {

        entityCards.innerHTML = `
            <div class="entity-card">
                No predefined medical entities were detected.
            </div>
        `;

    }

}


/* =========================
   HIGHLIGHT TEXT
========================= */

function renderHighlightedText(text, entities) {

    if (!entities || entities.length === 0) {

        highlightedText.textContent = text;

        return;
    }


    const sortedEntities =
        [...entities].sort(
            (a, b) => a.start - b.start
        );


    let html = "";

    let currentPosition = 0;


    sortedEntities.forEach(entity => {

        const start = entity.start;

        const end = entity.end;


        if (start < currentPosition) {
            return;
        }


        html += escapeHtml(
            text.slice(
                currentPosition,
                start
            )
        );


        const entityText =
            escapeHtml(
                text.slice(start, end)
            );


        const labelClass =
            getLabelClass(entity.label);


        html += `
            <span
                class="entity-highlight ${labelClass}"
                title="${formatLabel(entity.label)}"
            >
                ${entityText}
            </span>
        `;


        currentPosition = end;

    });


    html += escapeHtml(
        text.slice(currentPosition)
    );


    highlightedText.innerHTML = html;

}


/* =========================
   HELPERS
========================= */

function formatLabel(label) {

    return label
        .toLowerCase()
        .replace(/_/g, " ")
        .replace(/\b\w/g, char =>
            char.toUpperCase()
        );

}


function getLabelClass(label) {

    const classes = {

        SYMPTOM: "symptom",

        MEDICINE: "medicine",

        DISEASE: "disease",

        MEDICAL_TERM: "medical-term",

        DOSAGE: "dosage",

        FREQUENCY: "frequency",

        DURATION: "duration"

    };


    return classes[label] || "";

}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


function updateCharacterCount() {

    const count =
        medicalText.value.length;

    characterCount.textContent =
        `${count.toLocaleString()} characters`;

}


function setLoading(isLoading) {

    analyzeButton.disabled =
        isLoading;


    if (isLoading) {

        buttonText.textContent =
            "Analyzing...";

        loader.classList.remove("hidden");

    }

    else {

        buttonText.textContent =
            "Analyze Medical Text";

        loader.classList.add("hidden");

    }

}


function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove("hidden");

}


function hideError() {

    errorMessage.classList.add("hidden");

    errorMessage.textContent = "";

}




function updateStatistics(entities) {

    const symptomCount =
        entities.filter(
            entity => entity.label === "SYMPTOM"
        ).length;


    const medicineCount =
        entities.filter(
            entity => entity.label === "MEDICINE"
        ).length;


    const diseaseCount =
        entities.filter(
            entity => entity.label === "DISEASE"
        ).length;


    document.getElementById(
        "symptomCount"
    ).textContent = symptomCount;


    document.getElementById(
        "medicineCount"
    ).textContent = medicineCount;


    document.getElementById(
        "diseaseCount"
    ).textContent = diseaseCount;


    document.getElementById(
        "totalCount"
    ).textContent = entities.length;
}


updateStatistics(data.entities);

function saveHistory(text, entities) {

    const history =
        JSON.parse(
            localStorage.getItem(
                "medextract_history"
            )
        ) || [];


    history.unshift({

        text: text,

        entityCount: entities.length,

        timestamp:
            new Date().toLocaleString()

    });


    const limitedHistory =
        history.slice(0, 10);


    localStorage.setItem(
        "medextract_history",
        JSON.stringify(limitedHistory)
    );
}

saveHistory(
    inputText,
    data.entities
);


function renderHistory() {

    const history =
        JSON.parse(
            localStorage.getItem(
                "medextract_history"
            )
        ) || [];


    const container =
        document.getElementById(
            "historyList"
        );


    container.innerHTML = "";


    if (history.length === 0) {

        container.innerHTML =
            "<p>No extraction history yet.</p>";

        return;
    }


    history.forEach(item => {

        const element =
            document.createElement("div");


        element.className =
            "history-item";


        element.innerHTML = `
            <div>
                <strong>
                    ${escapeHtml(
                        item.text.slice(0, 100)
                    )}
                </strong>

                <small>
                    ${item.timestamp}
                </small>
            </div>

            <span>
                ${item.entityCount} entities
            </span>
        `;


        container.appendChild(element);

    });
}



function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}

escapeHtml(userText)


document
    .getElementById("clearHistory")
    .addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "medextract_history"
            );

            renderHistory();
        }
    );

renderHistory();


function downloadJSON(data) {

    const json =
        JSON.stringify(
            data,
            null,
            2
        );


    const blob =
        new Blob(
            [json],
            {
                type: "application/json"
            }
        );


    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download =
        "medical_extraction.json";


    link.click();


    URL.revokeObjectURL(url);
}

let latestResult = null;

latestResult = data;

document
    .getElementById("downloadJson")
    .addEventListener(
        "click",
        () => {

            if (!latestResult) {

                alert(
                    "Run extraction first."
                );

                return;
            }


            downloadJSON(
                latestResult
            );
        }
    );


function downloadCSV(entities) {

    const headers = [
        "Text",
        "Label",
        "Source",
        "Start",
        "End"
    ];


    const rows = entities.map(
        entity => [

            entity.text,

            entity.label,

            entity.source || "",

            entity.start,

            entity.end

        ]
    );


    const csv = [
        headers,
        ...rows
    ]
        .map(
            row =>
                row.map(
                    value =>
                        `"${String(value)
                            .replaceAll('"', '""')}"`
                ).join(",")
        )
        .join("\n");


    const blob =
        new Blob(
            [csv],
            {
                type: "text/csv"
            }
        );


    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download =
        "medical_entities.csv";


    link.click();


    URL.revokeObjectURL(url);
}