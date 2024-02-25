document.querySelectorAll('input[type="radio"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
      var eventId = this.getAttribute('name').split('-')[0];
      var coordinatorApproval = document.querySelector('input[name="' + eventId + '-coordinator"]:checked');
      var hodApproval = document.querySelector('input[name="' + eventId + '-hod"]:checked');
      var principalApproval = document.querySelector('input[name="' + eventId + '-principal"]:checked');
  
      if (coordinatorApproval && hodApproval && principalApproval) {
        if (coordinatorApproval.value === 'yes' && hodApproval.value === 'yes' && principalApproval.value === 'yes') {
          alert("Event Approved!");
          // Here you can make an AJAX call to update the backend
          $.ajax({
            type: 'POST',               // HTTP method (POST in this case)
            url: '/update_status',      // URL to send the request to
            data: { status: 'approved' }, // Data to send in the request body
            success: function(response) { // Function to execute if the request succeeds
                alert('Status updated to approved');
            },
            error: function(xhr, status, error) { // Function to execute if the request fails
                console.error('Error updating status:', error);
            }
        });
        } else {
          alert("Event not approved.");
        }
      }
    });
  });
  