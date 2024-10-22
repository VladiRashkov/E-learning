window.onload = function() {
  const enrolledCourses = window.opener.enrolledCourses || [];
  
  // Get the container element where the course list will be added
  const courseContainer = document.getElementById('course-list');
  
  if (enrolledCourses.length === 0) {
    // Create a new paragraph element for the message
    const messageElement = document.createElement('p');
    messageElement.className = 'no-courses-message'; // Add the CSS class
    messageElement.textContent = 'No enrolled courses available.'; // Set the message text
    
    courseContainer.appendChild(messageElement); // Append the message to the container
    return;
  }

  // Create the list of courses with hyperlinks
  const ul = document.createElement('ul');
  enrolledCourses.forEach(course => {
    const li = document.createElement('li');
    const a = document.createElement('a');

    a.href = `/course.html?id=${course.id}`;  // Assuming course pages are dynamically generated
    a.textContent = course.title;
    a.target = '_blank';  // Open the course page in a new tab

    li.appendChild(a);
    ul.appendChild(li);
  });

  // Add the list to the container
  courseContainer.appendChild(ul);
};
