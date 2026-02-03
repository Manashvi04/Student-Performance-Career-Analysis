/* =====================================================
   SECTION NAVIGATION (SIDEBAR ACTIVE & PAGE SWITCH)
===================================================== */

function showSection(id, element) {
  // Hide all sections
  document.querySelectorAll('.section').forEach(sec => {
    sec.classList.remove('active');
  });

  // Show selected section
  const section = document.getElementById(id);
  if (section) section.classList.add('active');

  // Remove active class from all sidebar links
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.classList.remove('active');
  });

  // Add active class to clicked link
  if (element) element.classList.add('active');
}


/* =====================================================
   ACADEMIC STUDENT DATA (FOR MARKS & ANALYTICS)
===================================================== */

const academicStudents = [
  { roll:101, name:"Aarav Patel", class:"CE-A",
    marks:{ CN:78, DBMS:82, OS:75, Extra:80 } },

  { roll:102, name:"Neha Sharma", class:"CE-A",
    marks:{ CN:88, DBMS:91, OS:90, Extra:92 } },

  { roll:103, name:"Rohan Mehta", class:"CE-A",
    marks:{ CN:70, DBMS:68, OS:72, Extra:74 } },

  { roll:104, name:"Isha Verma", class:"CE-B",
    marks:{ CN:85, DBMS:87, OS:83, Extra:86 } },

  { roll:105, name:"Kunal Joshi", class:"CE-B",
    marks:{ CN:76, DBMS:79, OS:80, Extra:82 } },

  { roll:106, name:"Pooja Singh", class:"CE-B",
    marks:{ CN:90, DBMS:93, OS:91, Extra:95 } }
];


/* =====================================================
   CSV FILE UPLOAD & PREVIEW
===================================================== */

function uploadCSV(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();

  reader.onload = () => {
    const rows = reader.result.split("\n");
    let html = `<tr>
                  <th>Roll No</th>
                  <th>Subject</th>
                  <th>Marks</th>
                </tr>`;

    rows.forEach(row => {
      const cols = row.split(",");
      if (cols.length >= 3) {
        html += `<tr>
                   <td>${cols[0]}</td>
                   <td>${cols[1]}</td>
                   <td>${cols[2]}</td>
                 </tr>`;
      }
    });

    document.getElementById("previewTable").innerHTML = html;
  };

  reader.readAsText(file);
}


/* =====================================================
   CLASS AVERAGE BAR CHART
===================================================== */

const classAverage = {
  CN: 82,
  DBMS: 85,
  OS: 81,
  Extra: 85
};

new Chart(document.getElementById("classChart"), {
  type: "bar",
  data: {
    labels: Object.keys(classAverage),
    datasets: [{
      label: "Class Average Marks",
      data: Object.values(classAverage)
    }]
  }
});


/* =====================================================
   INDIVIDUAL STUDENT PERFORMANCE GRAPH
===================================================== */

let studentChart = null;

function drawStudentGraph(roll) {
  const student = academicStudents.find(s => s.roll === roll);
  if (!student) return;

  // Destroy previous chart before creating new
  if (studentChart) studentChart.destroy();

  studentChart = new Chart(
    document.getElementById("studentChart"),
    {
      type: "line",
      data: {
        labels: Object.keys(student.marks),
        datasets: [{
          label: student.name,
          data: Object.values(student.marks),
          fill: false
        }]
      }
    }
  );

  // Auto-switch to analytics section
  showSection("analytics");
}


/* =====================================================
   DEPARTMENT-WISE STUDENT LIST (STATIC DISPLAY)
===================================================== */

const departmentStudents = [

  // IT STUDENTS
  { id:"IT1", name:"Rahul Sharma", dept:"IT" },
  { id:"IT2", name:"Ankit Verma", dept:"IT" },
  { id:"IT3", name:"Riya Patel", dept:"IT" },
  { id:"IT4", name:"Sneha Joshi", dept:"IT" },
  { id:"IT5", name:"Aman Gupta", dept:"IT" },
  { id:"IT6", name:"Kunal Mehta", dept:"IT" },
  { id:"IT7", name:"Pooja Shah", dept:"IT" },
  { id:"IT8", name:"Nikhil Jain", dept:"IT" },
  { id:"IT9", name:"Neha Singh", dept:"IT" },
  { id:"IT10", name:"Arjun Rao", dept:"IT" },

  // CE STUDENTS
  { id:"CE1", name:"Harsh Patel", dept:"CE" },
  { id:"CE2", name:"Yash Trivedi", dept:"CE" },
  { id:"CE3", name:"Mehul Desai", dept:"CE" },
  { id:"CE4", name:"Priya Modi", dept:"CE" },
  { id:"CE5", name:"Dhruv Shah", dept:"CE" },
  { id:"CE6", name:"Kiran Solanki", dept:"CE" },
  { id:"CE7", name:"Nisha Parmar", dept:"CE" },
  { id:"CE8", name:"Sahil Vyas", dept:"CE" },
  { id:"CE9", name:"Krupa Patel", dept:"CE" },
  { id:"CE10", name:"Rohit Dave", dept:"CE" },

  // CSE STUDENTS
  { id:"CSE1", name:"Aakash Malhotra", dept:"CSE" },
  { id:"CSE2", name:"Simran Kaur", dept:"CSE" },
  { id:"CSE3", name:"Vivek Mishra", dept:"CSE" },
  { id:"CSE4", name:"Isha Roy", dept:"CSE" },
  { id:"CSE5", name:"Mohit Yadav", dept:"CSE" },
  { id:"CSE6", name:"Ananya Sen", dept:"CSE" },
  { id:"CSE7", name:"Ritesh Kumar", dept:"CSE" },
  { id:"CSE8", name:"Payal Thakur", dept:"CSE" },
  { id:"CSE9", name:"Suman Das", dept:"CSE" },
  { id:"CSE10", name:"Aditya Bose", dept:"CSE" }
];


