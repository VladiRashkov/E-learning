window.onload = function() {
  const enrolledCourses = window.enrolledCourses || [];
  console.log("Enrolled Courses: ", enrolledCourses);

  const courseContainer = document.getElementById('course-list');
  if (!courseContainer) {
    console.error('Course container not found.');
    return;
  }

  if (enrolledCourses.length === 0) {
    const messageElement = document.createElement('p');
    messageElement.className = 'no-courses-message';
    messageElement.textContent = 'No enrolled courses available.';
    courseContainer.appendChild(messageElement);
    return;
  }

  const ul = document.createElement('ul');
  enrolledCourses.forEach(course => {
    console.log("Processing course: ", course); 

    const li = document.createElement('li');

    
    const titleLink = document.createElement('a');
    titleLink.href = course.link_course ? course.link_course : `/course.html?course_id=${course.course_id}`;
    titleLink.textContent = course.title;
    titleLink.target = '_blank'; 
    console.log("Title Link URL: ", titleLink.href); 
    li.appendChild(titleLink); 

   
    li.appendChild(document.createElement('br'));

    ul.appendChild(li);
  });

  courseContainer.appendChild(ul);
};
