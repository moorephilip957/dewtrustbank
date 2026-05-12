document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.spinner-form');

    forms.forEach(form => {
      const button = form.querySelector('.spinner-btn');

      form.addEventListener('submit', function (event) {
        // Prevent double submission
        if (button.disabled) {
          event.preventDefault();
          return;
        }

        event.preventDefault(); // stop default for now

        // Disable button
        button.disabled = true;

        // Add spinner and text
        button.innerHTML = `
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Processing...
        `;

        // Submit the form after a tiny delay to show spinner
        setTimeout(() => form.submit(), 50);
      });
    });
  });


//   <div class="container mt-5">
//   <form method="post" class="spinner-form">
//     {% csrf_token %}
//     {{ form.as_p }}

//     <button type="submit" class="btn btn-primary spinner-btn">
//       Submit
//     </button>
//   </form>

//   <form method="post" class="spinner-form mt-4">
//     {% csrf_token %}
//     {{ form.as_p }}

//     <button type="submit" class="btn btn-success spinner-btn">
//       Send
//     </button>
//   </form>
// </div>