/* =====================================================
   DISPLAY STUDENT LIST
===================================================== */

function displayStudents(list) {
  let html = `
    <div class="student-row header">
      <span>ID</span>
      <span>Name</span>
      <span>Department</span>
    </div>
  `;

  list.forEach(s => {
    html += `
      <div class="student-row">
        <span>${s.id}</span>
        <span>${s.name}</span>
        <span>${s.dept}</span>
      </div>
    `;
  });

  document.getElementById("studentList").innerHTML = html;
}


/* =====================================================
   SEARCH STUDENT (ID / NAME / DEPARTMENT)
===================================================== */

function searchStudent(value) {
  value = value.toLowerCase();

  const filtered = departmentStudents.filter(s =>
    s.id.toLowerCase().includes(value) ||
    s.name.toLowerCase().includes(value) ||
    s.dept.toLowerCase().includes(value)
  );

  displayStudents(filtered);
}

// Load all students when page loads
displayStudents(departmentStudents);


/* =====================================================
   LOAD FACULTY DATA FROM LOCAL STORAGE (SIDEBAR)
===================================================== */

const profile = JSON.parse(localStorage.getItem("facultyProfile"));

if (profile) {
  if (profile.photo)
    document.getElementById("sidebarPhoto").src = profile.photo;

  if (profile.displayName)
    document.getElementById("sidebarName").innerText = profile.displayName;

  if (profile.department)
    document.getElementById("sidebarDept").innerText = profile.department;
}


/* =====================================================
   DEPARTMENT-WISE SUBJECT AVERAGE (STATIC DATA)
===================================================== */

const subjects = ["CN", "DBMS", "OS", "Maths", "AI"];

// IT Department Average
const itData = [78, 82, 75, 80, 76];

// CE Department Average
const ceData = [82, 85, 81, 84, 80];

// CSE Department Average
const cseData = [88, 90, 86, 89, 92];


/* =====================================================
   CREATE CHART FUNCTION
===================================================== */

function createBarChart(canvasId, label, data) {
  new Chart(document.getElementById(canvasId), {
    type: "bar",
    data: {
      labels: subjects,
      datasets: [{
        label: label,
        data: data
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}


/* =====================================================
   INITIALIZE ALL DEPARTMENT CHARTS
===================================================== */

createBarChart("itChart", "IT Average Marks", itData);
createBarChart("ceChart", "CE Average Marks", ceData);
createBarChart("cseChart", "CSE Average Marks", cseData);

/* =====================================================
   OVERALL DEPARTMENT PERFORMANCE (PIE CHART)
===================================================== */

// Average score of each department (static demo)
const deptOverall = {
  IT: 78,
  CE: 82,
  CSE: 89
};

new Chart(document.getElementById("deptPieChart"), {
  type: "pie",
  data: {
    labels: Object.keys(deptOverall),
    datasets: [{
      data: Object.values(deptOverall)
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom"
      }
    }
  }
});

/* =====================================================
   DEPARTMENT-WISE CSV UPLOAD PREVIEW
===================================================== */

function uploadCSV(event, department) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    const rows = reader.result.split("\n");
    let html = `
      <tr>
        <th>Roll No</th>
        <th>Subject</th>
        <th>Marks</th>
      </tr>
    `;

    rows.forEach(row => {
      const cols = row.split(",");
      if (cols.length >= 3) {
        html += `
          <tr>
            <td>${cols[0]}</td>
            <td>${cols[1]}</td>
            <td>${cols[2]}</td>
          </tr>
        `;
      }
    });

    document.getElementById(department + "Table").innerHTML = html;
  };

  reader.readAsText(file);
}
