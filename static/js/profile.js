const form = document.getElementById("profileForm");
const img = document.getElementById("profileImg");

// LOAD PROFILE
window.onload = () => {
  const data = JSON.parse(localStorage.getItem("facultyProfile"));
  if (!data) return;

  Object.keys(data).forEach(key => {
    if (form[key]) form[key].value = data[key];
  });

  if (data.photo) img.src = data.photo;
};

// PHOTO CHANGE
function changePhoto(e) {
  const reader = new FileReader();
  reader.onload = () => {
    img.src = reader.result;
    saveProfile({ photo: reader.result });
  };
  reader.readAsDataURL(e.target.files[0]);
}

// SAVE PROFILE
form.onsubmit = e => {
  e.preventDefault();
  const data = {};
  [...form.elements].forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  saveProfile(data);
  alert("Profile Updated Successfully!");
};

// SAVE TO STORAGE
function saveProfile(newData) {
  const old = JSON.parse(localStorage.getItem("facultyProfile")) || {};
  localStorage.setItem("facultyProfile", JSON.stringify({ ...old, ...newData }));
}
