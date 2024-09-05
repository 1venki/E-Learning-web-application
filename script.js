function redirectToCourse(courseName) {
  // Redirect to the corresponding page with the course description
  switch (courseName) {
    case "CSPP":
      window.location.href = "/cspp-c"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    case "CSPP":
      window.location.href = "/cspp"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    case "WAD":
      window.location.href = "/wad"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    case "ICS":
      window.location.href = "ics.html"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    case "ADS":
      window.location.href = "ads.html"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    case "join":
      window.location.href = "/join"; // Replace 'cspp.html' with the actual URL of the page for CSPP course
      break;
    default:
      break;
  }
}
let activeIndex = 0;
let slides = document.querySelectorAll('.slide');

function changeSlide() {
  slides[activeIndex].classList.remove('active');
  activeIndex = (activeIndex + 1) % slides.length;
  slides[activeIndex].classList.add('active');
}

// Change slide every 3 seconds
setInterval(changeSlide, 3000);

function toggleFilterForm() {
  var filterForm = document.getElementById("filterForm");
  if (filterForm.style.display === "none") {
    filterForm.style.display = "block";
  } else {
    filterForm.style.display = "none";
  }
}

function filterCourses() {
  // Get selected filter values
  var category = document.getElementById("category").value;
  var duration = document.getElementById("duration").value;
  var startDate = document.getElementById("startDate").value;

  // Get all course items
  var courseItems = document.querySelectorAll(".course_name");

  // Loop through each course item to check if it matches the filter criteria
  courseItems.forEach(function (item) {
    // Get category, duration, and start date of the course item
    var itemCategory = item.getAttribute("data-category");
    var itemDuration = item.getAttribute("data-duration");
    var itemStartDate = item.getAttribute("data-start-date");

    // Check if the item matches the selected filters
    var showItem = true;
    if (category && category !== itemCategory) {
      showItem = false;
    }
    if (duration && duration !== itemDuration) {
      showItem = false;
    }
    if (startDate && startDate !== itemStartDate) {
      showItem = false;
    }

    // Show or hide the item based on the filter result
    if (showItem) {
      item.style.display = "flex"; // Show the item
    } else {
      item.style.display = "none"; // Hide the item
    }
  });
  document.getElementById("filterForm").reset();
}

function searchCourses() {
  // Get the search input value
  var searchText = document.querySelector(".search").value.toLowerCase();

  // Get all course items
  var courseItems = document.querySelectorAll(".course_name");

  // Loop through each course item to check if it matches the search query
  courseItems.forEach(function (item) {
    var courseName = item.querySelector(".text").textContent.toLowerCase();

    // Show or hide the course item based on the search query
    if (courseName.includes(searchText)) {
      item.style.display = "flex"; // Show the item
    } else {
      item.style.display = "none"; // Hide the item
    }
  });
  document.getElementById("search-container").reset();
}

function submitForm() {
  var form = document.getElementById("courseRegistrationForm");
  var formData = new FormData(form);

  fetch("/submit_form", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.text();
      }
      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      console.log(data); // Log response from server
      alert("Form submitted successfully!");
    })
    .catch((error) => {
      console.error("There was an error with the form submission:", error);
      alert("Error submitting form!");
    });
}

// async function sendEmail1(email, name, action) {
//   try {
//       const formData = new FormData();
//       formData.append('email', email);
//       formData.append('name', name);
//       formData.append('status', action);

//       const response = await fetch('/send-email', {
//           method: 'POST',
//           body: formData
//       });

//       if (response.ok) {
//           console.log('Email sent successfully');
//       } else {
//           console.error('Error sending email:', response.statusText);
//       }
//   } catch (error) {
//       console.error('Error sending email:', error);
//   }
// }

