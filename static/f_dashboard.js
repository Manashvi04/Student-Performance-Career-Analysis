// ===============================
// SECTION SWITCHING
// ===============================
function showSection(sectionId, element) {

    // Hide all sections
    document.querySelectorAll(".section").forEach(section => {
        section.classList.remove("active");
    });

    // Show selected section
    document.getElementById(sectionId).classList.add("active");

    // Remove active class from all nav links
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });

    // Add active class to clicked link
    if (element) {
        element.classList.add("active");
    }
}


// ===============================
// STUDENT SEARCH (Demo Data)
// ===============================
const students = [
    { id: "24DIT001", name: "Rahul Patel", dept: "IT" },
    { id: "24CE002", name: "Amit Shah", dept: "CE" },
    { id: "24CSE003", name: "Neha Sharma", dept: "CSE" },
    { id: "24DIT004", name: "Priya Mehta", dept: "IT" }
];

function loadStudents() {
    const container = document.getElementById("studentList");
    container.innerHTML = "";

    students.forEach(student => {
        container.innerHTML += `
            <div class="student-card">
                <h4>${student.name}</h4>
                <p>ID: ${student.id}</p>
                <p>Department: ${student.dept}</p>
            </div>
        `;
    });
}

function searchStudent(value) {
    const filtered = students.filter(student =>
        student.id.toLowerCase().includes(value.toLowerCase()) ||
        student.name.toLowerCase().includes(value.toLowerCase()) ||
        student.dept.toLowerCase().includes(value.toLowerCase())
    );

    const container = document.getElementById("studentList");
    container.innerHTML = "";

    filtered.forEach(student => {
        container.innerHTML += `
            <div class="student-card">
                <h4>${student.name}</h4>
                <p>ID: ${student.id}</p>
                <p>Department: ${student.dept}</p>
            </div>
        `;
    });
}


// ===============================
// CSV FILE PREVIEW
// ===============================
function uploadCSV(event, department) {

    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = function(e) {

        const text = e.target.result;
        const rows = text.split("\n").map(row => row.split(","));

        const tableId = department + "Table";
        const table = document.getElementById(tableId);

        table.innerHTML = "";

        rows.forEach((row, index) => {
            const tr = document.createElement("tr");

            row.forEach(cell => {
                const td = document.createElement(index === 0 ? "th" : "td");
                td.textContent = cell;
                tr.appendChild(td);
            });

            table.appendChild(tr);
        });
    };

    reader.readAsText(file);
}


// ===============================
// CHARTS
// ===============================
function createBarChart(canvasId, dataValues) {
    const ctx = document.getElementById(canvasId);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Maths", "DSA", "DBMS", "OS"],
            datasets: [{
                label: "Average Marks",
                data: dataValues
            }]
        }
    });
}

function createPieChart() {
    const ctx = document.getElementById("deptPieChart");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["IT", "CE", "CSE"],
            datasets: [{
                data: [75, 68, 82]
            }]
        }
    });
}


// ===============================
// INITIAL LOAD
// ===============================
window.onload = function () {

    loadStudents();

    // Demo charts
    createBarChart("itChart", [78, 82, 75, 80]);
    createBarChart("ceChart", [65, 70, 60, 72]);
    createBarChart("cseChart", [85, 88, 84, 90]);

    createPieChart();
};
